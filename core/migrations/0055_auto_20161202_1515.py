# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-02 14:15
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        # ('contact', '0009_auto_20161201_2007'),
        ("core", "0054_project"),
    ]

    operations = [
        migrations.RemoveField(model_name="standardpage", name="author",),
    ]
