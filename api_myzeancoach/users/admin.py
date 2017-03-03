from django.contrib import admin
from models import Profile, Emoticon

class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'nick', 'birthday', 'gender',
        'country', 'city')

    search_fields = ['user', 'nick']

class EmoticonAdmin(admin.ModelAdmin):
    list_display = ('user','name', 'is_positive', 'date')

    search_fields = ['user', 'date']

admin.site.register(Profile, ProfileAdmin)
admin.site.register(Emoticon, EmoticonAdmin)