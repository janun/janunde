# Generated by Django 2.2.8 on 2019-12-14 02:38

import core.blocks
from django.db import migrations
import wagtail.contrib.table_block.blocks
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.embeds.blocks
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0025_auto_20180712_1127'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='eventpage',
            name='event_page_tags',
        ),
        migrations.AlterField(
            model_name='eventpage',
            name='content',
            field=wagtail.core.fields.StreamField([('paragraph', core.blocks.ParagraphBlock(features=['h2', 'h3', 'bold', 'italic', 'link', 'ol', 'ul', 'document-link'])), ('image', wagtail.core.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock(label='Bild')), ('caption', wagtail.core.blocks.CharBlock(label='opt. Beschrift.', required=False)), ('size', wagtail.core.blocks.ChoiceBlock(choices=[('text-width', 'Text-Breite'), ('over-text-width', 'Über-Text-Breite'), ('screen-width', 'Bildchirm-Breite')]))])), ('several_images', core.blocks.ImagesBlock(core.blocks.ImageCarouselBlock)), ('gallery', wagtail.core.blocks.StructBlock([('collection', wagtail.core.blocks.ChoiceBlock(choices=core.blocks.get_image_gallery_choices, help_text='Die Bilder aus der Sammlung werden dann als Gallerie angezeigt.', label='Sammlung')), ('start_image', wagtail.images.blocks.ImageChooserBlock(help_text='Das Bild, das als erstes angezeigt wird.', label='erstes Bild', required=False))])), ('embed', wagtail.core.blocks.StructBlock([('embed', wagtail.embeds.blocks.EmbedBlock(help_text='von z.B. einem Youtube-Video, Facebook-Post, Instagram-Bild, …', label='URL')), ('caption', wagtail.core.blocks.CharBlock(label='opt. Beschrift.', required=False)), ('size', wagtail.core.blocks.ChoiceBlock(choices=[('text-width', 'Text-Breite'), ('over-text-width', 'Über-Text-Breite'), ('screen-width', 'Bildchirm-Breite')]))])), ('button', wagtail.core.blocks.StructBlock([('text', wagtail.core.blocks.CharBlock(label='Text')), ('link', wagtail.core.blocks.URLBlock(label='Link', required=False)), ('mail', wagtail.core.blocks.EmailBlock(help_text='wird anstelle von link benutzt', label='E-Mail', required=False)), ('color', wagtail.core.blocks.ChoiceBlock(choices=[('green', 'Grün'), ('red', 'Rot'), ('blue', 'Blau'), ('orange', 'Orange'), ('purple', 'Lila')], label='Farbe')), ('aslink', wagtail.core.blocks.BooleanBlock(label='ohne Hintergrund', required=False))])), ('attachment', core.blocks.Attachment()), ('table', wagtail.contrib.table_block.blocks.TableBlock()), ('map_image', wagtail.core.blocks.StructBlock([('tile_url', wagtail.core.blocks.URLBlock(help_text='URL zu den Kacheln, aus denen das Bild besteht. Benutze {z}, {x}, {y} in der URL für die Koordinaten', label='Kachel-URL', required=True)), ('height', wagtail.core.blocks.DecimalBlock(help_text='in speziellen Leaflet Einheiten', label='Höhe', required=True)), ('width', wagtail.core.blocks.DecimalBlock(help_text='in speziellen Leaflet Einheiten', label='Breite', required=True)), ('attribution', wagtail.core.blocks.CharBlock(help_text='Wird unten rechts im Bild angezeigt.', label='Urheber', required=False))])), ('iframe', wagtail.core.blocks.StructBlock([('url', wagtail.core.blocks.URLBlock(help_text='URL zu der Website, die mittels Iframe eingebunden werden soll.', label='URL', required=True)), ('allowFullScreen', wagtail.core.blocks.BooleanBlock(label='Vollbild erlauben?', required=False)), ('height', wagtail.core.blocks.DecimalBlock(default='1000', help_text='in px', label='Höhe')), ('width', wagtail.core.blocks.DecimalBlock(default='1000', help_text='in px', label='Breite'))])), ('video_link', wagtail.core.blocks.StructBlock([('url', wagtail.core.blocks.URLBlock(help_text='URL zu dem Video, auf das verlinkt wird', label='URL', required=True)), ('image', wagtail.images.blocks.ImageChooserBlock(label='Bild (schwarz wenn nichts angegeben)', required=False)), ('caption', wagtail.core.blocks.CharBlock(label='Bild-Unterschrift', required=False))]))], blank=True, verbose_name='Inhalt'),
        ),
        migrations.AlterField(
            model_name='seminarformpage',
            name='description',
            field=wagtail.core.fields.StreamField([('paragraph', core.blocks.ParagraphBlock(features=['h2', 'h3', 'bold', 'italic', 'link', 'ol', 'ul', 'document-link'])), ('image', wagtail.core.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock(label='Bild')), ('caption', wagtail.core.blocks.CharBlock(label='opt. Beschrift.', required=False)), ('size', wagtail.core.blocks.ChoiceBlock(choices=[('text-width', 'Text-Breite'), ('over-text-width', 'Über-Text-Breite'), ('screen-width', 'Bildchirm-Breite')]))])), ('several_images', core.blocks.ImagesBlock(core.blocks.ImageCarouselBlock)), ('gallery', wagtail.core.blocks.StructBlock([('collection', wagtail.core.blocks.ChoiceBlock(choices=core.blocks.get_image_gallery_choices, help_text='Die Bilder aus der Sammlung werden dann als Gallerie angezeigt.', label='Sammlung')), ('start_image', wagtail.images.blocks.ImageChooserBlock(help_text='Das Bild, das als erstes angezeigt wird.', label='erstes Bild', required=False))])), ('embed', wagtail.core.blocks.StructBlock([('embed', wagtail.embeds.blocks.EmbedBlock(help_text='von z.B. einem Youtube-Video, Facebook-Post, Instagram-Bild, …', label='URL')), ('caption', wagtail.core.blocks.CharBlock(label='opt. Beschrift.', required=False)), ('size', wagtail.core.blocks.ChoiceBlock(choices=[('text-width', 'Text-Breite'), ('over-text-width', 'Über-Text-Breite'), ('screen-width', 'Bildchirm-Breite')]))])), ('button', wagtail.core.blocks.StructBlock([('text', wagtail.core.blocks.CharBlock(label='Text')), ('link', wagtail.core.blocks.URLBlock(label='Link', required=False)), ('mail', wagtail.core.blocks.EmailBlock(help_text='wird anstelle von link benutzt', label='E-Mail', required=False)), ('color', wagtail.core.blocks.ChoiceBlock(choices=[('green', 'Grün'), ('red', 'Rot'), ('blue', 'Blau'), ('orange', 'Orange'), ('purple', 'Lila')], label='Farbe')), ('aslink', wagtail.core.blocks.BooleanBlock(label='ohne Hintergrund', required=False))])), ('attachment', core.blocks.Attachment()), ('table', wagtail.contrib.table_block.blocks.TableBlock()), ('map_image', wagtail.core.blocks.StructBlock([('tile_url', wagtail.core.blocks.URLBlock(help_text='URL zu den Kacheln, aus denen das Bild besteht. Benutze {z}, {x}, {y} in der URL für die Koordinaten', label='Kachel-URL', required=True)), ('height', wagtail.core.blocks.DecimalBlock(help_text='in speziellen Leaflet Einheiten', label='Höhe', required=True)), ('width', wagtail.core.blocks.DecimalBlock(help_text='in speziellen Leaflet Einheiten', label='Breite', required=True)), ('attribution', wagtail.core.blocks.CharBlock(help_text='Wird unten rechts im Bild angezeigt.', label='Urheber', required=False))])), ('iframe', wagtail.core.blocks.StructBlock([('url', wagtail.core.blocks.URLBlock(help_text='URL zu der Website, die mittels Iframe eingebunden werden soll.', label='URL', required=True)), ('allowFullScreen', wagtail.core.blocks.BooleanBlock(label='Vollbild erlauben?', required=False)), ('height', wagtail.core.blocks.DecimalBlock(default='1000', help_text='in px', label='Höhe')), ('width', wagtail.core.blocks.DecimalBlock(default='1000', help_text='in px', label='Breite'))])), ('video_link', wagtail.core.blocks.StructBlock([('url', wagtail.core.blocks.URLBlock(help_text='URL zu dem Video, auf das verlinkt wird', label='URL', required=True)), ('image', wagtail.images.blocks.ImageChooserBlock(label='Bild (schwarz wenn nichts angegeben)', required=False)), ('caption', wagtail.core.blocks.CharBlock(label='Bild-Unterschrift', required=False))]))], blank=True, verbose_name='Erklärung'),
        ),
    ]
