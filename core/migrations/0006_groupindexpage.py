# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-04-04 12:13
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_group_standardpagerelatedgroup'),
    ]

    operations = [
        migrations.CreateModel(
            name='GroupIndexPage',
            fields=[
                ('basepage_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.BasePage')),
            ],
            options={
                'verbose_name': 'Auflistung von Gruppen',
            },
            bases=('core.basepage',),
        ),
    ]