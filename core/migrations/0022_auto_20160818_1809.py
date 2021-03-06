# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-18 16:09
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0021_thema'),
    ]

    database_operations = [
        migrations.AlterModelTable('EventPage', 'events_eventpage'),
        migrations.AlterModelTable('EventIndexPage', 'events_eventindexpage')
    ]

    state_operations = [
        migrations.DeleteModel('EventPage'),
        migrations.DeleteModel('EventIndexPage')
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=database_operations,
            state_operations=state_operations)
    ]
