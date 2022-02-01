import json
from urllib.parse import quote_plus, unquote

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.signing import Signer, BadSignature
from django.http import HttpResponseRedirect, HttpResponseForbidden, HttpResponseBadRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy, reverse
from django.utils.datastructures import MultiValueDictKeyError
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET
from requests import RequestException

from assessment.forms import AssessmentForm, QuestionForm, StartAssessmentSelfForm
from assessment.models import Question, Assessment, Answer, AnswerSubmission, AssessmentAttempt
from assessment.services import Judge0, CodeMirrorMode, CodeMod
from codetester.local import HOST_URL


@login_required
def assessment_create(request):
    if request.method == "POST":
        assessment_form = AssessmentForm(request.POST)
        if assessment_form.is_valid():
            assessment_form.instance.author = request.user
            assessment = assessment_form.save()
            messages.add_message(request, messages.SUCCESS, "Assessment Created")
            return HttpResponseRedirect(reverse_lazy('assessment:assessment_update', args=(assessment.id,)))
    else:
        assessment_form = AssessmentForm()

    return render(request, 'assessment/assessment_form.html', {'form': assessment_form})


@login_required
def assessment_update(request, assessment_id):
    assessment = get_object_or_404(Assessment, id=assessment_id)
    if assessment.author != request.user:
        return HttpResponseForbidden()

    if request.method == "POST":
        assessment_form = AssessmentForm(request.POST, instance=assessment)
        if assessment_form.is_valid():
            assessment = assessment_form.save()
            messages.add_message(request, messages.SUCCESS, "Assessment Updated")
            return HttpResponseRedirect(reverse_lazy('assessment:assessment_update', args=(assessment.id,)))
    else:
        assessment_form = AssessmentForm(instance=assessment)

    signer = Signer()
    signed_assessment_id = quote_plus(signer.sign("%s" % (assessment.id)))

    return render(request, 'assessment/assessment_form.html', {'form': assessment_form,
                                                               'assessment': assessment,
                                                               'signed_assessment_id': signed_assessment_id})


@login_required
def assessment_delete(request, assessment_id):
    assessment = get_object_or_404(Assessment, id=assessment_id)
    if assessment.author != request.user:
        return HttpResponseForbidden()

    if request.method == "POST":
        assessment.delete()
        messages.add_message(request, messages.SUCCESS, "Assessment Deleted")
        return HttpResponseRedirect(reverse_lazy('general:dashboard'))
    else:
        return render(request, 'assessment/assessment_confirm_delete.html')


@login_required
def question_create(request):
    assessment = get_object_or_404(Assessment, id=request.GET['assessment_id'], author=request.user)
    if request.method == "POST":
        question_form = QuestionForm(request.POST, assessment=assessment)
        if question_form.is_valid():
            question_form.instance.assessment = assessment
            question = question_form.save()
            messages.add_message(request, messages.SUCCESS, "Question Created")
            return HttpResponseRedirect(reverse_lazy('assessment:question_update', args=(question.id,)))
    else:
        question_form = QuestionForm(assessment=assessment)

    return render(request, 'assessment/question_form.html', {'form': question_form, 'assessment': assessment})


@login_required
def question_update(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    if question.assessment.author != request.user:
        return HttpResponseForbidden()

    if request.method == "POST":
        question_form = QuestionForm(request.POST, instance=question, assessment=question.assessment)
        if question_form.is_valid():
            question = question_form.save()
            messages.add_message(request, messages.SUCCESS, "Question Updated")
            return HttpResponseRedirect(reverse_lazy('assessment:question_update', args=(question.id,)))
    else:
        question_form = QuestionForm(instance=question, assessment=question.assessment)

    signer = Signer()
    signed_question_id = quote_plus(signer.sign(str(question.id)))
    widget_link = "%s%s?question_id=%s" % (HOST_URL, reverse("assessment:question_info"), signed_question_id)
    return render(request, 'assessment/question_form.html', {'form': question_form,
                                                             'assessment': question.assessment,
                                                             'question': question,
                                                             'widget_link': widget_link})


@login_required
def question_delete(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    if question.assessment.author != request.user:
        return HttpResponseForbidden()

    if request.method == "POST":
        question.delete()
        messages.add_message(request, messages.SUCCESS, "Question Deleted")
        return HttpResponseRedirect(reverse_lazy('general:dashboard'))
    else:
        return render(request, 'assessment/question_confirm_delete.html')


def question_info(request):
    question = __unsign_question(request)
    if not question:
        return __add_cors(HttpResponseForbidden())

    return  __add_cors(JsonResponse({
        'title': question.title,
        'instructions': question.instructions,
        'starting_code': question.starting_code,
        'codemirror_language': CodeMirrorMode[question.assessment.language],
        'submit_url': "%s%s?question_id=%s" % (HOST_URL, reverse('assessment:submit_answer'), request.GET.get('question_id')),
        'check_submission_url': "%s%s" % (HOST_URL, reverse('assessment:check_submission')),
    }))


@login_required
@require_POST
def create_assessment_link(request):
    assessment = get_object_or_404(Assessment, id=request.POST['assessment_id'], author=request.user)
    if not request.POST.get('identifier'):
        return HttpResponseBadRequest()

    signer = Signer()
    value = quote_plus(signer.sign("%s_%s" % (assessment.id, request.POST.get('identifier'))))
    assessment_link = "%s%s?identifier=%s" % (HOST_URL, reverse('assessment:start_assessment'), value)
    return HttpResponse(assessment_link)


#@login_required
@require_POST
def run_code(request):
    code = request.POST.get('code')
    language = request.POST.get('language')
    input = request.POST.get('input', None)

    if not language or language not in Judge0.LanguageToIdDict:
        return HttpResponseBadRequest("%s language not found" % language)

    try:
        token = Judge0().submit_code(code, input, language)
    except RequestException as ex:
        return HttpResponseBadRequest(str(ex))

    return HttpResponse(token)


@csrf_exempt
def submit_answer(request):
    if request.method != "POST":
        return __add_cors(HttpResponse())

    json_data = json.loads(request.body)
    question = __unsign_question(request)
    if not question:
        return __add_cors(HttpResponseForbidden())

    if 'code' not in json_data or not json_data["code"]:
        return __add_cors(HttpResponseBadRequest("Code is empty"))

    code = json_data["code"]
    if question.wrap_output:
        code = CodeMod.wrap_code_in_method(code, question.assessment.language)

    try:
        token = Judge0().submit_code(code + "\n" + question.testing_code, None, question.assessment.language)
    except RequestException as ex:
        return __add_cors(HttpResponseBadRequest(str(ex)))

    AnswerSubmission.objects.create(question=question, code=code, token=token, identifier=__get_identifier(request))
    return __add_cors(HttpResponse(token))


@require_GET
def start_assessment(request):
    try:
        identifier = request.GET['identifier']
        value = Signer().unsign(unquote(identifier))
    except (BadSignature, MultiValueDictKeyError):
        return HttpResponseBadRequest()

    parts = value.split("_", 1)
    assessment_id = int(parts[0])
    user_id = parts[1]

    assessment_attempt = AssessmentAttempt.objects.filter(assessment_id=assessment_id, assignee=user_id).first()
    if not assessment_attempt:
        assessment_attempt = AssessmentAttempt.objects.create(assessment_id=assessment_id, assignee=user_id)

    request.session['assessment_attempt_id'] = assessment_attempt.id
    return redirect(reverse('assessment:take_assessment'))


def start_assessment_self(request):
    try:
        identifier = request.GET['identifier']
        value = Signer().unsign(unquote(identifier))
    except (BadSignature, MultiValueDictKeyError):
        return HttpResponseBadRequest()

    assessment = get_object_or_404(Assessment, id=int(value))

    if request.method == "POST":
        form = StartAssessmentSelfForm(request.POST)
        if form.is_valid():
            user_id = f'{form.data["name"]} - {form.data["email"]}'
            assessment_attempt = AssessmentAttempt.objects.filter(assessment_id=assessment.id, assignee=user_id).first()
            if not assessment_attempt:
                assessment_attempt = AssessmentAttempt.objects.create(assessment_id=assessment.id, assignee=user_id)

            request.session['assessment_attempt_id'] = assessment_attempt.id
            return redirect(reverse('assessment:take_assessment'))
    else:
        form = StartAssessmentSelfForm()

    return render(request, 'assessment/start_assessment_self.html', {'form': form,
                                                                     'assessment': assessment})


@require_GET
def take_assessment(request):
    assessment_attempt = get_object_or_404(AssessmentAttempt, id=request.session['assessment_attempt_id'])
    question = assessment_attempt.get_question_to_answer()

    if question:
        answer = Answer.objects.filter(assessment_attempt=assessment_attempt, question=question).first()
        if not answer:
            Answer.objects.create(question=question, assessment_attempt=assessment_attempt)

    if question is None:
        assessment_attempt.done = True
        assessment_attempt.save()
        del request.session['assessment_attempt_id']

    question_num = assessment_attempt.assessment.get_question_num(question)
    total_questions = assessment_attempt.assessment.questions.count()
    return render(request, 'assessment/take_assessment.html', {'question': question,
                                                               'question_num': question_num,
                                                               'total_questions': total_questions})


@require_POST
def submit_assessment_answer(request):
    code = request.POST.get('code')
    assessment_attempt = get_object_or_404(AssessmentAttempt, id=request.session['assessment_attempt_id'])
    answer = get_object_or_404(Answer, assessment_attempt=assessment_attempt, question=assessment_attempt.get_question_to_answer())

    if answer.question.wrap_output:
        code = CodeMod.wrap_code_in_method(code, answer.question.assessment.language)

    try:
        token = Judge0().submit_code(code + "\n" + answer.question.testing_code, None, answer.question.assessment.language)
    except RequestException as ex:
        return HttpResponseBadRequest(str(ex))

    AnswerSubmission.objects.create(answer=answer, code=code, token=token, identifier=__get_identifier(request))
    return HttpResponse(token)


@require_GET
def check_submission(request):
    token = request.GET.get('token')

    try:
         response = Judge0().check_submission(token)
    except RequestException as ex:
        return __add_cors(HttpResponseBadRequest(str(ex)))

    status = response['status']['id']
    if status == 1 or status == 2:
        return __add_cors(JsonResponse({"status": "processing"}))

    status_description = response['status']['description']
    stdout = response['stdout']
    stderr = response['stderr']
    message = response['message']
    compile_output = response['compile_output']
    passed = stderr is None and compile_output is None and status == 3

    summary = ""
    if status_description != "Accepted":
        summary += "Submission status:   %s\n" % status_description
    if stdout:
        summary += "Stdout:   %s\n" % stdout.rstrip()
    if stderr:
        summary += "Stderr:   %s\n" % stderr.rstrip()
    if message:
        summary += "Message:   %s\n" % message
    if compile_output:
        summary += "Compile Output:   %s\n" % compile_output

    summary += "\nPassed:   %s" % passed

    submission = AnswerSubmission.objects.filter(token=token).first()
    if submission:
        submission.response = "%s..." % summary[0:1000] if len(summary) > 1000 else summary
        submission.passed = passed
        submission.save()

        if passed and submission.answer:
            submission.answer.passed = passed
            submission.answer.save()

    return __add_cors(JsonResponse({
        "status": "done",
        "text": summary,
        "passed": passed,
    }))


@require_GET
def question_done(request):
    assessment_attempt = get_object_or_404(AssessmentAttempt, id=request.session['assessment_attempt_id'])
    question = assessment_attempt.get_question_to_answer()
    answer = Answer.objects.get(assessment_attempt=assessment_attempt, question=question)
    answer.done = True
    answer.save()
    return redirect(reverse('assessment:take_assessment'))


@login_required
def assessment_attempts(request):
    assessment = get_object_or_404(Assessment, id=request.GET.get("assessment_id"))
    if assessment.author != request.user:
        return HttpResponseForbidden()

    return render(request, 'assessment/assessment_attempts.html', {'assessment': assessment})


@login_required
def assessment_attempt(request, assessment_attempt_id):
    assessment_attempt = get_object_or_404(AssessmentAttempt, id=assessment_attempt_id)
    if assessment_attempt.assessment.author != request.user:
        return HttpResponseForbidden()

    return render(request, 'assessment/assessment_attempt.html', {'assessment_attempt': assessment_attempt})


@login_required
def question_submissions(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    if question.assessment.author != request.user:
        return HttpResponseForbidden()

    return render(request, 'assessment/question_submissions.html', {'question': question})


def __unsign_question(request):
    try:
        signed_question_id = request.GET.get("question_id")
        question_id = Signer().unsign(unquote(signed_question_id))
        question = Question.objects.filter(id=question_id).first()
    except BadSignature:
        return None

    return question


def __get_identifier(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    user_agent = request.META['HTTP_USER_AGENT']
    if len(user_agent) > 200:
        user_agent = user_agent[:200] + ".."
    return "%s_%s" % (ip, user_agent)


def __add_cors(response):
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "GET, " \
                                               ", OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "X-Requested-With, Content-Type"
    return response