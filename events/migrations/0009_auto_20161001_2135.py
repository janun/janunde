# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-01 19:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0008_auto_20160913_1709'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventpage',
            name='color',
            field=models.CharField(blank=True, choices=[('green', 'Grün'), ('red', 'Rot'), ('blue', 'Blau'), ('orange', 'Orange')], help_text='Die Veranstaltung bekommt diese Farbe, falls es kein Bild gibt.', max_length=18, null=True, verbose_name='Farbe als Ersatz für Bild'),
        ),
    ]