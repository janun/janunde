# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations
from django.core.exceptions import ObjectDoesNotExist


current_title = "Aktuelles"
current_slug = current_title.lower()
current_url = '/' + current_slug + '/'


def create_current(apps, schema_editor):
    """Creates a new Current page titled current_title
    being a child of the homepage created by the home app"""
    # Get models
    ContentType = apps.get_model('contenttypes.ContentType')
    Page = apps.get_model('wagtailcore.Page')
    Site = apps.get_model('wagtailcore.Site')
    Current = apps.get_model('current.Current')
    HomePage = apps.get_model('home.HomePage')

    # Create content type for current model
    current_content_type, created = ContentType.objects.get_or_create(
        model='current', app_label='current')

    # Create a new current page
    current = Current.objects.create(
        title=current_title,
        slug=current_slug,
        show_in_menus=True,
        content_type=current_content_type,
        depth=3,
        path='000100010001',
        numchild=0,
        url_path=current_url,
    )

    # adjust parent node
    homepage = HomePage.objects.first()
    homepage.numchild = 1
    homepage.save()


def delete_current(apps, schema_editor):
    Current = apps.get_model('current.Current')
    try:
        Current.objects.get(title=current_title).delete()
    except ObjectDoesNotExist:
        pass


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_create_homepage'), # needs a created homepage
        ('current', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_current, delete_current),
    ]
