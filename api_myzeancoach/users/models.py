# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nick = models.CharField(max_length=100,blank=True)
    birthday = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10,blank=True)
    country = models.CharField(max_length=100,blank=True)
    city = models.CharField(max_length=100,blank=True)
    description = models.CharField(max_length=100,blank=True)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

def update_profile(username, data):
    user = User.objects.get(username=username)
    if user:
        user.profile.nick = data.get("nick",False)
        user.profile.birthday = data.get("birthday",False)
        user.profile.gender = data.get("gender",False)
        user.profile.country = data.get("country",False)
        user.profile.city = data.get("city",False)
        user.profile.description = data.get("description",False)
        user.save()

    return user


class Emoticon(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100,blank=True)
    is_positive = models.BooleanField(blank=True)
    date = models.DateTimeField(_(u'date'), auto_now_add=True)