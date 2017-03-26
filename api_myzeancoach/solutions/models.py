# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

class Dilemma(models.Model):
    """
    Dilemmas for social actions
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(_(u'date'), auto_now_add=True)
    title = models.TextField(blank=True, null=False, default=None)
    description = models.TextField(blank=True, null=False, default=None)
    nick_user = models.TextField(blank=True, null=False, default=None)
    type = models.TextField(blank=True, null=False, default=None)
    state = models.TextField(blank=True, null=False, default=None)

    class Meta:
        verbose_name = "Dilemma"
        verbose_name_plural = "Dilemmas"

class CommentDilemma(models.Model):
    """
    Comments for Dilemmas for social actions
    """
    dilemma = models.ForeignKey(Dilemma, on_delete=models.CASCADE, related_name='dilemmas')
    nick_user = models.TextField(blank=True, null=False, default=None)
    date = models.DateTimeField(_(u'date'), auto_now_add=True)
    description = models.TextField(blank=True, null=False, default=None)
    like = models.BooleanField(default=False)
    feedback = models.TextField(blank=True, null=False, default=None)
    date_feedback = models.DateTimeField(_(u'date'), auto_now_add=True)

    class Meta:
        verbose_name = "Comment Dilemma"
        verbose_name_plural = "Comments Dilemmas"


class CommentDilemmaCoach(models.Model):
    """
    Coach indicate the changes for dilemma
    """
    dilemma_coach = models.ForeignKey(Dilemma, on_delete=models.CASCADE, related_name='dilemmas_coach')
    date = models.DateTimeField(_(u'date'), auto_now_add=True)
    description = models.TextField(blank=True, null=False, default=None)

    class Meta:
        verbose_name = "Comment Dilemma Coach"
        verbose_name_plural = "Comments Dilemmas Coach"

class ProCommentDilemma(models.Model):
    """
    Pros for Dilemmas for social actions
    """
    pro_dilemma = models.ForeignKey(CommentDilemma, on_delete=models.CASCADE, related_name='pro_dilemmas')
    description = models.TextField(blank=True, null=False, default=None)

    class Meta:
        verbose_name = "Pro Dilemma"
        verbose_name_plural = "Pros Dilemmas"

class ConCommentDilemma(models.Model):
    """
    Cons for Dilemmas for social actions
    """
    con_dilemma = models.ForeignKey(CommentDilemma, on_delete=models.CASCADE, related_name='con_dilemmas')
    description = models.TextField(blank=True, null=False, default=None)

    class Meta:
        verbose_name = "Con Dilemma"
        verbose_name_plural = "Cons Dilemmas"

