from django.contrib import admin
from models import Dilemma, CommentDilemma,CommentDilemmaCoach, ProCommentDilemma, ConCommentDilemma

class DilemmaAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'title', 'description', 'nick_user', 'type', 'state')

    search_fields = ['title','description']

class CommentDilemmaAdmin(admin.ModelAdmin):
    list_display = ('dilemma', 'nick_user', 'date', 'description', 'like', 'feedback', 'date_feedback')

    search_fields = ['description']

class CommentDilemmaCoachAdmin(admin.ModelAdmin):
    list_display = ('dilemma_coach', 'date', 'description')

    search_fields = ['description']

class ProCommentDilemmaAdmin(admin.ModelAdmin):
    list_display = ('pro_dilemma', 'description')

    search_fields = ['description']

class ConCommentDilemmaAdmin(admin.ModelAdmin):
    list_display = ('con_dilemma', 'description')

    search_fields = ['description']

admin.site.register(Dilemma, DilemmaAdmin)
admin.site.register(CommentDilemma, CommentDilemmaAdmin)
admin.site.register(CommentDilemmaCoach, CommentDilemmaCoachAdmin)
admin.site.register(ProCommentDilemma, ProCommentDilemmaAdmin)
admin.site.register(ConCommentDilemma, ConCommentDilemmaAdmin)