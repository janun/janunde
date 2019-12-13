# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-01 19:07
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
        ('contact', '0008_auto_20161107_1430'),
    ]

    operations = [
        migrations.AlterField(
            model_name='officepage',
            name='text',
            field=wagtail.core.fields.StreamField((('paragraph', core.blocks.ParagraphBlock()), ('image', wagtail.core.blocks.StructBlock((('image', wagtail.images.blocks.ImageChooserBlock(label='Bild')), ('caption', wagtail.core.blocks.CharBlock(label='opt. Beschrift.', required=False)), ('size', wagtail.core.blocks.ChoiceBlock(choices=[('text-width', 'Text-Breite'), ('over-text-width', 'Über-Text-Breite'), ('screen-width', 'Bildchirm-Breite')]))))), ('embed', wagtail.core.blocks.StructBlock((('embed', wagtail.embeds.blocks.EmbedBlock(help_text='von z.B. einem Youtube-Video, Facebook-Post, Instagram-Bild, …', label='URL')), ('caption', wagtail.core.blocks.CharBlock(label='opt. Beschrift.', required=False)), ('size', wagtail.core.blocks.ChoiceBlock(choices=[('text-width', 'Text-Breite'), ('over-text-width', 'Über-Text-Breite'), ('screen-width', 'Bildchirm-Breite')]))))), ('button', wagtail.core.blocks.StructBlock((('text', wagtail.core.blocks.CharBlock(label='Text')), ('link', wagtail.core.blocks.URLBlock(label='Link')), ('color', wagtail.core.blocks.ChoiceBlock(choices=[('green', 'Grün'), ('red', 'Rot'), ('blue', 'Blau'), ('orange', 'Orange')], default='green', label='Farbe'))))), ('attachment', core.blocks.Attachment()), ('table', wagtail.contrib.table_block.blocks.TableBlock())), blank=True, verbose_name='Text'),
        ),
        migrations.AlterField(
            model_name='personpage',
            name='text',
            field=wagtail.core.fields.StreamField((('paragraph', core.blocks.ParagraphBlock()), ('image', wagtail.core.blocks.StructBlock((('image', wagtail.images.blocks.ImageChooserBlock(label='Bild')), ('caption', wagtail.core.blocks.CharBlock(label='opt. Beschrift.', required=False)), ('size', wagtail.core.blocks.ChoiceBlock(choices=[('text-width', 'Text-Breite'), ('over-text-width', 'Über-Text-Breite'), ('screen-width', 'Bildchirm-Breite')]))))), ('embed', wagtail.core.blocks.StructBlock((('embed', wagtail.embeds.blocks.EmbedBlock(help_text='von z.B. einem Youtube-Video, Facebook-Post, Instagram-Bild, …', label='URL')), ('caption', wagtail.core.blocks.CharBlock(label='opt. Beschrift.', required=False)), ('size', wagtail.core.blocks.ChoiceBlock(choices=[('text-width', 'Text-Breite'), ('over-text-width', 'Über-Text-Breite'), ('screen-width', 'Bildchirm-Breite')]))))), ('button', wagtail.core.blocks.StructBlock((('text', wagtail.core.blocks.CharBlock(label='Text')), ('link', wagtail.core.blocks.URLBlock(label='Link')), ('color', wagtail.core.blocks.ChoiceBlock(choices=[('green', 'Grün'), ('red', 'Rot'), ('blue', 'Blau'), ('orange', 'Orange')], default='green', label='Farbe'))))), ('attachment', core.blocks.Attachment()), ('table', wagtail.contrib.table_block.blocks.TableBlock())), blank=True, verbose_name='Text'),
        ),
    ]
