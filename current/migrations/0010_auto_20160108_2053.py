# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('current', '0009_auto_20160107_2251'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='subheading',
            field=models.CharField(verbose_name='optionale Unterüberschrift', max_length=255, blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='article',
            name='hide_title',
            field=models.BooleanField(verbose_name='Titel verstecken', help_text='Titel unter Unterüberschrift verstecken. Z.B. wenn der Text schon im Hauptbild enthalten ist.', default=False),
        ),
    ]
