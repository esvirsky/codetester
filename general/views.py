from urllib.parse import quote_plus

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.signing import Signer
from django.shortcuts import render
from django.urls import reverse

from assessment.models import Assessment, Question


def index(request):
    return render(request, 'general/index.html')


@login_required
def dashboard(request):
    assessments = Assessment.objects.filter(author_id=request.user.id).prefetch_related('questions', 'attempts').all();
    return render(request, 'general/dashboard.html', {'assessments': assessments})


def contact(request):
    return render(request, 'general/contact.html')


def fizzbuzz_python(request):
    question = Question.objects.filter(title='FizzBuzz').order_by('created_at').first();
    signer = Signer()
    signed_question_id = quote_plus(signer.sign(str(question.id)))
    widget_link = "%s%s?question_id=%s" % (settings.HOST_URL, reverse("assessment:question_info"), signed_question_id)
    return render(request, 'general/fizzbuzz_python.html', {"widget_link": widget_link})


def coding_assessment_tool(request):
    return render(request, 'general/coding_assessment_tool.html')


def widget(request):
    return render(request, 'general/widget.html')


def python_tutorial1(request):
    signer = Signer()

    q1_id = quote_plus(signer.sign(str(Question.objects.filter(title='Hello World', assessment__name='Python Tutorial').order_by('created_at').first().id)))
    q1_widget_link = "%s%s?question_id=%s" % (settings.HOST_URL, reverse("assessment:question_info"), q1_id)

    q2_id = quote_plus(signer.sign(str(Question.objects.filter(title='Variables', assessment__name='Python Tutorial').order_by('created_at').first().id)))
    q2_widget_link = "%s%s?question_id=%s" % (settings.HOST_URL, reverse("assessment:question_info"), q2_id)

    q3_id = quote_plus(signer.sign(str(
    Question.objects.filter(title='Send Invites', assessment__name='Python Tutorial').order_by('created_at').first().id)))
    q3_widget_link = "%s%s?question_id=%s" % (settings.HOST_URL, reverse("assessment:question_info"), q3_id)

    q4_id = quote_plus(signer.sign(str(Question.objects.filter(title='Invite John', assessment__name='Python Tutorial').order_by('created_at').first().id)))
    q4_widget_link = "%s%s?question_id=%s" % (settings.HOST_URL, reverse("assessment:question_info"), q4_id)

    q5_id = quote_plus(signer.sign(str(Question.objects.filter(title='Tutorial1 Test', assessment__name='Python Tutorial').order_by('created_at').first().id)))
    q5_widget_link = "%s%s?question_id=%s" % (settings.HOST_URL, reverse("assessment:question_info"), q5_id)

    return render(request, 'general/python_tutorial1.html', {'q1_widget_link': q1_widget_link,
                                                             'q2_widget_link': q2_widget_link,
                                                             'q3_widget_link': q3_widget_link,
                                                             'q4_widget_link': q4_widget_link,
                                                             'q5_widget_link': q5_widget_link})