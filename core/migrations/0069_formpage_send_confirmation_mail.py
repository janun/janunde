# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-27 13:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0068_formpage_confirmation_mail_subject'),
    ]

    operations = [
        migrations.AddField(
            model_name='formpage',
            name='send_confirmation_mail',
            field=models.BooleanField(default='False', help_text='Benutzer bekommt nach Ausfüllen des Formulars eine Bestätigungsmail', verbose_name='Bestätigungsmail versenden?'),
        ),
    ]
