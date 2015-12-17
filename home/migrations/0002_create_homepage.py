# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations
from django.core.exceptions import ObjectDoesNotExist

homepage_title = "Startseite"
homepage_slug = homepage_title.lower()
homepage_url = '/'


def create_homepage(apps, schema_editor):
    """Creates a new HomePage titled homepage_title
    being the site root, also deletes default site root and default homepage"""
    # Get models
    ContentType = apps.get_model('contenttypes.ContentType')
    Page = apps.get_model('wagtailcore.Page')
    Site = apps.get_model('wagtailcore.Site')
    HomePage = apps.get_model('home.HomePage')

    # Delete the default homepage if it exists
    try:
        Page.objects.get(id=2).delete()
    except ObjectDoesNotExist:
        pass

    # Create content type for homepage model
    homepage_content_type, created = ContentType.objects.get_or_create(
        model='homepage', app_label='home')

    # Create a new homepage
    homepage = HomePage.objects.create(
        title=homepage_title,
        slug=homepage_slug,
        content_type=homepage_content_type,
        path='00010001',
        depth=2,
        numchild=0,
        url_path=homepage_url,
    )

    # Create a site with the new homepage set as the root
    Site.objects.create(
        hostname='localhost',
        root_page=homepage,
        is_default_site=True
    )


def delete_homepage(apps, schema_editor):
    HomePage = apps.get_model('home.HomePage')
    # Delete the homepage if it exists
    try:
        HomePage.objects.get(title=homepage_title).delete()
    except ObjectDoesNotExist:
        pass


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0002_initial_data'),
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_homepage, delete_homepage),
    ]
