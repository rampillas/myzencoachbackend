# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

"""FIRST PART"""
class Reminders(models.Model):
    """
    Reminders for Users
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.TextField(blank=True, null=False, default=None)
    subtitle = models.TextField(blank=True, null=False, default=None)
    description = models.TextField(blank=True, null=False, default=None)
    is_personal = models.BooleanField(default=False)
    date = models.DateTimeField(_(u'date'), auto_now_add=True)
    time = models.TextField(blank=True, null=False, default=None)
    is_finished = models.BooleanField(default=False)
    is_observations_enabled = models.BooleanField(default=False)
    observations = models.TextField(blank=True, null=False, default=None)
    frequency = models.TextField(blank=True, null=False, default=None)

    class Meta:
        verbose_name = "Reminder"
        verbose_name_plural = "Reminders"


class Rewards(models.Model):
    """
    Rewards for Reminders
    """
    reminder = models.ForeignKey(Reminders, on_delete=models.CASCADE, related_name='reminders')
    points = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Reward"
        verbose_name_plural = "Rewards"


"""SECOND PART"""
class StressDetectionQuestions(models.Model):
    """
    Stress Questions
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=False, default=None)
    possible_answers = models.IntegerField(default=0)
    is_personal_question = models.BooleanField(default=False)
    active = models.IntegerField(default=0)
    user_answer = models.TextField(blank=True, null=False, default=None)

    class Meta:
        verbose_name = "Stress Questions"
        verbose_name_plural = "Stress Questions"


class StressDetectionAnswers(models.Model):
    """
    Stress Answers
    """
    question = models.ForeignKey(StressDetectionQuestions, on_delete=models.CASCADE, related_name='questions')
    description = models.TextField(blank=True, null=False, default=None)
    color = models.TextField(blank=True, null=False, default=None)
    popup_message = models.TextField(blank=True, null=False, default=None)

    class Meta:
        verbose_name = "Stress Answers"
        verbose_name_plural = "Stress Answers"


class CoachFollowUp(models.Model):
    """
    Coach Followup
    """
    description = models.TextField(blank=True, null=False, default=None)
    active = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Coach Follow-up"
        verbose_name_plural = "Coach Follow-ups"

