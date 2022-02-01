from django.urls import path, re_path

from assessment import views

urlpatterns = [
    path('assessment-create', views.assessment_create, name='assessment_create'),
    re_path('assessment-update/(?P<assessment_id>\d+)', views.assessment_update, name='assessment_update'),
    re_path('assessment-delete/(?P<assessment_id>\d+)', views.assessment_delete, name='assessment_delete'),
    path('question-create', views.question_create, name='question_create'),
    re_path('question-update/(?P<question_id>\d+)', views.question_update, name='question_update'),
    re_path('question-delete/(?P<question_id>\d+)', views.question_delete, name='question_delete'),
    path('create-assessment-link', views.create_assessment_link, name='create_assessment_link'),
    path('start-assessment', views.start_assessment, name='start_assessment'),
    re_path('start-assessment-self', views.start_assessment_self, name='start_assessment_self'),
    path('take-assessment', views.take_assessment, name='take_assessment'),
    path('run-code', views.run_code, name='run_code'),
    path('submit-answer', views.submit_answer, name='submit_answer'),
    path('submit-assessment-answer', views.submit_assessment_answer, name='submit_assessment_answer'),
    path('check-submission', views.check_submission, name='check_submission'),
    path('question-done', views.question_done, name='question_done'),
    re_path('assessment-attempt/(?P<assessment_attempt_id>\d+)', views.assessment_attempt, name='assessment_attempt'),
    path('assessment-attempts', views.assessment_attempts, name='assessment_attempts'),
    path('question-info', views.question_info, name='question_info'),
    re_path('question-submissions/(?P<question_id>\d+)', views.question_submissions, name='question_submissions'),
]
