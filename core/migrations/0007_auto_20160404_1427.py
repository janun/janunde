# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-04-04 12:27
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_groupindexpage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='standardpagerelatedgroup',
            name='page',
        ),
        migrations.RemoveField(
            model_name='standardpagerelatedgroup',
            name='related_group',
        ),
        migrations.AddField(
            model_name='article',
            name='related_group',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='core.Group', verbose_name='Zugehörige Gruppe'),
        ),
        migrations.DeleteModel(
            name='StandardPageRelatedGroup',
        ),
    ]
