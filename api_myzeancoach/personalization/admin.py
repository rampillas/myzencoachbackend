from django.contrib import admin
from models import Reminders,Rewards,StressDetectionQuestions,StressDetectionAnswers,CoachFollowUp

class RemindersAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'subtitle', 'description', 'is_personal', 'date', 'time','is_finished',
                    'is_observations_enabled', 'observations', 'frequency')

    search_fields = ['description']

class RewardsAdmin(admin.ModelAdmin):
    list_display = ('reminder', 'points')

    search_fields = ['reminder']

class StressDetectionQuestionsAdmin(admin.ModelAdmin):
    list_display = ('user', 'description', 'possible_answers', 'is_personal_question', 'active', 'user_answer')

    search_fields = ['description']

class StressDetectionAnswersAdmin(admin.ModelAdmin):
    list_display = ('question', 'description', 'color', 'popup_message')

    search_fields = ['description']

class CoachFollowUpAdmin(admin.ModelAdmin):
    list_display = ('description', 'active')

    search_fields = ['description']

admin.site.register(Reminders, RemindersAdmin)
admin.site.register(Rewards, RewardsAdmin)
admin.site.register(StressDetectionQuestions, StressDetectionQuestionsAdmin)
admin.site.register(StressDetectionAnswers, StressDetectionAnswersAdmin)
admin.site.register(CoachFollowUp, CoachFollowUpAdmin)