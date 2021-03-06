# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-04-15 15:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_auto_20160415_1641'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventpage',
            name='color',
            field=models.CharField(blank=True, choices=[('rgb(70, 187, 0)', 'Grün'), ('rgb(196, 23, 55)', 'Rot'), ('rgb(0, 118, 164)', 'Blau'), ('rgb(233, 88, 34)', 'Orange')], help_text='Farbe, die diese Veranstaltung bekommt, falls kein Poster angegeben ist.', max_length=10, null=True, verbose_name='Farbe'),
        ),
    ]
