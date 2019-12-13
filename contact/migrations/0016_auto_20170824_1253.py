# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-24 10:53
from __future__ import unicode_literals

import core.blocks
from django.db import migrations
import wagtail.contrib.table_block.blocks
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.embeds.blocks
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0015_auto_20170803_1715'),
    ]

    operations = [
        migrations.AlterField(
            model_name='officepage',
            name='text',
            field=wagtail.core.fields.StreamField((('paragraph', core.blocks.ParagraphBlock()), ('image', wagtail.core.blocks.StructBlock((('image', wagtail.images.blocks.ImageChooserBlock(label='Bild')), ('caption', wagtail.core.blocks.CharBlock(label='opt. Beschrift.', required=False)), ('size', wagtail.core.blocks.ChoiceBlock(choices=[('text-width', 'Text-Breite'), ('over-text-width', 'Über-Text-Breite'), ('screen-width', 'Bildchirm-Breite')]))))), ('several_images', core.blocks.ImagesBlock(core.blocks.ImageCarouselBlock)), ('gallery', wagtail.core.blocks.StructBlock((('collection', wagtail.core.blocks.ChoiceBlock(choices=core.blocks.get_image_gallery_choices, help_text='Die Bilder aus der Sammlung werden dann als Gallerie angezeigt.', label='Sammlung')), ('start_image', wagtail.images.blocks.ImageChooserBlock(help_text='Das Bild, das als erstes angezeigt wird.', label='erstes Bild', required=False))))), ('embed', wagtail.core.blocks.StructBlock((('embed', wagtail.embeds.blocks.EmbedBlock(help_text='von z.B. einem Youtube-Video, Facebook-Post, Instagram-Bild, …', label='URL')), ('caption', wagtail.core.blocks.CharBlock(label='opt. Beschrift.', required=False)), ('size', wagtail.core.blocks.ChoiceBlock(choices=[('text-width', 'Text-Breite'), ('over-text-width', 'Über-Text-Breite'), ('screen-width', 'Bildchirm-Breite')]))))), ('button', wagtail.core.blocks.StructBlock((('text', wagtail.core.blocks.CharBlock(label='Text')), ('link', wagtail.core.blocks.URLBlock(label='Link', required=False)), ('mail', wagtail.core.blocks.EmailBlock(help_text='wird anstelle von link benutzt', label='E-Mail', required=False)), ('color', wagtail.core.blocks.ChoiceBlock(choices=[('green', 'Grün'), ('red', 'Rot'), ('blue', 'Blau'), ('orange', 'Orange'), ('purple', 'Lila')], label='Farbe')), ('aslink', wagtail.core.blocks.BooleanBlock(label='ohne Hintergrund', required=False))))), ('attachment', core.blocks.Attachment()), ('table', wagtail.contrib.table_block.blocks.TableBlock())), blank=True, verbose_name='Text'),
        ),
        migrations.AlterField(
            model_name='personpage',
            name='text',
            field=wagtail.core.fields.StreamField((('paragraph', core.blocks.ParagraphBlock()), ('image', wagtail.core.blocks.StructBlock((('image', wagtail.images.blocks.ImageChooserBlock(label='Bild')), ('caption', wagtail.core.blocks.CharBlock(label='opt. Beschrift.', required=False)), ('size', wagtail.core.blocks.ChoiceBlock(choices=[('text-width', 'Text-Breite'), ('over-text-width', 'Über-Text-Breite'), ('screen-width', 'Bildchirm-Breite')]))))), ('several_images', core.blocks.ImagesBlock(core.blocks.ImageCarouselBlock)), ('gallery', wagtail.core.blocks.StructBlock((('collection', wagtail.core.blocks.ChoiceBlock(choices=core.blocks.get_image_gallery_choices, help_text='Die Bilder aus der Sammlung werden dann als Gallerie angezeigt.', label='Sammlung')), ('start_image', wagtail.images.blocks.ImageChooserBlock(help_text='Das Bild, das als erstes angezeigt wird.', label='erstes Bild', required=False))))), ('embed', wagtail.core.blocks.StructBlock((('embed', wagtail.embeds.blocks.EmbedBlock(help_text='von z.B. einem Youtube-Video, Facebook-Post, Instagram-Bild, …', label='URL')), ('caption', wagtail.core.blocks.CharBlock(label='opt. Beschrift.', required=False)), ('size', wagtail.core.blocks.ChoiceBlock(choices=[('text-width', 'Text-Breite'), ('over-text-width', 'Über-Text-Breite'), ('screen-width', 'Bildchirm-Breite')]))))), ('button', wagtail.core.blocks.StructBlock((('text', wagtail.core.blocks.CharBlock(label='Text')), ('link', wagtail.core.blocks.URLBlock(label='Link', required=False)), ('mail', wagtail.core.blocks.EmailBlock(help_text='wird anstelle von link benutzt', label='E-Mail', required=False)), ('color', wagtail.core.blocks.ChoiceBlock(choices=[('green', 'Grün'), ('red', 'Rot'), ('blue', 'Blau'), ('orange', 'Orange'), ('purple', 'Lila')], label='Farbe')), ('aslink', wagtail.core.blocks.BooleanBlock(label='ohne Hintergrund', required=False))))), ('attachment', core.blocks.Attachment()), ('table', wagtail.contrib.table_block.blocks.TableBlock())), blank=True, verbose_name='Text'),
        ),
    ]
