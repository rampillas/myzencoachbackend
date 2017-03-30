from django.contrib import admin
from models import Events, CommentEvent, Interests

class EventsAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'title', 'description', 'likes', 'category')

    search_fields = ['title','description']

class CommentEventAdmin(admin.ModelAdmin):
    list_display = ('user', 'event', 'date', 'description')

    search_fields = ['description']

class InterestsAdmin(admin.ModelAdmin):
    list_display = ('user', 'name')

    search_fields = ['name']

admin.site.register(Events, EventsAdmin)
admin.site.register(CommentEvent, CommentEventAdmin)
admin.site.register(Interests, InterestsAdmin)