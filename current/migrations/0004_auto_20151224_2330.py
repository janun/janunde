# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import wagtail.wagtailcore.blocks
import django.db.models.deletion
import wagtail.wagtailimages.blocks
import wagtail.wagtailcore.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0008_image_created_at_index'),
        ('current', '0003_article_highlight'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='article',
            options={'verbose_name': 'article', 'verbose_name_plural': 'articles'},
        ),
        migrations.AlterModelOptions(
            name='current',
            options={'verbose_name': 'current'},
        ),
        migrations.AddField(
            model_name='article',
            name='main_image',
            field=models.ForeignKey(null=True, blank=True, on_delete=django.db.models.deletion.SET_NULL, to='wagtailimages.Image', verbose_name='Main Image', help_text='Optional main image shown at the top', related_name='+'),
        ),
        migrations.AlterField(
            model_name='article',
            name='body',
            field=wagtail.wagtailcore.fields.StreamField((('paragraph', wagtail.wagtailcore.blocks.RichTextBlock()), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock())), blank=True, help_text='body'),
        ),
        migrations.AlterField(
            model_name='article',
            name='highlight',
            field=models.BooleanField(verbose_name='highlight'),
        ),
    ]
