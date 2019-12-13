# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-04-15 14:41
from __future__ import unicode_literals

import core.blocks
from django.db import migrations, models
import django.db.models.deletion
import wagtail.core.blocks
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0028_merge'),
        ('core', '0007_auto_20160404_1427'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='eventpage',
            name='highlight',
        ),
        migrations.RemoveField(
            model_name='eventpage',
            name='standardpage_ptr',
        ),
        migrations.AddField(
            model_name='eventpage',
            name='contact_mail',
            field=models.EmailField(blank=True, help_text='Die E-Mail-Adresse, um Kontakt für diese Veranstaltung aufzunehmen', max_length=254, null=True, verbose_name='Kontakt E-Mail'),
        ),
        migrations.AddField(
            model_name='eventpage',
            name='content',
            field=wagtail.core.fields.StreamField((('paragraph', wagtail.core.blocks.RichTextBlock(icon='pilcrow', label='Absatz')), ('image', core.blocks.ImageBlock()), ('embedded_video', core.blocks.EmbedBlock())), blank=True, verbose_name='Inhalt'),
        ),
        migrations.AddField(
            model_name='eventpage',
            name='facebook_event_url',
            field=models.URLField(blank=True, help_text='Die URL zum Facebook-Event dieser Veranstaltung', null=True, verbose_name='Facebook Event'),
        ),
        migrations.AddField(
            model_name='eventpage',
            name='page_ptr',
            field=models.OneToOneField(auto_created=True, default=1, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='eventpage',
            name='related_group',
            field=models.ForeignKey(blank=True, help_text='Eine JANUN-Gruppe, die dieser Veranstaltung zugeordnet ist', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='event_pages', to='core.Group', verbose_name='Zugehörige Gruppe'),
        ),
        migrations.AddField(
            model_name='eventpage',
            name='website_url',
            field=models.URLField(blank=True, help_text='Die URL einer externen Website zu dieser Veranstaltung', null=True, verbose_name='externe Website'),
        ),
        migrations.AlterField(
            model_name='article',
            name='related_group',
            field=models.ForeignKey(blank=True, help_text='Eine JANUN-Gruppe, die diesem Artikel zugeordnet ist', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='articles', to='core.Group', verbose_name='Zugehörige Gruppe'),
        ),
        migrations.AlterField(
            model_name='eventpage',
            name='main_image',
            field=models.ForeignKey(blank=True, help_text='Poster oder Bild für diese Veranstaltung.Bitte kein Gruppen- oder JANUN-Logo!', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='core.AttributedImage', verbose_name='Poster'),
        ),
    ]
