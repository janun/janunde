# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-30 12:00
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0029_auto_20160829_2322'),
    ]

    operations = [
        migrations.AlterField(
            model_name='standardpage',
            name='author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='pages', to='core.Person', verbose_name='Autor'),
        ),
    ]