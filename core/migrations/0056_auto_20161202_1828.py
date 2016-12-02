# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-02 17:28
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0055_auto_20161202_1515'),
    ]

    operations = [
        migrations.AddField(
            model_name='groupindexpage',
            name='header_image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='core.AttributedImage', verbose_name='Header-Bild'),
        ),
        migrations.AddField(
            model_name='groupindexpage',
            name='heading',
            field=models.CharField(blank=True, max_length=255, verbose_name='Überschrift'),
        ),
    ]
