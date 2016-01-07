# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import wagtail.wagtailimages.blocks
import wagtail.wagtailcore.fields
import django.db.models.deletion
import wagtail.wagtailcore.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('current', '0005_auto_20151228_1421'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='article',
            options={'verbose_name': 'Artikel', 'verbose_name_plural': 'Artikel'},
        ),
        migrations.AlterModelOptions(
            name='current',
            options={'verbose_name': 'Aktuelles'},
        ),
        migrations.AlterField(
            model_name='article',
            name='body',
            field=wagtail.wagtailcore.fields.StreamField((('paragraph', wagtail.wagtailcore.blocks.RichTextBlock()), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock())), help_text='Inhalt des Artikels', blank=True),
        ),
        migrations.AlterField(
            model_name='article',
            name='highlight',
            field=models.BooleanField(verbose_name='Highlight', help_text='Falls ja, taucht es z.B. auf der Startseite auf.'),
        ),
        migrations.AlterField(
            model_name='article',
            name='main_image',
            field=models.ForeignKey(verbose_name='Hauptbild', blank=True, null=True, related_name='+', on_delete=django.db.models.deletion.SET_NULL, help_text='Bild, das den Artikel repräsentiert. Wird in Übersichten verwendet.', to='wagtailimages.Image'),
        ),
    ]
