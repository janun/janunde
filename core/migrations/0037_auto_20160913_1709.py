# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-13 15:09
from __future__ import unicode_literals

import core.blocks
from django.db import migrations, models
import django.db.models.deletion
import wagtail.contrib.table_block.blocks
import wagtail.wagtailcore.blocks
import wagtail.wagtailcore.fields
import wagtail.wagtailembeds.blocks
import wagtail.wagtailimages.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0036_auto_20160912_1623'),
        ('contact', '0006_auto_20160913_1709'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attributedimage',
            name='attribution',
            field=models.CharField(max_length=255, verbose_name='Quellenangabe'),
        ),
        migrations.AlterField(
            model_name='standardpage',
            name='author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='pages', to='contact.PersonPage', verbose_name='Autor_in'),
        ),
        migrations.AlterField(
            model_name='standardpage',
            name='body',
            field=wagtail.wagtailcore.fields.StreamField((('h2', wagtail.wagtailcore.blocks.StructBlock((('title', wagtail.wagtailcore.blocks.CharBlock(label='Titel')), ('color', wagtail.wagtailcore.blocks.ChoiceBlock(choices=[('brown', 'Braun'), ('green', 'Grün'), ('red', 'Rot'), ('blue', 'Blau'), ('orange', 'Orange')], default='brown', label='Farbe')), ('bold', wagtail.wagtailcore.blocks.BooleanBlock(help_text='Für eine große und fette Überschrift', label='Fett', required=False))))), ('paragraph', core.blocks.ParagraphBlock()), ('image', wagtail.wagtailcore.blocks.StructBlock((('image', wagtail.wagtailimages.blocks.ImageChooserBlock(label='Bild')), ('caption', wagtail.wagtailcore.blocks.CharBlock(label='Bildunterschrift', required=False)), ('full_width', wagtail.wagtailcore.blocks.BooleanBlock(help_text='Soll das Bild auf voller Breite des Bildschirms angezeigt werden?', label='volle Breite', required=False))))), ('embedded_video', wagtail.wagtailcore.blocks.StructBlock((('embed', wagtail.wagtailembeds.blocks.EmbedBlock('Video-URL', help_text='URL von z.B. Youtube oder Vimeo hier reinkopieren')), ('caption', wagtail.wagtailcore.blocks.CharBlock(label='Bildunterschrift', required=False))))), ('button', wagtail.wagtailcore.blocks.StructBlock((('text', wagtail.wagtailcore.blocks.CharBlock(label='Text')), ('link', wagtail.wagtailcore.blocks.URLBlock(label='Link')), ('color', wagtail.wagtailcore.blocks.ChoiceBlock(choices=[('brown', 'Braun'), ('green', 'Grün'), ('red', 'Rot'), ('blue', 'Blau'), ('orange', 'Orange')], default='green', label='Farbe'))))), ('attachment', core.blocks.Attachment()), ('sticker', wagtail.wagtailcore.blocks.StructBlock((('title', wagtail.wagtailcore.blocks.CharBlock(label='Text')), ('color', wagtail.wagtailcore.blocks.ChoiceBlock(choices=[('brown', 'Braun'), ('green', 'Grün'), ('red', 'Rot'), ('blue', 'Blau'), ('orange', 'Orange')], default='green', label='Farbe')), ('link', wagtail.wagtailcore.blocks.URLBlock(label='Link'))))), ('table', wagtail.contrib.table_block.blocks.TableBlock())), blank=True, verbose_name='Inhalt'),
        ),
        migrations.AlterField(
            model_name='thema',
            name='body',
            field=wagtail.wagtailcore.fields.StreamField((('h2', wagtail.wagtailcore.blocks.StructBlock((('title', wagtail.wagtailcore.blocks.CharBlock(label='Titel')), ('color', wagtail.wagtailcore.blocks.ChoiceBlock(choices=[('brown', 'Braun'), ('green', 'Grün'), ('red', 'Rot'), ('blue', 'Blau'), ('orange', 'Orange')], default='brown', label='Farbe')), ('bold', wagtail.wagtailcore.blocks.BooleanBlock(help_text='Für eine große und fette Überschrift', label='Fett', required=False))))), ('paragraph', core.blocks.ParagraphBlock()), ('image', wagtail.wagtailcore.blocks.StructBlock((('image', wagtail.wagtailimages.blocks.ImageChooserBlock(label='Bild')), ('caption', wagtail.wagtailcore.blocks.CharBlock(label='Bildunterschrift', required=False)), ('full_width', wagtail.wagtailcore.blocks.BooleanBlock(help_text='Soll das Bild auf voller Breite des Bildschirms angezeigt werden?', label='volle Breite', required=False))))), ('embedded_video', wagtail.wagtailcore.blocks.StructBlock((('embed', wagtail.wagtailembeds.blocks.EmbedBlock('Video-URL', help_text='URL von z.B. Youtube oder Vimeo hier reinkopieren')), ('caption', wagtail.wagtailcore.blocks.CharBlock(label='Bildunterschrift', required=False))))), ('button', wagtail.wagtailcore.blocks.StructBlock((('text', wagtail.wagtailcore.blocks.CharBlock(label='Text')), ('link', wagtail.wagtailcore.blocks.URLBlock(label='Link')), ('color', wagtail.wagtailcore.blocks.ChoiceBlock(choices=[('brown', 'Braun'), ('green', 'Grün'), ('red', 'Rot'), ('blue', 'Blau'), ('orange', 'Orange')], default='green', label='Farbe'))))), ('attachment', core.blocks.Attachment()), ('sticker', wagtail.wagtailcore.blocks.StructBlock((('title', wagtail.wagtailcore.blocks.CharBlock(label='Text')), ('color', wagtail.wagtailcore.blocks.ChoiceBlock(choices=[('brown', 'Braun'), ('green', 'Grün'), ('red', 'Rot'), ('blue', 'Blau'), ('orange', 'Orange')], default='green', label='Farbe')), ('link', wagtail.wagtailcore.blocks.URLBlock(label='Link'))))), ('table', wagtail.contrib.table_block.blocks.TableBlock())), blank=True, verbose_name='Beschreibung'),
        ),
    ]
