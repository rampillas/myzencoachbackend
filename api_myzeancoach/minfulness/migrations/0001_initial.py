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
            name='Exercise',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('week', models.IntegerField(default=0)),
                ('description', models.TextField(default=None, blank=True)),
                ('audio_url', models.TextField(default=None, blank=True)),
                ('instructions', models.TextField(default=None, blank=True)),
                ('feedback', models.TextField(default=None, blank=True)),
            ],
            options={
                'verbose_name': 'Exercise',
                'verbose_name_plural': 'Exercises',
            },
        ),
        migrations.CreateModel(
            name='QuestionExercise',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('question', models.TextField(default=None, blank=True)),
                ('answer', models.BooleanField(default=False)),
                ('is_answered', models.BooleanField(default=False)),
                ('exercises', models.ForeignKey(related_name='question_exercises', to='minfulness.Exercise')),
            ],
            options={
                'verbose_name': 'QuestionExercise',
                'verbose_name_plural': 'QuestionExercises',
            },
        ),
        migrations.CreateModel(
            name='WellnessPlan',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='date')),
                ('description', models.TextField(default=None, blank=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'WellnessPlan',
                'verbose_name_plural': 'WellnessPlans',
            },
        ),
        migrations.AddField(
            model_name='exercise',
            name='plans',
            field=models.ForeignKey(related_name='exercises', to='minfulness.WellnessPlan'),
        ),
    ]
