# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-14 17:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0047_auto_20161114_1822'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='address',
            field=models.CharField(blank=True, help_text='Adresse, an dem die Gruppe zu finden ist', max_length=255, null=True, verbose_name='Adresse'),
        ),
    ]
