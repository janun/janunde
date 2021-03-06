# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-27 15:17
from __future__ import unicode_literals

from django.db import migrations, models
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0069_formpage_send_confirmation_mail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='formpage',
            name='confirmation_mail_field',
            field=models.CharField(blank=True, help_text='Exakte Beschriftung des Felds aus dem Formular für die E-Mail-Adresse des Benutzers. Dahin wird die Bestätigungsmail geschickt.', max_length=255, verbose_name='Feld für E-Mail-Adresse'),
        ),
        migrations.AlterField(
            model_name='formpage',
            name='confirmation_mail_subject',
            field=models.CharField(blank=True, max_length=255, verbose_name='Betreff'),
        ),
        migrations.AlterField(
            model_name='formpage',
            name='confirmation_mail_text',
            field=wagtail.core.fields.RichTextField(blank=True, help_text='Welcher Text soll in der Bestätigungsmail sein?', verbose_name='Text'),
        ),
        migrations.AlterField(
            model_name='formpage',
            name='send_confirmation_mail',
            field=models.BooleanField(default='False', help_text='Soll der Benutzer nach Ausfüllen des Formulars eine Bestätigungsmail bekommen?', verbose_name='Bestätigungsmail versenden?'),
        ),
    ]
