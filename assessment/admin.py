from django.contrib import admin

from assessment.models import Assessment, Question, Answer, AnswerSubmission, AssessmentAttempt


class AnswerSubmissionAdmin(admin.ModelAdmin):
    list_display = ['answer', 'question', 'token', 'created_at', 'modified_at']
    ordering = ['-id']


admin.site.register(Assessment)
admin.site.register(Question)
admin.site.register(AssessmentAttempt)
admin.site.register(Answer)
admin.site.register(AnswerSubmission, AnswerSubmissionAdmin)