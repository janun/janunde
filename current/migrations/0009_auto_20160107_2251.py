# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('current', '0008_auto_20160107_2240'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='dont_crop',
            field=models.BooleanField(default=False, help_text='Normalerweise wird das Hauptbild beschnitten, um besser auf die Seite zu passen. Falls ja, wird das Seitenverhältnis des Hauptbildes beibehalten.', verbose_name='Hauptbild nicht abschneiden'),
        ),
        migrations.AlterField(
            model_name='article',
            name='highlight',
            field=models.BooleanField(default=False, help_text='Ist dies ein ge-highlighteter Artikel? Falls ja, taucht es z.B. auf der Startseite auf.', verbose_name='Highlight'),
        ),
    ]
