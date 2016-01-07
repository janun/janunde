# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('current', '0002_create_current'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='highlight',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
    ]
