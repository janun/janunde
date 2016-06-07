# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-07 18:08
from __future__ import unicode_literals

import core.fields
from django.db import migrations, models
import wagtail.wagtailimages.models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_auto_20160529_2028'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventpage',
            name='register_url',
            field=core.fields.PrettyURLField(blank=True, help_text='Link zu einem externen Anmelde-Formular', null=True, verbose_name='Anmelde-Formular'),
        ),
        migrations.AlterField(
            model_name='attributedrendition',
            name='file',
            field=models.ImageField(height_field='height', upload_to=wagtail.wagtailimages.models.get_rendition_upload_to, width_field='width'),
        ),
        migrations.AlterField(
            model_name='eventpage',
            name='all_day',
            field=models.BooleanField(default=False, help_text='Bei ganztägigen Veranstaltungen werden Uhrzeiten ignoriert.', verbose_name='ganztägig'),
        ),
    ]
