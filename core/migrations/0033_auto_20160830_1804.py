# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-30 16:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0032_auto_20160830_1506'),
    ]

    operations = [
        migrations.AlterField(
            model_name='standardpage',
            name='title_color',
            field=models.CharField(blank=True, choices=[('brown', 'Braun'), ('green', 'Grün'), ('red', 'Rot'), ('blue', 'Blau'), ('orange', 'Orange')], default='brown', help_text='Der Titel wird in dieser Farbe angezeigt.', max_length=255, null=True, verbose_name='Titelfarbe'),
        ),
    ]
