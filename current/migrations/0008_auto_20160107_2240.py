# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('current', '0007_auto_20160107_2236'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='dont_crop',
            field=models.BooleanField(default=False, verbose_name='Hauptbild nicht abschneiden', help_text='Normalerweise wird das Hauptbild beschnitten um auf besser auf die Seite zu passen'),
        ),
        migrations.AlterField(
            model_name='article',
            name='hide_title',
            field=models.BooleanField(default=False, verbose_name='Titel verstecken', help_text='Titel verstecken. Z.B. wenn der Text schon im Hauptbild enthalten ist.'),
        ),
    ]
