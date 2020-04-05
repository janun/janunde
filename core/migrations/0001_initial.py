# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-03 17:37
from __future__ import unicode_literals

import django.db.models.deletion
import modelcluster.fields
import taggit.managers
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.search.index
import wagtail.images.models
from django.conf import settings
from django.db import migrations, models

import core.blocks


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('wagtailcore', '0023_alter_page_revision_on_delete_behaviour'),
        ('taggit', '0002_auto_20150616_2121'),
        ('wagtailimages', '0010_change_on_delete_behaviour'),
    ]

    operations = [
        migrations.CreateModel(
            name='AttributedImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('file', models.ImageField(height_field='height', upload_to=wagtail.images.models.get_upload_to, verbose_name='file', width_field='width')),
                ('width', models.IntegerField(editable=False, verbose_name='width')),
                ('height', models.IntegerField(editable=False, verbose_name='height')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='created at')),
                ('focal_point_x', models.PositiveIntegerField(blank=True, null=True)),
                ('focal_point_y', models.PositiveIntegerField(blank=True, null=True)),
                ('focal_point_width', models.PositiveIntegerField(blank=True, null=True)),
                ('focal_point_height', models.PositiveIntegerField(blank=True, null=True)),
                ('file_size', models.PositiveIntegerField(editable=False, null=True)),
                ('author', models.CharField(blank=True, max_length=255, verbose_name='Autor')),
                ('author_url', models.URLField(blank=True, max_length=255, verbose_name='Autor-Website')),
                ('source', models.URLField(blank=True, max_length=255, verbose_name='Quelle')),
                ('license', models.CharField(blank=True, max_length=255, verbose_name='Lizenz')),
                ('license_url', models.URLField(blank=True, max_length=255, verbose_name='Lizenz-Website')),
                ('tags', taggit.managers.TaggableManager(blank=True, help_text=None, through='taggit.TaggedItem', to='taggit.Tag', verbose_name='tags')),
                ('uploaded_by_user', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='uploaded by user')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model, wagtail.search.index.Indexed),
        ),
        migrations.CreateModel(
            name='AttributedRendition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.ImageField(height_field='height', upload_to='images', width_field='width')),
                ('width', models.IntegerField(editable=False)),
                ('height', models.IntegerField(editable=False)),
                ('focal_point_key', models.CharField(blank=True, default='', editable=False, max_length=255)),
                ('filter', models.IntegerField(blank=True, null=True)),
                ('image', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='renditions', to='core.AttributedImage')),
            ],
        ),
        migrations.CreateModel(
            name='BasePage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='StandardPageRelatedPage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('page', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='related_pages', to='wagtailcore.Page')),
                ('related_page', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='wagtailcore.Page', verbose_name='Zugehörige Seite')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ArticleIndexPage',
            fields=[
                ('basepage_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.BasePage')),
            ],
            options={
                'verbose_name': 'Auflistung von Artikeln',
            },
            bases=('core.basepage',),
        ),
        migrations.CreateModel(
            name='EventIndexPage',
            fields=[
                ('basepage_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.BasePage')),
            ],
            options={
                'verbose_name': 'Auflistung von Veranstaltungen',
                'verbose_name_plural': 'Auflistungen von Veranstaltungen',
            },
            bases=('core.basepage',),
        ),
        migrations.CreateModel(
            name='HomePage',
            fields=[
                ('basepage_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.BasePage')),
            ],
            options={
                'verbose_name': 'Startseite',
            },
            bases=('core.basepage',),
        ),
        migrations.CreateModel(
            name='StandardPage',
            fields=[
                ('basepage_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.BasePage')),
                ('body', wagtail.core.fields.StreamField((('paragraph', wagtail.core.blocks.RichTextBlock(icon='pilcrow', label='Absatz')), ('image', core.blocks.ImageBlock()), ('pullquote', wagtail.core.blocks.StructBlock((('quote', wagtail.core.blocks.TextBlock(label='Zitat')), ('attribution', wagtail.core.blocks.CharBlock(label='Zuschreibung'))))), ('embedded_video', core.blocks.EmbedBlock())), blank=True, verbose_name='Inhalt')),
            ],
            options={
                'verbose_name': 'Einfache Seite',
                'verbose_name_plural': 'Einfache Seiten',
            },
            bases=('core.basepage',),
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('standardpage_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.StandardPage')),
                ('highlight', models.BooleanField(default=False, help_text='Ist dies ein ge-highlighteter Artikel? Falls ja, taucht es z.B. auf der Startseite auf.', verbose_name='Highlight')),
                ('main_image', models.ForeignKey(blank=True, help_text='Bild, das den Artikel repräsentiert. Wird in Übersichten verwendet.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='core.AttributedImage', verbose_name='Hauptbild')),
            ],
            options={
                'verbose_name': 'Artikel',
                'verbose_name_plural': 'Artikel',
            },
            bases=('core.standardpage',),
        ),
        migrations.CreateModel(
            name='EventPage',
            fields=[
                ('standardpage_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.StandardPage')),
                ('highlight', models.BooleanField(default=False, help_text='Ist dies eine ge-highlightete Veranstaltung? Falls ja, taucht es z.B. auf der Startseite auf.', verbose_name='Highlight')),
                ('start_datetime', models.DateTimeField(verbose_name='Startzeit')),
                ('end_datetime', models.DateTimeField(blank=True, null=True, verbose_name='Endzeit')),
                ('main_image', models.ForeignKey(blank=True, help_text='Bild, das die Veranstaltung repräsentiert. Wird in Übersichten verwendet.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='core.AttributedImage', verbose_name='Hauptbild')),
            ],
            options={
                'verbose_name': 'Veranstaltung',
                'verbose_name_plural': 'Veranstaltungen',
            },
            bases=('core.standardpage',),
        ),
        migrations.AlterUniqueTogether(
            name='attributedrendition',
            unique_together=set([('image', 'filter', 'focal_point_key')]),
        ),
    ]
