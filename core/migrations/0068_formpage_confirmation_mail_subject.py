# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-21 15:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0067_auto_20170721_1723'),
    ]

    operations = [
        migrations.AddField(
            model_name='formpage',
            name='confirmation_mail_subject',
            field=models.CharField(blank=True, max_length=255, verbose_name='Betreff der Bestätigungsmail'),
        ),
    ]
