# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-14 22:47
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0006_auto_20160913_1709'),
        ("core", "0039_remove_standardpage_author"),
    ]

    operations = [
        migrations.AddField(
            model_name="standardpage",
            name="author",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="pages",
                to="contact.PersonPage",
                verbose_name="Autor_in",
            ),
        ),
    ]
