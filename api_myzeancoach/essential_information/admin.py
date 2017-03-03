from django.contrib import admin
from models import Videos

class VideosAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'url', 'new_attr', 'is_watched', 'date')

    search_fields = ['user', 'name']

admin.site.register(Videos, VideosAdmin)