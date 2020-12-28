# Generated by Django 2.2.17 on 2020-12-28 22:20

import core.blocks
from django.db import migrations
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('wimmelbilder', '0017_auto_20201225_2141'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wimmelbildpage',
            name='after',
            field=wagtail.core.fields.StreamField([('paragraph', core.blocks.ParagraphBlock(features=['h2', 'h3', 'bold', 'italic', 'link', 'ol', 'ul', 'document-link', 'anchor-identifier'])), ('image', wagtail.core.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock(label='Bild')), ('caption', wagtail.core.blocks.CharBlock(label='Bildunterschrift', required=False)), ('size', wagtail.core.blocks.ChoiceBlock(choices=[('text-width', 'Text-Breite'), ('over-text-width', 'Über-Text-Breite')]))])), ('several_images', core.blocks.ImagesBlock(core.blocks.ImageCarouselBlock)), ('gallery', wagtail.core.blocks.StructBlock([('collection', wagtail.core.blocks.ChoiceBlock(choices=core.blocks.get_image_gallery_choices, help_text='Die Bilder aus der Sammlung werden dann als Gallerie angezeigt.', label='Sammlung')), ('start_image', wagtail.images.blocks.ImageChooserBlock(help_text='Das Bild, das als erstes angezeigt wird.', label='erstes Bild', required=False))])), ('button', wagtail.core.blocks.StructBlock([('text', wagtail.core.blocks.CharBlock(label='Text')), ('link', wagtail.core.blocks.CharBlock(help_text='Schreibe https://example.com für einen externen Link, /unterseite für einen internen, #sektion für einen Anchor-Link, mailto:max@muster.de für eine E-Mail-Adresse, tel:+49123121 für eine Telefonnummer etc.', label='Link', required=False))])), ('attachment', core.blocks.Attachment()), ('iframe', wagtail.core.blocks.StructBlock([('url', wagtail.core.blocks.URLBlock(help_text='URL zu der Website, die mittels Iframe eingebunden werden soll.', label='URL', required=True)), ('allowFullScreen', wagtail.core.blocks.BooleanBlock(label='Vollbild erlauben?', required=False)), ('height', wagtail.core.blocks.DecimalBlock(default='1000', help_text='in px', label='Höhe')), ('width', wagtail.core.blocks.DecimalBlock(default='1000', help_text='in px', label='Breite'))])), ('video_link', wagtail.core.blocks.StructBlock([('url', wagtail.core.blocks.URLBlock(help_text='URL zu dem Video, auf das verlinkt wird', label='URL', required=True)), ('image', wagtail.images.blocks.ImageChooserBlock(label='Bild (schwarz wenn nichts angegeben)', required=False)), ('caption', wagtail.core.blocks.CharBlock(label='Bild-Unterschrift', required=False))])), ('media', core.blocks.MediaUploadBlock())], blank=True, null=True, verbose_name='Nach dem Wimmelbild'),
        ),
        migrations.AlterField(
            model_name='wimmelbildpage',
            name='before',
            field=wagtail.core.fields.StreamField([('paragraph', core.blocks.ParagraphBlock(features=['h2', 'h3', 'bold', 'italic', 'link', 'ol', 'ul', 'document-link', 'anchor-identifier'])), ('image', wagtail.core.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock(label='Bild')), ('caption', wagtail.core.blocks.CharBlock(label='Bildunterschrift', required=False)), ('size', wagtail.core.blocks.ChoiceBlock(choices=[('text-width', 'Text-Breite'), ('over-text-width', 'Über-Text-Breite')]))])), ('several_images', core.blocks.ImagesBlock(core.blocks.ImageCarouselBlock)), ('gallery', wagtail.core.blocks.StructBlock([('collection', wagtail.core.blocks.ChoiceBlock(choices=core.blocks.get_image_gallery_choices, help_text='Die Bilder aus der Sammlung werden dann als Gallerie angezeigt.', label='Sammlung')), ('start_image', wagtail.images.blocks.ImageChooserBlock(help_text='Das Bild, das als erstes angezeigt wird.', label='erstes Bild', required=False))])), ('button', wagtail.core.blocks.StructBlock([('text', wagtail.core.blocks.CharBlock(label='Text')), ('link', wagtail.core.blocks.CharBlock(help_text='Schreibe https://example.com für einen externen Link, /unterseite für einen internen, #sektion für einen Anchor-Link, mailto:max@muster.de für eine E-Mail-Adresse, tel:+49123121 für eine Telefonnummer etc.', label='Link', required=False))])), ('attachment', core.blocks.Attachment()), ('iframe', wagtail.core.blocks.StructBlock([('url', wagtail.core.blocks.URLBlock(help_text='URL zu der Website, die mittels Iframe eingebunden werden soll.', label='URL', required=True)), ('allowFullScreen', wagtail.core.blocks.BooleanBlock(label='Vollbild erlauben?', required=False)), ('height', wagtail.core.blocks.DecimalBlock(default='1000', help_text='in px', label='Höhe')), ('width', wagtail.core.blocks.DecimalBlock(default='1000', help_text='in px', label='Breite'))])), ('video_link', wagtail.core.blocks.StructBlock([('url', wagtail.core.blocks.URLBlock(help_text='URL zu dem Video, auf das verlinkt wird', label='URL', required=True)), ('image', wagtail.images.blocks.ImageChooserBlock(label='Bild (schwarz wenn nichts angegeben)', required=False)), ('caption', wagtail.core.blocks.CharBlock(label='Bild-Unterschrift', required=False))])), ('media', core.blocks.MediaUploadBlock())], blank=True, null=True, verbose_name='Vor dem Wimmelbild'),
        ),
    ]
