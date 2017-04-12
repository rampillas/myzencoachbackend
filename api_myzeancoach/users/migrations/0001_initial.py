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
            name='Emoticon',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, blank=True)),
                ('is_positive', models.BooleanField()),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='date')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('birthday', models.DateField(null=True, blank=True)),
                ('gender', models.CharField(max_length=10, blank=True)),
                ('country', models.CharField(max_length=100, blank=True)),
                ('city', models.CharField(max_length=100, blank=True)),
                ('description', models.CharField(max_length=100, blank=True)),
                ('rural_zone', models.CharField(max_length=100, blank=True)),
                ('change_country', models.BooleanField(default=False)),
                ('level_studies', models.CharField(max_length=100, blank=True)),
                ('notification_token', models.TextField(blank=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
