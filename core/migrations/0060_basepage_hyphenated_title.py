# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-25 14:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0059_auto_20161222_1644'),
    ]

    def populate_hyphenated_title(apps, schema_editor):
        BasePage = apps.get_model("core", "BasePage")
        for page in BasePage.objects.all():
            page.save()

    operations = [
        migrations.AddField(
            model_name='basepage',
            name='hyphenated_title',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.RunPython(populate_hyphenated_title, lambda a,s: None),
    ]
