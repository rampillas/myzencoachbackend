from django.contrib import admin
from models import WellnessPlan, Exercise, QuestionExercise

class WellnessPlanAdmin(admin.ModelAdmin):
    list_display = ('user', 'date','description', 'is_finished')

    search_fields = ['user','description']

class ExerciseAdmin(admin.ModelAdmin):
    list_display = ('plans', 'week', 'description', 'audio_url', 'instructions', 'feedback','appreciation')

    search_fields = ['plans', 'description']

class QuestionExerciseAdmin(admin.ModelAdmin):
    list_display = ('exercises', 'question', 'answer', 'is_answered', 'response')

    search_fields = ['exercises', 'question']

admin.site.register(WellnessPlan, WellnessPlanAdmin)
admin.site.register(Exercise, ExerciseAdmin)
admin.site.register(QuestionExercise, QuestionExerciseAdmin)