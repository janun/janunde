# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-29 17:46
from __future__ import unicode_literals

import core.blocks
from django.db import migrations
import wagtail.wagtailcore.blocks
import wagtail.wagtailcore.fields
import wagtail.wagtailimages.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_auto_20160825_1618'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventpage',
            name='content',
            field=wagtail.wagtailcore.fields.StreamField((('title', wagtail.wagtailcore.blocks.StructBlock((('title', wagtail.wagtailcore.blocks.CharBlock(classname='title', label='Titel')), ('color', wagtail.wagtailcore.blocks.ChoiceBlock(choices=[('brown', 'Braun'), ('green', 'Grün'), ('red', 'Rot'), ('blue', 'Blau'), ('orange', 'Orange')], default='brown', label='Farbe'))))), ('h2', wagtail.wagtailcore.blocks.StructBlock((('title', wagtail.wagtailcore.blocks.CharBlock(label='Titel')), ('color', wagtail.wagtailcore.blocks.ChoiceBlock(choices=[('brown', 'Braun'), ('green', 'Grün'), ('red', 'Rot'), ('blue', 'Blau'), ('orange', 'Orange')], default='brown', label='Farbe'))))), ('paragraph', wagtail.wagtailcore.blocks.RichTextBlock(icon='pilcrow', label='Absatz')), ('image', wagtail.wagtailcore.blocks.StructBlock((('image', wagtail.wagtailimages.blocks.ImageChooserBlock(label='Bild')), ('caption', wagtail.wagtailcore.blocks.CharBlock(label='Bildunterschrift', required=False)), ('full_width', wagtail.wagtailcore.blocks.BooleanBlock(help_text='Soll das Bild auf voller Breite des Bildschirms angezeigt werden?', label='volle Breite', required=False))))), ('embedded_video', core.blocks.VideoBlock()), ('button', wagtail.wagtailcore.blocks.StructBlock((('text', wagtail.wagtailcore.blocks.CharBlock(label='Text')), ('link', wagtail.wagtailcore.blocks.URLBlock(label='Link')), ('color', wagtail.wagtailcore.blocks.ChoiceBlock(choices=[('brown', 'Braun'), ('green', 'Grün'), ('red', 'Rot'), ('blue', 'Blau'), ('orange', 'Orange')], default='green', label='Farbe'))))), ('attachment', core.blocks.Attachment())), blank=True, verbose_name='Inhalt'),
        ),
    ]