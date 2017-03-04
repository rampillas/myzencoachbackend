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

    class Meta:
        verbose_name = "Video"
        verbose_name_plural = "Videos"

