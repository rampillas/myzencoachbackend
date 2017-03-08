from django.contrib import admin
from models import Profile, Emoticon

class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'birthday', 'gender',
        'country', 'city', 'rural_zone','change_country','level_studies')

    search_fields = ['user', 'nick']

class EmoticonAdmin(admin.ModelAdmin):
    list_display = ('user','name', 'is_positive', 'date')

    search_fields = ['user', 'date']

admin.site.register(Profile, ProfileAdmin)
admin.site.register(Emoticon, EmoticonAdmin)