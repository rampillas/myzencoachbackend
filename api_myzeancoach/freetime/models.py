# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

class Events(models.Model):
    """
    Public Events for users
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(_(u'date'), auto_now_add=True)
    title = models.TextField(blank=True, null=False, default=None)
    description = models.TextField(blank=True, null=False, default=None)
    likes = models.IntegerField(default=0)
    category = models.TextField(blank=True, null=False, default=None)

    class Meta:
        verbose_name = "Events"
        verbose_name_plural = "Events"

class CommentEvent(models.Model):
    """
    Comments for Events
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Events, on_delete=models.CASCADE, related_name='events')
    date = models.DateTimeField(_(u'date'), auto_now_add=True)
    description = models.TextField(blank=True, null=False, default=None)

    class Meta:
        verbose_name = "Comment Event"
        verbose_name_plural = "Comments Events"

class Interests(models.Model):
    """
    Interests for Users
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.TextField(blank=True, null=False, default=None)

    class Meta:
        verbose_name = "Interests"
        verbose_name_plural = "Interests"