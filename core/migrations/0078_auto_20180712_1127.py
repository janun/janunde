# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-07-12 09:27
from __future__ import unicode_literals

import core.blocks
from django.db import migrations
import wagtail.contrib.table_block.blocks
import wagtail.wagtailcore.blocks
import wagtail.wagtailcore.fields
import wagtail.wagtailembeds.blocks
import wagtail.wagtailimages.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0077_group_list_on_group_index_page'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='body',
            field=wagtail.wagtailcore.fields.StreamField((('paragraph', core.blocks.ParagraphBlock(features=['h2', 'h3', 'bold', 'italic', 'link', 'ol', 'ul', 'document-link'])), ('image', wagtail.wagtailcore.blocks.StructBlock((('image', wagtail.wagtailimages.blocks.ImageChooserBlock(label='Bild')), ('caption', wagtail.wagtailcore.blocks.CharBlock(label='opt. Beschrift.', required=False)), ('size', wagtail.wagtailcore.blocks.ChoiceBlock(choices=[('text-width', 'Text-Breite'), ('over-text-width', 'Über-Text-Breite'), ('screen-width', 'Bildchirm-Breite')]))))), ('several_images', core.blocks.ImagesBlock(core.blocks.ImageCarouselBlock)), ('gallery', wagtail.wagtailcore.blocks.StructBlock((('collection', wagtail.wagtailcore.blocks.ChoiceBlock(choices=core.blocks.get_image_gallery_choices, help_text='Die Bilder aus der Sammlung werden dann als Gallerie angezeigt.', label='Sammlung')), ('start_image', wagtail.wagtailimages.blocks.ImageChooserBlock(help_text='Das Bild, das als erstes angezeigt wird.', label='erstes Bild', required=False))))), ('embed', wagtail.wagtailcore.blocks.StructBlock((('embed', wagtail.wagtailembeds.blocks.EmbedBlock(help_text='von z.B. einem Youtube-Video, Facebook-Post, Instagram-Bild, …', label='URL')), ('caption', wagtail.wagtailcore.blocks.CharBlock(label='opt. Beschrift.', required=False)), ('size', wagtail.wagtailcore.blocks.ChoiceBlock(choices=[('text-width', 'Text-Breite'), ('over-text-width', 'Über-Text-Breite'), ('screen-width', 'Bildchirm-Breite')]))))), ('button', wagtail.wagtailcore.blocks.StructBlock((('text', wagtail.wagtailcore.blocks.CharBlock(label='Text')), ('link', wagtail.wagtailcore.blocks.URLBlock(label='Link', required=False)), ('mail', wagtail.wagtailcore.blocks.EmailBlock(help_text='wird anstelle von link benutzt', label='E-Mail', required=False)), ('color', wagtail.wagtailcore.blocks.ChoiceBlock(choices=[('green', 'Grün'), ('red', 'Rot'), ('blue', 'Blau'), ('orange', 'Orange'), ('purple', 'Lila')], label='Farbe')), ('aslink', wagtail.wagtailcore.blocks.BooleanBlock(label='ohne Hintergrund', required=False))))), ('attachment', core.blocks.Attachment()), ('table', wagtail.contrib.table_block.blocks.TableBlock()), ('map_image', wagtail.wagtailcore.blocks.StructBlock((('tile_url', wagtail.wagtailcore.blocks.URLBlock(help_text='URL zu den Kacheln, aus denen das Bild besteht. Benutze {z}, {x}, {y} in der URL für die Koordinaten', label='Kachel-URL', required=True)), ('height', wagtail.wagtailcore.blocks.DecimalBlock(help_text='in speziellen Leaflet Einheiten', label='Höhe', required=True)), ('width', wagtail.wagtailcore.blocks.DecimalBlock(help_text='in speziellen Leaflet Einheiten', label='Breite', required=True)), ('attribution', wagtail.wagtailcore.blocks.CharBlock(help_text='Wird unten rechts im Bild angezeigt.', label='Urheber', required=False)))))), blank=True, verbose_name='Inhalt'),
        ),
        migrations.AlterField(
            model_name='standardpage',
            name='body',
            field=wagtail.wagtailcore.fields.StreamField((('paragraph', core.blocks.ParagraphBlock(features=['h2', 'h3', 'bold', 'italic', 'link', 'ol', 'ul', 'document-link'])), ('image', wagtail.wagtailcore.blocks.StructBlock((('image', wagtail.wagtailimages.blocks.ImageChooserBlock(label='Bild')), ('caption', wagtail.wagtailcore.blocks.CharBlock(label='opt. Beschrift.', required=False)), ('size', wagtail.wagtailcore.blocks.ChoiceBlock(choices=[('text-width', 'Text-Breite'), ('over-text-width', 'Über-Text-Breite'), ('screen-width', 'Bildchirm-Breite')]))))), ('several_images', core.blocks.ImagesBlock(core.blocks.ImageCarouselBlock)), ('gallery', wagtail.wagtailcore.blocks.StructBlock((('collection', wagtail.wagtailcore.blocks.ChoiceBlock(choices=core.blocks.get_image_gallery_choices, help_text='Die Bilder aus der Sammlung werden dann als Gallerie angezeigt.', label='Sammlung')), ('start_image', wagtail.wagtailimages.blocks.ImageChooserBlock(help_text='Das Bild, das als erstes angezeigt wird.', label='erstes Bild', required=False))))), ('embed', wagtail.wagtailcore.blocks.StructBlock((('embed', wagtail.wagtailembeds.blocks.EmbedBlock(help_text='von z.B. einem Youtube-Video, Facebook-Post, Instagram-Bild, …', label='URL')), ('caption', wagtail.wagtailcore.blocks.CharBlock(label='opt. Beschrift.', required=False)), ('size', wagtail.wagtailcore.blocks.ChoiceBlock(choices=[('text-width', 'Text-Breite'), ('over-text-width', 'Über-Text-Breite'), ('screen-width', 'Bildchirm-Breite')]))))), ('button', wagtail.wagtailcore.blocks.StructBlock((('text', wagtail.wagtailcore.blocks.CharBlock(label='Text')), ('link', wagtail.wagtailcore.blocks.URLBlock(label='Link', required=False)), ('mail', wagtail.wagtailcore.blocks.EmailBlock(help_text='wird anstelle von link benutzt', label='E-Mail', required=False)), ('color', wagtail.wagtailcore.blocks.ChoiceBlock(choices=[('green', 'Grün'), ('red', 'Rot'), ('blue', 'Blau'), ('orange', 'Orange'), ('purple', 'Lila')], label='Farbe')), ('aslink', wagtail.wagtailcore.blocks.BooleanBlock(label='ohne Hintergrund', required=False))))), ('attachment', core.blocks.Attachment()), ('table', wagtail.contrib.table_block.blocks.TableBlock()), ('map_image', wagtail.wagtailcore.blocks.StructBlock((('tile_url', wagtail.wagtailcore.blocks.URLBlock(help_text='URL zu den Kacheln, aus denen das Bild besteht. Benutze {z}, {x}, {y} in der URL für die Koordinaten', label='Kachel-URL', required=True)), ('height', wagtail.wagtailcore.blocks.DecimalBlock(help_text='in speziellen Leaflet Einheiten', label='Höhe', required=True)), ('width', wagtail.wagtailcore.blocks.DecimalBlock(help_text='in speziellen Leaflet Einheiten', label='Breite', required=True)), ('attribution', wagtail.wagtailcore.blocks.CharBlock(help_text='Wird unten rechts im Bild angezeigt.', label='Urheber', required=False)))))), blank=True, verbose_name='Inhalt'),
        ),
        migrations.AlterField(
            model_name='thema',
            name='body',
            field=wagtail.wagtailcore.fields.StreamField((('paragraph', core.blocks.ParagraphBlock(features=['h2', 'h3', 'bold', 'italic', 'link', 'ol', 'ul', 'document-link'])), ('image', wagtail.wagtailcore.blocks.StructBlock((('image', wagtail.wagtailimages.blocks.ImageChooserBlock(label='Bild')), ('caption', wagtail.wagtailcore.blocks.CharBlock(label='opt. Beschrift.', required=False)), ('size', wagtail.wagtailcore.blocks.ChoiceBlock(choices=[('text-width', 'Text-Breite'), ('over-text-width', 'Über-Text-Breite'), ('screen-width', 'Bildchirm-Breite')]))))), ('several_images', core.blocks.ImagesBlock(core.blocks.ImageCarouselBlock)), ('gallery', wagtail.wagtailcore.blocks.StructBlock((('collection', wagtail.wagtailcore.blocks.ChoiceBlock(choices=core.blocks.get_image_gallery_choices, help_text='Die Bilder aus der Sammlung werden dann als Gallerie angezeigt.', label='Sammlung')), ('start_image', wagtail.wagtailimages.blocks.ImageChooserBlock(help_text='Das Bild, das als erstes angezeigt wird.', label='erstes Bild', required=False))))), ('embed', wagtail.wagtailcore.blocks.StructBlock((('embed', wagtail.wagtailembeds.blocks.EmbedBlock(help_text='von z.B. einem Youtube-Video, Facebook-Post, Instagram-Bild, …', label='URL')), ('caption', wagtail.wagtailcore.blocks.CharBlock(label='opt. Beschrift.', required=False)), ('size', wagtail.wagtailcore.blocks.ChoiceBlock(choices=[('text-width', 'Text-Breite'), ('over-text-width', 'Über-Text-Breite'), ('screen-width', 'Bildchirm-Breite')]))))), ('button', wagtail.wagtailcore.blocks.StructBlock((('text', wagtail.wagtailcore.blocks.CharBlock(label='Text')), ('link', wagtail.wagtailcore.blocks.URLBlock(label='Link', required=False)), ('mail', wagtail.wagtailcore.blocks.EmailBlock(help_text='wird anstelle von link benutzt', label='E-Mail', required=False)), ('color', wagtail.wagtailcore.blocks.ChoiceBlock(choices=[('green', 'Grün'), ('red', 'Rot'), ('blue', 'Blau'), ('orange', 'Orange'), ('purple', 'Lila')], label='Farbe')), ('aslink', wagtail.wagtailcore.blocks.BooleanBlock(label='ohne Hintergrund', required=False))))), ('attachment', core.blocks.Attachment()), ('table', wagtail.contrib.table_block.blocks.TableBlock()), ('map_image', wagtail.wagtailcore.blocks.StructBlock((('tile_url', wagtail.wagtailcore.blocks.URLBlock(help_text='URL zu den Kacheln, aus denen das Bild besteht. Benutze {z}, {x}, {y} in der URL für die Koordinaten', label='Kachel-URL', required=True)), ('height', wagtail.wagtailcore.blocks.DecimalBlock(help_text='in speziellen Leaflet Einheiten', label='Höhe', required=True)), ('width', wagtail.wagtailcore.blocks.DecimalBlock(help_text='in speziellen Leaflet Einheiten', label='Breite', required=True)), ('attribution', wagtail.wagtailcore.blocks.CharBlock(help_text='Wird unten rechts im Bild angezeigt.', label='Urheber', required=False)))))), blank=True, verbose_name='Beschreibung'),
        ),
    ]