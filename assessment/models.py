from datetime import timedelta

from django.conf import settings
from django.db import models
from django.db.models import Prefetch, Q

from general.models import BaseCreatedModifiedModel, Language

LANGUAGES = (
    (Language.JAVA.value, 'Java'),
    (Language.JAVASCRIPT.value, 'Javascript'),
    (Language.PYTHON.value, 'Python'),
    (Language.RUBY.value, 'Ruby'),
)

class Assessment(BaseCreatedModifiedModel):

    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='assessments', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    language = models.CharField(max_length=255, choices=LANGUAGES)

    def get_question_num(self, question):
        questions = self.questions.order_by('created_at')
        for idx, q in enumerate(questions):
            if q == question:
                return idx

        return None

    def __str__(self):
        return self.name

    class Meta:
        managed = True
        db_table = 'assessments'
        unique_together = ('author', 'name')


class Question(BaseCreatedModifiedModel):
    assessment = models.ForeignKey('Assessment', related_name='questions', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    instructions = models.TextField()
    starting_code = models.TextField()
    testing_code = models.TextField()
    solution_code = models.TextField()
    wrap_output = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        managed = True
        db_table = 'questions'


class AssessmentAttempt(BaseCreatedModifiedModel):
    assessment = models.ForeignKey('Assessment', related_name='attempts', on_delete=models.CASCADE)
    assignee = models.CharField(max_length=255)
    done = models.BooleanField(default=False)

    def get_time_spent(self):
        last_submission = AnswerSubmission.objects.filter(answer__assessment_attempt=self).order_by('created_at').last()
        if not last_submission:
            return timedelta(seconds=0)

        return last_submission.created_at - self.created_at

    def get_questions_passed(self):
        return self.answers.filter(passed=True).count()


    def get_question_to_answer(self):
        # Grab the current question that needs to be answered
        return self.assessment.questions\
            .exclude(answers__in=self.answers.filter(done=True))\
            .order_by('created_at').first()


    class Meta:
        managed = True
        db_table = 'assessment_attempts'


class Answer(BaseCreatedModifiedModel):
    assessment_attempt = models.ForeignKey('AssessmentAttempt', related_name='answers', on_delete=models.CASCADE)
    question = models.ForeignKey('Question', related_name='answers', on_delete=models.CASCADE)
    passed = models.BooleanField(default=False)
    done = models.BooleanField(default=False)

    def __str__(self):
        return "Answer to %s" % self.question

    class Meta:
        managed = True
        ordering = ['created_at']
        db_table = 'answers'


class AnswerSubmission(BaseCreatedModifiedModel):
    # An answer submission that isn't tied to an answer is just a submission to question
    answer = models.ForeignKey('Answer', related_name='submissions', on_delete=models.CASCADE, blank=True, null=True)
    question = models.ForeignKey('Question', related_name='question_submissions', on_delete=models.CASCADE, blank=True, null=True)
    identifier = models.CharField(max_length=255)
    passed = models.BooleanField(default=False)
    code = models.TextField(max_length=2000)
    response = models.TextField(max_length=2000)
    token = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = True
        ordering = ['created_at']
        db_table = 'answer_submissions'
