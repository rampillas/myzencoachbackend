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
            name='CommentDilemma',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nick_user', models.TextField(default=None, blank=True)),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='date')),
                ('description', models.TextField(default=None, blank=True)),
                ('like', models.BooleanField(default=False)),
                ('feedback', models.TextField(default=None, blank=True)),
                ('date_feedback', models.DateTimeField(auto_now_add=True, verbose_name='date')),
            ],
            options={
                'verbose_name': 'Comment Dilemma',
                'verbose_name_plural': 'Comments Dilemmas',
            },
        ),
        migrations.CreateModel(
            name='CommentDilemmaCoach',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='date')),
                ('description', models.TextField(default=None, blank=True)),
            ],
            options={
                'verbose_name': 'Comment Dilemma Coach',
                'verbose_name_plural': 'Comments Dilemmas Coach',
            },
        ),
        migrations.CreateModel(
            name='ConCommentDilemma',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.TextField(default=None, blank=True)),
                ('con_dilemma', models.ForeignKey(related_name='con_dilemmas', to='solutions.CommentDilemma')),
            ],
            options={
                'verbose_name': 'Con Dilemma',
                'verbose_name_plural': 'Cons Dilemmas',
            },
        ),
        migrations.CreateModel(
            name='Dilemma',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='date')),
                ('title', models.TextField(default=None, blank=True)),
                ('description', models.TextField(default=None, blank=True)),
                ('nick_user', models.TextField(default=None, blank=True)),
                ('type', models.TextField(default=None, blank=True)),
                ('state', models.TextField(default=None, blank=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Dilemma',
                'verbose_name_plural': 'Dilemmas',
            },
        ),
        migrations.CreateModel(
            name='ProCommentDilemma',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.TextField(default=None, blank=True)),
                ('pro_dilemma', models.ForeignKey(related_name='pro_dilemmas', to='solutions.CommentDilemma')),
            ],
            options={
                'verbose_name': 'Pro Dilemma',
                'verbose_name_plural': 'Pros Dilemmas',
            },
        ),
        migrations.AddField(
            model_name='commentdilemmacoach',
            name='dilemma_coach',
            field=models.ForeignKey(related_name='dilemmas_coach', to='solutions.Dilemma'),
        ),
        migrations.AddField(
            model_name='commentdilemma',
            name='dilemma',
            field=models.ForeignKey(related_name='dilemmas', to='solutions.Dilemma'),
        ),
    ]
