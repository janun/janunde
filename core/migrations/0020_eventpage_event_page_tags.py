# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-16 14:59
from __future__ import unicode_literals

from django.db import migrations
import modelcluster.contrib.taggit


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0002_auto_20150616_2121'),
        ('core', '0019_auto_20160816_1653'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventpage',
            name='event_page_tags',
            field=modelcluster.contrib.taggit.ClusterTaggableManager(blank=True, help_text='A comma-separated list of tags.', through='core.JanunTag', to='taggit.Tag', verbose_name='Tags'),
        ),
    ]
