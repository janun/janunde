# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-30 21:05
from __future__ import unicode_literals

from django.db import migrations, models
from django.utils import timezone

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0060_basepage_hyphenated_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='attributedimage',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, default=timezone.now),
        ),
    ]