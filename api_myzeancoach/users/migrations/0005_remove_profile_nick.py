# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20170306_2312'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='nick',
        ),
    ]
