# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-25 14:18
from __future__ import unicode_literals

import core.blocks
from django.db import migrations
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventpage',
            name='content',
            field=wagtail.core.fields.StreamField((('title', wagtail.core.blocks.StructBlock((('title', wagtail.core.blocks.CharBlock(classname='title', label='Titel')), ('color', wagtail.core.blocks.ChoiceBlock(choices=[('brown', 'Braun'), ('green', 'Grün'), ('red', 'Rot'), ('blue', 'Blau'), ('orange', 'Orange')], classname='', default='brown', label='Farbe'))))), ('paragraph', wagtail.core.blocks.RichTextBlock(icon='pilcrow', label='Absatz')), ('image', wagtail.core.blocks.StructBlock((('image', wagtail.images.blocks.ImageChooserBlock(label='Bild')), ('caption', wagtail.core.blocks.CharBlock(label='Bildunterschrift', required=False))))), ('embedded_video', core.blocks.EmbedBlock())), blank=True, verbose_name='Inhalt'),
        ),
    ]
