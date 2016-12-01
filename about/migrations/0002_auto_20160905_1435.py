# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-05 12:35
from __future__ import unicode_literals

import core.blocks
from django.db import migrations, models
import django.db.models.deletion
import wagtail.wagtailcore.blocks
import wagtail.wagtailcore.fields
import wagtail.wagtailimages.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0033_auto_20160830_1804'),
        ('about', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='aboutpage',
            name='content',
            field=wagtail.wagtailcore.fields.StreamField((('h2', wagtail.wagtailcore.blocks.StructBlock((('title', wagtail.wagtailcore.blocks.CharBlock(label='Titel')), ('color', wagtail.wagtailcore.blocks.ChoiceBlock(choices=[('brown', 'Braun'), ('green', 'Grün'), ('red', 'Rot'), ('blue', 'Blau'), ('orange', 'Orange')], default='brown', label='Farbe'))))), ('paragraph', wagtail.wagtailcore.blocks.RichTextBlock(icon='pilcrow', label='Absatz')), ('image', wagtail.wagtailcore.blocks.StructBlock((('image', wagtail.wagtailimages.blocks.ImageChooserBlock(label='Bild')), ('caption', wagtail.wagtailcore.blocks.CharBlock(label='Bildunterschrift', required=False)), ('full_width', wagtail.wagtailcore.blocks.BooleanBlock(help_text='Soll das Bild auf voller Breite des Bildschirms angezeigt werden?', label='volle Breite', required=False))))), ('embedded_video', core.blocks.EmbedBlock()), ('button', wagtail.wagtailcore.blocks.StructBlock((('text', wagtail.wagtailcore.blocks.CharBlock(label='Text')), ('link', wagtail.wagtailcore.blocks.URLBlock(label='Link')), ('color', wagtail.wagtailcore.blocks.ChoiceBlock(choices=[('brown', 'Braun'), ('green', 'Grün'), ('red', 'Rot'), ('blue', 'Blau'), ('orange', 'Orange')], default='green', label='Farbe'))))), ('attachment', core.blocks.Attachment())), blank=True, verbose_name='Inhalt'),
        ),
        migrations.AddField(
            model_name='aboutpage',
            name='heading',
            field=models.CharField(blank=True, max_length=255, verbose_name='Überschrift'),
        ),
        migrations.AddField(
            model_name='aboutpage',
            name='image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='core.AttributedImage', verbose_name='Bild'),
        ),
        migrations.AddField(
            model_name='aboutpage',
            name='intro_text',
            field=wagtail.wagtailcore.fields.RichTextField(blank=True, verbose_name='Eingangstext'),
        ),
    ]
