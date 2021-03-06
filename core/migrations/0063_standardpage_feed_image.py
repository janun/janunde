# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-03-09 16:16
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0062_auto_20170118_2353'),
    ]

    operations = [
        migrations.AddField(
            model_name='standardpage',
            name='feed_image',
            field=models.ForeignKey(blank=True, help_text='Wird in Übersichten verwendet.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='core.AttributedImage', verbose_name='Hauptbild'),
        ),
    ]
