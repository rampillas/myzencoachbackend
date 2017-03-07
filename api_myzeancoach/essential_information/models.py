# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

class Videos(models.Model):
    """
    Videos for users
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.TextField(blank=True,null=False, default=None)
    url = models.TextField(blank=True, null=False, default=None)
    new_attr = models.IntegerField(default=0)
    is_watched = models.BooleanField(default=False)
    date = models.DateTimeField(_(u'date'), auto_now_add=True)
    photo_url = models.TextField(blank=True, null=True, default=None)

    class Meta:
        verbose_name = "Video"
        verbose_name_plural = "Videos"

class Survey(models.Model):
    """
    Surveys for users
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey(Videos, on_delete=models.CASCADE,related_name='survey')
    description = models.TextField(blank=True, null=False, default=None)
    score = models.IntegerField(default=0)
    is_completed = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Survey"
        verbose_name_plural = "Surveys"


class Question(models.Model):
    """
    Questions for Survey
    """
    survey = models.ForeignKey(Survey,on_delete=models.CASCADE,related_name='questions')
    description = models.TextField(blank=True, null=False, default=None)
    is_completed = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Question"
        verbose_name_plural = "Questions"


class Answer(models.Model):
    """
    Answers for Questions
    """
    question = models.ForeignKey(Question, on_delete=models.CASCADE,related_name='answers')
    description = models.TextField(blank=True, null=False, default=None)
    is_right = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Answer"
        verbose_name_plural = "Answers"