# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('minfulness', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='exercise',
            name='appreciation',
            field=models.TextField(default=None, blank=True),
        ),
        migrations.AddField(
            model_name='questionexercise',
            name='response',
            field=models.TextField(default=None, blank=True),
        ),
        migrations.AddField(
            model_name='wellnessplan',
            name='is_finished',
            field=models.BooleanField(default=False),
        ),
    ]
