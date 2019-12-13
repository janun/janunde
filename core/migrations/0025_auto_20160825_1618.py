# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-25 14:18
from __future__ import unicode_literals

import core.blocks
import core.models
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import modelcluster.fields
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0024_auto_20160819_1506'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='highlight',
        ),
        migrations.RemoveField(
            model_name='attributedimage',
            name='author',
        ),
        migrations.RemoveField(
            model_name='attributedimage',
            name='author_url',
        ),
        migrations.RemoveField(
            model_name='attributedimage',
            name='license',
        ),
        migrations.RemoveField(
            model_name='attributedimage',
            name='license_url',
        ),
        migrations.RemoveField(
            model_name='attributedimage',
            name='original_title',
        ),
        migrations.RemoveField(
            model_name='attributedimage',
            name='source',
        ),
        migrations.AddField(
            model_name='attributedimage',
            name='attribution',
            field=models.CharField(blank=True, max_length=255, verbose_name='Quellenangabe'),
        ),
        migrations.AlterField(
            model_name='highlight',
            name='end_datetime',
            field=models.DateTimeField(default=core.models.get_in_14_days, help_text='Bis wann soll das Highlight auftauchen?', verbose_name='Endzeit'),
        ),
        migrations.AlterField(
            model_name='highlight',
            name='highlighted_page',
            field=modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='highlight', to='wagtailcore.Page'),
        ),
        migrations.AlterField(
            model_name='highlight',
            name='start_datetime',
            field=models.DateTimeField(default=django.utils.timezone.now, help_text='Ab wann soll das Highlight auftauchen?', verbose_name='Startzeit'),
        ),
        migrations.AlterField(
            model_name='highlight',
            name='title_override',
            field=models.CharField(blank=True, help_text='Wird statt des Titels des Originals angezeigt.', max_length=255, verbose_name='Überschreib-Titel'),
        ),
        migrations.AlterField(
            model_name='standardpage',
            name='body',
            field=wagtail.core.fields.StreamField((('title', wagtail.core.blocks.StructBlock((('title', wagtail.core.blocks.CharBlock(classname='title', label='Titel')), ('color', wagtail.core.blocks.ChoiceBlock(choices=[('brown', 'Braun'), ('green', 'Grün'), ('red', 'Rot'), ('blue', 'Blau'), ('orange', 'Orange')], classname='', default='brown', label='Farbe'))))), ('paragraph', wagtail.core.blocks.RichTextBlock(icon='pilcrow', label='Absatz')), ('image', wagtail.core.blocks.StructBlock((('image', wagtail.images.blocks.ImageChooserBlock(label='Bild')), ('caption', wagtail.core.blocks.CharBlock(label='Bildunterschrift', required=False))))), ('embedded_video', core.blocks.EmbedBlock())), blank=True, verbose_name='Inhalt'),
        ),
        migrations.AlterField(
            model_name='thema',
            name='body',
            field=wagtail.core.fields.StreamField((('title', wagtail.core.blocks.StructBlock((('title', wagtail.core.blocks.CharBlock(classname='title', label='Titel')), ('color', wagtail.core.blocks.ChoiceBlock(choices=[('brown', 'Braun'), ('green', 'Grün'), ('red', 'Rot'), ('blue', 'Blau'), ('orange', 'Orange')], classname='', default='brown', label='Farbe'))))), ('paragraph', wagtail.core.blocks.RichTextBlock(icon='pilcrow', label='Absatz')), ('image', wagtail.core.blocks.StructBlock((('image', wagtail.images.blocks.ImageChooserBlock(label='Bild')), ('caption', wagtail.core.blocks.CharBlock(label='Bildunterschrift', required=False))))), ('embedded_video', core.blocks.EmbedBlock())), blank=True, verbose_name='Beschreibung'),
        ),
    ]
