# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-14 17:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0048_group_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='subtitle',
            field=models.CharField(blank=True, help_text='Z.B. eine sehr kurze Beschreibung', max_length=80, null=True, verbose_name='Untertitel'),
        ),
    ]
