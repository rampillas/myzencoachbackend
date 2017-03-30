# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CommentEvent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='date')),
                ('description', models.TextField(default=None, blank=True)),
            ],
            options={
                'verbose_name': 'Comment Event',
                'verbose_name_plural': 'Comments Events',
            },
        ),
        migrations.CreateModel(
            name='Events',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='date')),
                ('title', models.TextField(default=None, blank=True)),
                ('description', models.TextField(default=None, blank=True)),
                ('likes', models.IntegerField(default=0)),
                ('category', models.TextField(default=None, blank=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Events',
                'verbose_name_plural': 'Events',
            },
        ),
        migrations.CreateModel(
            name='Interests',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.TextField(default=None, blank=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='commentevent',
            name='event',
            field=models.ForeignKey(related_name='events', to='freetime.Events'),
        ),
        migrations.AddField(
            model_name='commentevent',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
