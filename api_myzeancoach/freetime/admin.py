from django.contrib import admin
from models import Events, CommentEvent, Interests, UserEventLike

class EventsAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'title', 'description', 'likes', 'category')

    search_fields = ['title','description']

class CommentEventAdmin(admin.ModelAdmin):
    list_display = ('user', 'event', 'date', 'description')

    search_fields = ['description']

class UserEventLikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'event', 'is_liked')

    search_fields = ['user']

class InterestsAdmin(admin.ModelAdmin):
    list_display = ('user', 'name')

    search_fields = ['name']

admin.site.register(Events, EventsAdmin)
admin.site.register(CommentEvent, CommentEventAdmin)
admin.site.register(UserEventLike, UserEventLikeAdmin)
admin.site.register(Interests, InterestsAdmin)