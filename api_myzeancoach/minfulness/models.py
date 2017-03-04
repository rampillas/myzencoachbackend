# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

class WellnessPlan(models.Model):
    """
    Plans Minfulness for users
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(_(u'date'), auto_now_add=True)
    description = models.TextField(blank=True, null=False, default=None)

    class Meta:
        verbose_name = "WellnessPlan"
        verbose_name_plural = "WellnessPlans"

class Exercise(models.Model):
    """
    Exercises for User's Plans
    """
    plans = models.ForeignKey(WellnessPlan, on_delete=models.CASCADE, related_name='exercises')
    week = models.IntegerField(default=0)
    description = models.TextField(blank=True, null=False, default=None)
    audio_url = models.TextField(blank=True, null=False, default=None)
    instructions = models.TextField(blank=True, null=False, default=None)
    feedback = models.TextField(blank=True, null=False, default=None)

    class Meta:
        verbose_name = "Exercise"
        verbose_name_plural = "Exercises"


class QuestionExercise(models.Model):
    """
    Questions for Exercises
    """
    exercises = models.ForeignKey(Exercise, on_delete=models.CASCADE, related_name='question_exercises')
    question = models.TextField(blank=True, null=False, default=None)
    answer = models.BooleanField(default=False)
    is_answered = models.BooleanField(default=False)

    class Meta:
        verbose_name = "QuestionExercise"
        verbose_name_plural = "QuestionExercises"