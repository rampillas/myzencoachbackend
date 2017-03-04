from django.contrib import admin
from models import Videos, Survey, Question, Answer

class VideosAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'url', 'new_attr', 'is_watched', 'date')

    search_fields = ['user', 'name']

class SurveyAdmin(admin.ModelAdmin):
    list_display = ('user', 'description', 'score', 'is_completed')

    search_fields = ['user', 'description']

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('survey','description')

    search_fields = ['description']

class AnswerAdmin(admin.ModelAdmin):
    list_display = ('question','description')

    search_fields = ['description']

admin.site.register(Videos, VideosAdmin)
admin.site.register(Survey, SurveyAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)