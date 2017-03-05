# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('essential_information', '0002_auto_20170304_2129'),
    ]

    operations = [
        migrations.AddField(
            model_name='videos',
            name='photo_url',
            field=models.TextField(default=None, null=True, blank=True),
        ),
    ]
