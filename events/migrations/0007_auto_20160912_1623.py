# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-12 14:23
from __future__ import unicode_literals

import core.blocks
from django.db import migrations
import wagtail.wagtailcore.blocks
import wagtail.wagtailcore.fields
import wagtail.wagtailembeds.blocks
import wagtail.wagtailimages.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0006_auto_20160908_1602'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventpage',
            name='content',
            field=wagtail.wagtailcore.fields.StreamField((('h2', wagtail.wagtailcore.blocks.StructBlock((('title', wagtail.wagtailcore.blocks.CharBlock(label='Titel')), ('color', wagtail.wagtailcore.blocks.ChoiceBlock(choices=[('brown', 'Braun'), ('green', 'Grün'), ('red', 'Rot'), ('blue', 'Blau'), ('orange', 'Orange')], default='brown', label='Farbe')), ('bold', wagtail.wagtailcore.blocks.BooleanBlock(help_text='Für eine große und fette Überschrift', label='Fett', required=False))))), ('paragraph', core.blocks.ParagraphBlock()), ('image', wagtail.wagtailcore.blocks.StructBlock((('image', wagtail.wagtailimages.blocks.ImageChooserBlock(label='Bild')), ('caption', wagtail.wagtailcore.blocks.CharBlock(label='Bildunterschrift', required=False)), ('full_width', wagtail.wagtailcore.blocks.BooleanBlock(help_text='Soll das Bild auf voller Breite des Bildschirms angezeigt werden?', label='volle Breite', required=False))))), ('embedded_video', wagtail.wagtailcore.blocks.StructBlock((('embed', wagtail.wagtailembeds.blocks.EmbedBlock('Video-URL', help_text='URL von z.B. Youtube oder Vimeo hier reinkopieren')), ('caption', wagtail.wagtailcore.blocks.CharBlock(label='Bildunterschrift', required=False))))), ('button', wagtail.wagtailcore.blocks.StructBlock((('text', wagtail.wagtailcore.blocks.CharBlock(label='Text')), ('link', wagtail.wagtailcore.blocks.URLBlock(label='Link')), ('color', wagtail.wagtailcore.blocks.ChoiceBlock(choices=[('brown', 'Braun'), ('green', 'Grün'), ('red', 'Rot'), ('blue', 'Blau'), ('orange', 'Orange')], default='green', label='Farbe'))))), ('attachment', core.blocks.Attachment()), ('sticker', wagtail.wagtailcore.blocks.StructBlock((('title', wagtail.wagtailcore.blocks.CharBlock(label='Text')), ('color', wagtail.wagtailcore.blocks.ChoiceBlock(choices=[('brown', 'Braun'), ('green', 'Grün'), ('red', 'Rot'), ('blue', 'Blau'), ('orange', 'Orange')], default='green', label='Farbe')), ('link', wagtail.wagtailcore.blocks.URLBlock(label='Link')))))), blank=True, verbose_name='Inhalt'),
        ),
    ]
