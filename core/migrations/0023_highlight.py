# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-18 22:35
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0029_unicode_slugfield_dj19'),
        ('core', '0022_auto_20160818_1809'),
    ]

    operations = [
        migrations.CreateModel(
            name='Highlight',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_datetime', models.DateTimeField(verbose_name='Startzeit')),
                ('end_datetime', models.DateTimeField(blank=True, null=True, verbose_name='Endzeit')),
                ('title', models.CharField(max_length=255)),
                ('highlighted_page', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='highlights', to='wagtailcore.Page')),
            ],
        ),
    ]
