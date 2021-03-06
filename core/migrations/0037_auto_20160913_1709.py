# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-13 15:09
from __future__ import unicode_literals

import core.blocks
from django.db import migrations, models
import django.db.models.deletion
import wagtail.contrib.table_block.blocks
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.embeds.blocks
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0036_auto_20160912_1623"),
        ('contact', '0006_auto_20160913_1709'),
    ]

    operations = [
        migrations.AlterField(
            model_name="attributedimage",
            name="attribution",
            field=models.CharField(max_length=255, verbose_name="Quellenangabe"),
        ),
        migrations.AlterField(
            model_name="standardpage",
            name="author",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="pages",
                to="contact.PersonPage",
                verbose_name="Autor_in",
            ),
        ),
        migrations.AlterField(
            model_name="standardpage",
            name="body",
            field=wagtail.core.fields.StreamField(
                (
                    (
                        "h2",
                        wagtail.core.blocks.StructBlock(
                            (
                                ("title", wagtail.core.blocks.CharBlock(label="Titel")),
                                (
                                    "color",
                                    wagtail.core.blocks.ChoiceBlock(
                                        choices=[
                                            ("brown", "Braun"),
                                            ("green", "Grün"),
                                            ("red", "Rot"),
                                            ("blue", "Blau"),
                                            ("orange", "Orange"),
                                        ],
                                        default="brown",
                                        label="Farbe",
                                    ),
                                ),
                                (
                                    "bold",
                                    wagtail.core.blocks.BooleanBlock(
                                        help_text="Für eine große und fette Überschrift",
                                        label="Fett",
                                        required=False,
                                    ),
                                ),
                            )
                        ),
                    ),
                    ("paragraph", core.blocks.ParagraphBlock()),
                    (
                        "image",
                        wagtail.core.blocks.StructBlock(
                            (
                                (
                                    "image",
                                    wagtail.images.blocks.ImageChooserBlock(
                                        label="Bild"
                                    ),
                                ),
                                (
                                    "caption",
                                    wagtail.core.blocks.CharBlock(
                                        label="Bildunterschrift", required=False
                                    ),
                                ),
                                (
                                    "full_width",
                                    wagtail.core.blocks.BooleanBlock(
                                        help_text="Soll das Bild auf voller Breite des Bildschirms angezeigt werden?",
                                        label="volle Breite",
                                        required=False,
                                    ),
                                ),
                            )
                        ),
                    ),
                    (
                        "embedded_video",
                        wagtail.core.blocks.StructBlock(
                            (
                                (
                                    "embed",
                                    wagtail.embeds.blocks.EmbedBlock(
                                        "Video-URL",
                                        help_text="URL von z.B. Youtube oder Vimeo hier reinkopieren",
                                    ),
                                ),
                                (
                                    "caption",
                                    wagtail.core.blocks.CharBlock(
                                        label="Bildunterschrift", required=False
                                    ),
                                ),
                            )
                        ),
                    ),
                    (
                        "button",
                        wagtail.core.blocks.StructBlock(
                            (
                                ("text", wagtail.core.blocks.CharBlock(label="Text")),
                                ("link", wagtail.core.blocks.URLBlock(label="Link")),
                                (
                                    "color",
                                    wagtail.core.blocks.ChoiceBlock(
                                        choices=[
                                            ("brown", "Braun"),
                                            ("green", "Grün"),
                                            ("red", "Rot"),
                                            ("blue", "Blau"),
                                            ("orange", "Orange"),
                                        ],
                                        default="green",
                                        label="Farbe",
                                    ),
                                ),
                            )
                        ),
                    ),
                    ("attachment", core.blocks.Attachment()),
                    (
                        "sticker",
                        wagtail.core.blocks.StructBlock(
                            (
                                ("title", wagtail.core.blocks.CharBlock(label="Text")),
                                (
                                    "color",
                                    wagtail.core.blocks.ChoiceBlock(
                                        choices=[
                                            ("brown", "Braun"),
                                            ("green", "Grün"),
                                            ("red", "Rot"),
                                            ("blue", "Blau"),
                                            ("orange", "Orange"),
                                        ],
                                        default="green",
                                        label="Farbe",
                                    ),
                                ),
                                ("link", wagtail.core.blocks.URLBlock(label="Link")),
                            )
                        ),
                    ),
                    ("table", wagtail.contrib.table_block.blocks.TableBlock()),
                ),
                blank=True,
                verbose_name="Inhalt",
            ),
        ),
        migrations.AlterField(
            model_name="thema",
            name="body",
            field=wagtail.core.fields.StreamField(
                (
                    (
                        "h2",
                        wagtail.core.blocks.StructBlock(
                            (
                                ("title", wagtail.core.blocks.CharBlock(label="Titel")),
                                (
                                    "color",
                                    wagtail.core.blocks.ChoiceBlock(
                                        choices=[
                                            ("brown", "Braun"),
                                            ("green", "Grün"),
                                            ("red", "Rot"),
                                            ("blue", "Blau"),
                                            ("orange", "Orange"),
                                        ],
                                        default="brown",
                                        label="Farbe",
                                    ),
                                ),
                                (
                                    "bold",
                                    wagtail.core.blocks.BooleanBlock(
                                        help_text="Für eine große und fette Überschrift",
                                        label="Fett",
                                        required=False,
                                    ),
                                ),
                            )
                        ),
                    ),
                    ("paragraph", core.blocks.ParagraphBlock()),
                    (
                        "image",
                        wagtail.core.blocks.StructBlock(
                            (
                                (
                                    "image",
                                    wagtail.images.blocks.ImageChooserBlock(
                                        label="Bild"
                                    ),
                                ),
                                (
                                    "caption",
                                    wagtail.core.blocks.CharBlock(
                                        label="Bildunterschrift", required=False
                                    ),
                                ),
                                (
                                    "full_width",
                                    wagtail.core.blocks.BooleanBlock(
                                        help_text="Soll das Bild auf voller Breite des Bildschirms angezeigt werden?",
                                        label="volle Breite",
                                        required=False,
                                    ),
                                ),
                            )
                        ),
                    ),
                    (
                        "embedded_video",
                        wagtail.core.blocks.StructBlock(
                            (
                                (
                                    "embed",
                                    wagtail.embeds.blocks.EmbedBlock(
                                        "Video-URL",
                                        help_text="URL von z.B. Youtube oder Vimeo hier reinkopieren",
                                    ),
                                ),
                                (
                                    "caption",
                                    wagtail.core.blocks.CharBlock(
                                        label="Bildunterschrift", required=False
                                    ),
                                ),
                            )
                        ),
                    ),
                    (
                        "button",
                        wagtail.core.blocks.StructBlock(
                            (
                                ("text", wagtail.core.blocks.CharBlock(label="Text")),
                                ("link", wagtail.core.blocks.URLBlock(label="Link")),
                                (
                                    "color",
                                    wagtail.core.blocks.ChoiceBlock(
                                        choices=[
                                            ("brown", "Braun"),
                                            ("green", "Grün"),
                                            ("red", "Rot"),
                                            ("blue", "Blau"),
                                            ("orange", "Orange"),
                                        ],
                                        default="green",
                                        label="Farbe",
                                    ),
                                ),
                            )
                        ),
                    ),
                    ("attachment", core.blocks.Attachment()),
                    (
                        "sticker",
                        wagtail.core.blocks.StructBlock(
                            (
                                ("title", wagtail.core.blocks.CharBlock(label="Text")),
                                (
                                    "color",
                                    wagtail.core.blocks.ChoiceBlock(
                                        choices=[
                                            ("brown", "Braun"),
                                            ("green", "Grün"),
                                            ("red", "Rot"),
                                            ("blue", "Blau"),
                                            ("orange", "Orange"),
                                        ],
                                        default="green",
                                        label="Farbe",
                                    ),
                                ),
                                ("link", wagtail.core.blocks.URLBlock(label="Link")),
                            )
                        ),
                    ),
                    ("table", wagtail.contrib.table_block.blocks.TableBlock()),
                ),
                blank=True,
                verbose_name="Beschreibung",
            ),
        ),
    ]
