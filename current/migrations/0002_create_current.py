# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


def create_current(apps, schema_editor):
    # Get models
    ContentType = apps.get_model('contenttypes.ContentType')
    Page = apps.get_model('wagtailcore.Page')
    Site = apps.get_model('wagtailcore.Site')
    Current = apps.get_model('current.Current')

    # Create content type for current model
    current_content_type, created = ContentType.objects.get_or_create(
        model='current', app_label='current')

    # Create a new current page
    current = Current.objects.create(
        title="Aktuelles",
        slug='aktuelles',
        content_type=current_content_type,
        depth=3,
        numchild=0,
        url_path='/aktuelles/',
    )

class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        #migrations.RunPython(create_current),
    ]
