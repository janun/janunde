# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-20 21:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_group_abbr'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventpage',
            name='subtitle',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Untertitel'),
        ),
        migrations.AlterField(
            model_name='group',
            name='abbr',
            field=models.CharField(blank=True, help_text='Nur zwei Zeichen', max_length=2, null=True, verbose_name='Abkürzung'),
        ),
    ]
