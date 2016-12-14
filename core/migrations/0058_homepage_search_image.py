# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-14 14:21
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0057_auto_20161206_1505'),
    ]

    operations = [
        migrations.AddField(
            model_name='homepage',
            name='search_image',
            field=models.ForeignKey(blank=True, help_text='Wird z.B. angezeigt, wenn jmd. www.janun.de bei Facebook postet', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='core.AttributedImage', verbose_name='Suchmaschinen-Bild'),
        ),
    ]
