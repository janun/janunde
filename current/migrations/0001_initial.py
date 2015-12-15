# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import wagtail.wagtailcore.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0020_add_index_on_page_first_published_at'),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('page_ptr', models.OneToOneField(to='wagtailcore.Page', primary_key=True, auto_created=True, parent_link=True, serialize=False)),
                ('body', wagtail.wagtailcore.fields.RichTextField()),
            ],
            options={
                'verbose_name': 'Artikel',
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='Current',
            fields=[
                ('page_ptr', models.OneToOneField(to='wagtailcore.Page', primary_key=True, auto_created=True, parent_link=True, serialize=False)),
            ],
            options={
                'verbose_name': 'Aktuelles',
            },
            bases=('wagtailcore.page',),
        ),
    ]
