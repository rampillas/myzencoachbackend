# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from models import Profile,Emoticon
from rest_framework import serializers,validators
from django.core.validators import RegexValidator, EmailValidator
from django.utils.translation import ugettext_lazy as _

USERNAME_HINT = _('Enter a valid username, between 4 and 20 characters. '
                  'This value may contain only letters, numbers '
                  'and /-/_ characters.')

class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Profile
        fields = (
            'birthday', 'gender', 'country', 'city', 'description', 'rural_zone','change_country',
            'level_studies', 'notification_token'
        )

class UserSerializer(serializers.HyperlinkedModelSerializer):
    url_field_name = 'username'

    url = serializers.HyperlinkedIdentityField(view_name='user-detail', lookup_field='username')
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = (
            'url', 'username', 'email', 'first_name', 'last_name', 'is_active', 'last_login','profile'
        )

        extra_kwargs = {
            'username': {
                'help_text': USERNAME_HINT,
                'validators': [
                    RegexValidator(r'^[a-z0-9._-]{4,100}$', USERNAME_HINT, code='invalid_username'),
                    validators.UniqueValidator(User.objects.all())
                ],
            },
            'email': {
                'validators': [
                    EmailValidator(code='invalid_email'),
                    validators.UniqueValidator(User.objects.all())
                ],
            },
        }

class EmoticonSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Emoticon
        fields = (
            'name', 'is_positive', 'date'
        )