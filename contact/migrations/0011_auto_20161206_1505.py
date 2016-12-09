# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-06 14:05
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
        ('contact', '0010_auto_20161202_1828'),
    ]

    operations = [
        migrations.AlterField(
            model_name='officepage',
            name='text',
            field=wagtail.wagtailcore.fields.StreamField((('paragraph', core.blocks.ParagraphBlock()), ('image', wagtail.wagtailcore.blocks.StructBlock((('image', wagtail.wagtailimages.blocks.ImageChooserBlock(label='Bild')), ('caption', wagtail.wagtailcore.blocks.CharBlock(label='opt. Beschrift.', required=False)), ('size', wagtail.wagtailcore.blocks.ChoiceBlock(choices=[('text-width', 'Text-Breite'), ('over-text-width', 'Über-Text-Breite'), ('screen-width', 'Bildchirm-Breite')]))))), ('embed', wagtail.wagtailcore.blocks.StructBlock((('embed', wagtail.wagtailembeds.blocks.EmbedBlock(help_text='von z.B. einem Youtube-Video, Facebook-Post, Instagram-Bild, …', label='URL')), ('caption', wagtail.wagtailcore.blocks.CharBlock(label='opt. Beschrift.', required=False)), ('size', wagtail.wagtailcore.blocks.ChoiceBlock(choices=[('text-width', 'Text-Breite'), ('over-text-width', 'Über-Text-Breite'), ('screen-width', 'Bildchirm-Breite')], default='text-width'))))), ('button', wagtail.wagtailcore.blocks.StructBlock((('text', wagtail.wagtailcore.blocks.CharBlock(label='Text')), ('link', wagtail.wagtailcore.blocks.URLBlock(label='Link')), ('color', wagtail.wagtailcore.blocks.ChoiceBlock(choices=[('green', 'Grün'), ('red', 'Rot'), ('blue', 'Blau'), ('orange', 'Orange')], default='green', label='Farbe'))))), ('attachment', core.blocks.Attachment()), ('table', wagtail.contrib.table_block.blocks.TableBlock())), blank=True, verbose_name='Text'),
        ),
        migrations.AlterField(
            model_name='personpage',
            name='text',
            field=wagtail.wagtailcore.fields.StreamField((('paragraph', core.blocks.ParagraphBlock()), ('image', wagtail.wagtailcore.blocks.StructBlock((('image', wagtail.wagtailimages.blocks.ImageChooserBlock(label='Bild')), ('caption', wagtail.wagtailcore.blocks.CharBlock(label='opt. Beschrift.', required=False)), ('size', wagtail.wagtailcore.blocks.ChoiceBlock(choices=[('text-width', 'Text-Breite'), ('over-text-width', 'Über-Text-Breite'), ('screen-width', 'Bildchirm-Breite')]))))), ('embed', wagtail.wagtailcore.blocks.StructBlock((('embed', wagtail.wagtailembeds.blocks.EmbedBlock(help_text='von z.B. einem Youtube-Video, Facebook-Post, Instagram-Bild, …', label='URL')), ('caption', wagtail.wagtailcore.blocks.CharBlock(label='opt. Beschrift.', required=False)), ('size', wagtail.wagtailcore.blocks.ChoiceBlock(choices=[('text-width', 'Text-Breite'), ('over-text-width', 'Über-Text-Breite'), ('screen-width', 'Bildchirm-Breite')], default='text-width'))))), ('button', wagtail.wagtailcore.blocks.StructBlock((('text', wagtail.wagtailcore.blocks.CharBlock(label='Text')), ('link', wagtail.wagtailcore.blocks.URLBlock(label='Link')), ('color', wagtail.wagtailcore.blocks.ChoiceBlock(choices=[('green', 'Grün'), ('red', 'Rot'), ('blue', 'Blau'), ('orange', 'Orange')], default='green', label='Farbe'))))), ('attachment', core.blocks.Attachment()), ('table', wagtail.contrib.table_block.blocks.TableBlock())), blank=True, verbose_name='Text'),
        ),
    ]