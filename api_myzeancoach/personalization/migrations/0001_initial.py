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
            name='CoachFollowUp',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.TextField(default=None, blank=True)),
                ('active', models.IntegerField(default=0)),
            ],
            options={
                'verbose_name': 'Coach Follow-up',
                'verbose_name_plural': 'Coach Follow-ups',
            },
        ),
        migrations.CreateModel(
            name='Reminders',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.TextField(default=None, blank=True)),
                ('subtitle', models.TextField(default=None, blank=True)),
                ('description', models.TextField(default=None, blank=True)),
                ('is_personal', models.BooleanField(default=False)),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='date')),
                ('time', models.TextField(default=None, blank=True)),
                ('is_finished', models.BooleanField(default=False)),
                ('is_observations_enabled', models.BooleanField(default=False)),
                ('observations', models.TextField(default=None, blank=True)),
                ('frequency', models.TextField(default=None, blank=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Reminder',
                'verbose_name_plural': 'Reminders',
            },
        ),
        migrations.CreateModel(
            name='Rewards',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('points', models.IntegerField(default=0)),
                ('reminder', models.ForeignKey(related_name='reminders', to='personalization.Reminders')),
            ],
            options={
                'verbose_name': 'Reward',
                'verbose_name_plural': 'Rewards',
            },
        ),
        migrations.CreateModel(
            name='StressDetectionAnswers',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.TextField(default=None, blank=True)),
                ('color', models.TextField(default=None, blank=True)),
                ('popup_message', models.TextField(default=None, blank=True)),
            ],
            options={
                'verbose_name': 'Stress Answers',
                'verbose_name_plural': 'Stress Answers',
            },
        ),
        migrations.CreateModel(
            name='StressDetectionQuestions',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.TextField(default=None, blank=True)),
                ('possible_answers', models.IntegerField(default=0)),
                ('is_personal_question', models.BooleanField(default=False)),
                ('active', models.IntegerField(default=0)),
                ('user_answer', models.TextField(default=None, blank=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Stress Questions',
                'verbose_name_plural': 'Stress Questions',
            },
        ),
        migrations.AddField(
            model_name='stressdetectionanswers',
            name='question',
            field=models.ForeignKey(related_name='questions', to='personalization.StressDetectionQuestions'),
        ),
    ]
