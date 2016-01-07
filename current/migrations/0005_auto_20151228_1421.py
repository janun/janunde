# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import wagtail.wagtailimages.blocks
import wagtail.wagtailcore.fields
import django.db.models.deletion
import wagtail.wagtailcore.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('current', '0004_auto_20151224_2330'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='body',
            field=wagtail.wagtailcore.fields.StreamField((('paragraph', wagtail.wagtailcore.blocks.RichTextBlock()), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock())), help_text='Content of the article', blank=True),
        ),
        migrations.AlterField(
            model_name='article',
            name='highlight',
            field=models.BooleanField(verbose_name='highlight', help_text='Wether this is a highlighted article'),
        ),
        migrations.AlterField(
            model_name='article',
            name='main_image',
            field=models.ForeignKey(help_text='Image representing this article in lists. Upload best resolution possible; Will be resized.', on_delete=django.db.models.deletion.SET_NULL, blank=True, related_name='+', verbose_name='Main Image', to='wagtailimages.Image', null=True),
        ),
    ]
