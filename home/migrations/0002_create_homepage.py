# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


def create_homepage(apps, schema_editor):
    # Get models
    ContentType = apps.get_model('contenttypes.ContentType')
    Page = apps.get_model('wagtailcore.Page')
    Site = apps.get_model('wagtailcore.Site')
    HomePage = apps.get_model('home.HomePage')

    # Delete the default homepage and site root
    Page.objects.get(id=2).delete()
    Page.objects.get(id=1).delete()

    # Create content type for homepage model
    homepage_content_type, created = ContentType.objects.get_or_create(
        model='homepage', app_label='home')

    # Create a new homepage as the site root
    homepage = HomePage.objects.create(
        title="Homepage",
        slug='home',
        content_type=homepage_content_type,
        path='0001',
        depth=1,
        numchild=0,
        url_path='/',
    )

    # Create a site with the new homepage set as the root
    Site.objects.create(
        hostname='localhost', root_page=homepage, is_default_site=True)


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_homepage),
    ]
