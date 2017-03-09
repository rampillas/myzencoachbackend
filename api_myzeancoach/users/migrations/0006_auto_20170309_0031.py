# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_remove_profile_nick'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='change_country',
            field=models.BooleanField(default=False),
        ),
    ]
