# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('current', '0006_auto_20160107_2209'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='hide_title',
            field=models.BooleanField(default=False, verbose_name='Titel verstecken', help_text='Titel verstecken. Z.B. wenn Text schon im Bild enthalten'),
        ),
        migrations.AlterField(
            model_name='article',
            name='highlight',
            field=models.BooleanField(default=False, verbose_name='Highlight', help_text='Falls ja, taucht es z.B. auf der Startseite auf.'),
        ),
    ]
