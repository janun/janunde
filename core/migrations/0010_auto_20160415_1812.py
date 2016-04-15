# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-04-15 16:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_eventpage_color'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventpage',
            name='location',
            field=models.CharField(blank=True, help_text='Ort, an dem die Veranstaltung stattfindet', max_length=255, null=True, verbose_name='Ort'),
        ),
        migrations.AlterField(
            model_name='eventpage',
            name='color',
            field=models.CharField(blank=True, choices=[('rgb(70, 187, 0)', 'Grün'), ('rgb(196, 23, 55)', 'Rot'), ('rgb(0, 118, 164)', 'Blau'), ('rgb(233, 88, 34)', 'Orange')], help_text='Farbe, die diese Veranstaltung bekommt, falls kein Poster angegeben ist.', max_length=18, null=True, verbose_name='Farbe'),
        ),
    ]
