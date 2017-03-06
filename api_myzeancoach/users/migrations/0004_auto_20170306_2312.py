# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_emoticon'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='change_country',
            field=models.CharField(max_length=10, blank=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='level_studies',
            field=models.CharField(max_length=100, blank=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='rural_zone',
            field=models.CharField(max_length=100, blank=True),
        ),
    ]
