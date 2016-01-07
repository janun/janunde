# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='socialmediapage',
            name='page',
        ),
        migrations.RemoveField(
            model_name='socialmediasettings',
            name='site',
        ),
        migrations.DeleteModel(
            name='SocialMediaPage',
        ),
        migrations.DeleteModel(
            name='SocialMediaSettings',
        ),
    ]
