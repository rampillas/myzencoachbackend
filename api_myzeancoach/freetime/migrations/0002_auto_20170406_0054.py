# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('freetime', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserEventLike',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_liked', models.BooleanField(default=False)),
                ('event', models.ForeignKey(related_name='events_likes', to='freetime.Events')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterModelOptions(
            name='interests',
            options={'verbose_name': 'Interests', 'verbose_name_plural': 'Interests'},
        ),
    ]
