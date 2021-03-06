# Generated by Django 2.2.12 on 2020-04-05 14:52

from django.db import migrations, models, connection
import django.db.models.deletion
import wagtail.contrib.table_block.blocks
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.embeds.blocks
import wagtail.images.blocks
import core.blocks


def author_id_exists():
    """checks if author_id already exists"""
    try:
        cursor = connection.cursor()
        if not cursor:
            raise Exception
        table = connection.introspection.get_table_description(cursor, "core_article")
    except:
        raise Exception("unable to determine if the table '%s' exists" % table)
    return "author_id" in [info.name for info in table]


def add_article_author(apps, schema_editor):
    """Add author_id only if non-existent"""
    if not author_id_exists():
        migrations.AddField(
            model_name="article",
            name="author",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="pages",
                to="contact.PersonPage",
                verbose_name="Autor_in",
            ),
        )


class Migration(migrations.Migration):

    dependencies = [
        ("contact", "0021_auto_20200405_1652"),
        ("core", "0082_auto_20200116_1740"),
    ]

    operations = [
        migrations.RunPython(add_article_author),
        migrations.AlterField(
            model_name="group",
            name="body",
            field=wagtail.core.fields.StreamField(
                [
                    (
                        "paragraph",
                        core.blocks.ParagraphBlock(
                            features=[
                                "h2",
                                "h3",
                                "bold",
                                "italic",
                                "link",
                                "ol",
                                "ul",
                                "document-link",
                                "anchor-identifier",
                            ]
                        ),
                    ),
                    (
                        "image",
                        wagtail.core.blocks.StructBlock(
                            [
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
                                    "size",
                                    wagtail.core.blocks.ChoiceBlock(
                                        choices=[
                                            ("text-width", "Text-Breite"),
                                            ("over-text-width", "Über-Text-Breite"),
                                        ]
                                    ),
                                ),
                            ]
                        ),
                    ),
                    (
                        "several_images",
                        core.blocks.ImagesBlock(core.blocks.ImageCarouselBlock),
                    ),
                    (
                        "gallery",
                        wagtail.core.blocks.StructBlock(
                            [
                                (
                                    "collection",
                                    wagtail.core.blocks.ChoiceBlock(
                                        choices=core.blocks.get_image_gallery_choices,
                                        help_text="Die Bilder aus der Sammlung werden dann als Gallerie angezeigt.",
                                        label="Sammlung",
                                    ),
                                ),
                                (
                                    "start_image",
                                    wagtail.images.blocks.ImageChooserBlock(
                                        help_text="Das Bild, das als erstes angezeigt wird.",
                                        label="erstes Bild",
                                        required=False,
                                    ),
                                ),
                            ]
                        ),
                    ),
                    (
                        "embed",
                        wagtail.core.blocks.StructBlock(
                            [
                                (
                                    "embed",
                                    wagtail.embeds.blocks.EmbedBlock(
                                        help_text="von z.B. einem Youtube-Video, Facebook-Post, Instagram-Bild, …",
                                        label="URL",
                                    ),
                                ),
                                (
                                    "caption",
                                    wagtail.core.blocks.CharBlock(
                                        label="opt. Beschrift.", required=False
                                    ),
                                ),
                                (
                                    "size",
                                    wagtail.core.blocks.ChoiceBlock(
                                        choices=[
                                            ("text-width", "Text-Breite"),
                                            ("over-text-width", "Über-Text-Breite"),
                                        ]
                                    ),
                                ),
                            ]
                        ),
                    ),
                    (
                        "button",
                        wagtail.core.blocks.StructBlock(
                            [
                                ("text", wagtail.core.blocks.CharBlock(label="Text")),
                                (
                                    "link",
                                    wagtail.core.blocks.URLBlock(
                                        label="Link", required=False
                                    ),
                                ),
                                (
                                    "mail",
                                    wagtail.core.blocks.EmailBlock(
                                        help_text="wird anstelle von link benutzt",
                                        label="E-Mail",
                                        required=False,
                                    ),
                                ),
                                (
                                    "color",
                                    wagtail.core.blocks.ChoiceBlock(
                                        choices=[
                                            ("green", "Grün"),
                                            ("red", "Rot"),
                                            ("blue", "Blau"),
                                            ("orange", "Orange"),
                                            ("purple", "Lila"),
                                        ],
                                        label="Farbe",
                                    ),
                                ),
                                (
                                    "aslink",
                                    wagtail.core.blocks.BooleanBlock(
                                        label="ohne Hintergrund", required=False
                                    ),
                                ),
                            ]
                        ),
                    ),
                    ("attachment", core.blocks.Attachment()),
                    ("table", wagtail.contrib.table_block.blocks.TableBlock()),
                    (
                        "map_image",
                        wagtail.core.blocks.StructBlock(
                            [
                                (
                                    "tile_url",
                                    wagtail.core.blocks.URLBlock(
                                        help_text="URL zu den Kacheln, aus denen das Bild besteht. Benutze {z}, {x}, {y} in der URL für die Koordinaten",
                                        label="Kachel-URL",
                                        required=True,
                                    ),
                                ),
                                (
                                    "height",
                                    wagtail.core.blocks.DecimalBlock(
                                        help_text="in speziellen Leaflet Einheiten",
                                        label="Höhe",
                                        required=True,
                                    ),
                                ),
                                (
                                    "width",
                                    wagtail.core.blocks.DecimalBlock(
                                        help_text="in speziellen Leaflet Einheiten",
                                        label="Breite",
                                        required=True,
                                    ),
                                ),
                                (
                                    "attribution",
                                    wagtail.core.blocks.CharBlock(
                                        help_text="Wird unten rechts im Bild angezeigt.",
                                        label="Urheber",
                                        required=False,
                                    ),
                                ),
                            ]
                        ),
                    ),
                    (
                        "iframe",
                        wagtail.core.blocks.StructBlock(
                            [
                                (
                                    "url",
                                    wagtail.core.blocks.URLBlock(
                                        help_text="URL zu der Website, die mittels Iframe eingebunden werden soll.",
                                        label="URL",
                                        required=True,
                                    ),
                                ),
                                (
                                    "allowFullScreen",
                                    wagtail.core.blocks.BooleanBlock(
                                        label="Vollbild erlauben?", required=False
                                    ),
                                ),
                                (
                                    "height",
                                    wagtail.core.blocks.DecimalBlock(
                                        default="1000", help_text="in px", label="Höhe"
                                    ),
                                ),
                                (
                                    "width",
                                    wagtail.core.blocks.DecimalBlock(
                                        default="1000",
                                        help_text="in px",
                                        label="Breite",
                                    ),
                                ),
                            ]
                        ),
                    ),
                    (
                        "video_link",
                        wagtail.core.blocks.StructBlock(
                            [
                                (
                                    "url",
                                    wagtail.core.blocks.URLBlock(
                                        help_text="URL zu dem Video, auf das verlinkt wird",
                                        label="URL",
                                        required=True,
                                    ),
                                ),
                                (
                                    "image",
                                    wagtail.images.blocks.ImageChooserBlock(
                                        label="Bild (schwarz wenn nichts angegeben)",
                                        required=False,
                                    ),
                                ),
                                (
                                    "caption",
                                    wagtail.core.blocks.CharBlock(
                                        label="Bild-Unterschrift", required=False
                                    ),
                                ),
                            ]
                        ),
                    ),
                ],
                blank=True,
                verbose_name="Inhalt",
            ),
        ),
        migrations.AlterField(
            model_name="standardpage",
            name="body",
            field=wagtail.core.fields.StreamField(
                [
                    (
                        "paragraph",
                        core.blocks.ParagraphBlock(
                            features=[
                                "h2",
                                "h3",
                                "bold",
                                "italic",
                                "link",
                                "ol",
                                "ul",
                                "document-link",
                                "anchor-identifier",
                            ]
                        ),
                    ),
                    (
                        "image",
                        wagtail.core.blocks.StructBlock(
                            [
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
                                    "size",
                                    wagtail.core.blocks.ChoiceBlock(
                                        choices=[
                                            ("text-width", "Text-Breite"),
                                            ("over-text-width", "Über-Text-Breite"),
                                        ]
                                    ),
                                ),
                            ]
                        ),
                    ),
                    (
                        "several_images",
                        core.blocks.ImagesBlock(core.blocks.ImageCarouselBlock),
                    ),
                    (
                        "gallery",
                        wagtail.core.blocks.StructBlock(
                            [
                                (
                                    "collection",
                                    wagtail.core.blocks.ChoiceBlock(
                                        choices=core.blocks.get_image_gallery_choices,
                                        help_text="Die Bilder aus der Sammlung werden dann als Gallerie angezeigt.",
                                        label="Sammlung",
                                    ),
                                ),
                                (
                                    "start_image",
                                    wagtail.images.blocks.ImageChooserBlock(
                                        help_text="Das Bild, das als erstes angezeigt wird.",
                                        label="erstes Bild",
                                        required=False,
                                    ),
                                ),
                            ]
                        ),
                    ),
                    (
                        "embed",
                        wagtail.core.blocks.StructBlock(
                            [
                                (
                                    "embed",
                                    wagtail.embeds.blocks.EmbedBlock(
                                        help_text="von z.B. einem Youtube-Video, Facebook-Post, Instagram-Bild, …",
                                        label="URL",
                                    ),
                                ),
                                (
                                    "caption",
                                    wagtail.core.blocks.CharBlock(
                                        label="opt. Beschrift.", required=False
                                    ),
                                ),
                                (
                                    "size",
                                    wagtail.core.blocks.ChoiceBlock(
                                        choices=[
                                            ("text-width", "Text-Breite"),
                                            ("over-text-width", "Über-Text-Breite"),
                                        ]
                                    ),
                                ),
                            ]
                        ),
                    ),
                    (
                        "button",
                        wagtail.core.blocks.StructBlock(
                            [
                                ("text", wagtail.core.blocks.CharBlock(label="Text")),
                                (
                                    "link",
                                    wagtail.core.blocks.URLBlock(
                                        label="Link", required=False
                                    ),
                                ),
                                (
                                    "mail",
                                    wagtail.core.blocks.EmailBlock(
                                        help_text="wird anstelle von link benutzt",
                                        label="E-Mail",
                                        required=False,
                                    ),
                                ),
                                (
                                    "color",
                                    wagtail.core.blocks.ChoiceBlock(
                                        choices=[
                                            ("green", "Grün"),
                                            ("red", "Rot"),
                                            ("blue", "Blau"),
                                            ("orange", "Orange"),
                                            ("purple", "Lila"),
                                        ],
                                        label="Farbe",
                                    ),
                                ),
                                (
                                    "aslink",
                                    wagtail.core.blocks.BooleanBlock(
                                        label="ohne Hintergrund", required=False
                                    ),
                                ),
                            ]
                        ),
                    ),
                    ("attachment", core.blocks.Attachment()),
                    ("table", wagtail.contrib.table_block.blocks.TableBlock()),
                    (
                        "map_image",
                        wagtail.core.blocks.StructBlock(
                            [
                                (
                                    "tile_url",
                                    wagtail.core.blocks.URLBlock(
                                        help_text="URL zu den Kacheln, aus denen das Bild besteht. Benutze {z}, {x}, {y} in der URL für die Koordinaten",
                                        label="Kachel-URL",
                                        required=True,
                                    ),
                                ),
                                (
                                    "height",
                                    wagtail.core.blocks.DecimalBlock(
                                        help_text="in speziellen Leaflet Einheiten",
                                        label="Höhe",
                                        required=True,
                                    ),
                                ),
                                (
                                    "width",
                                    wagtail.core.blocks.DecimalBlock(
                                        help_text="in speziellen Leaflet Einheiten",
                                        label="Breite",
                                        required=True,
                                    ),
                                ),
                                (
                                    "attribution",
                                    wagtail.core.blocks.CharBlock(
                                        help_text="Wird unten rechts im Bild angezeigt.",
                                        label="Urheber",
                                        required=False,
                                    ),
                                ),
                            ]
                        ),
                    ),
                    (
                        "iframe",
                        wagtail.core.blocks.StructBlock(
                            [
                                (
                                    "url",
                                    wagtail.core.blocks.URLBlock(
                                        help_text="URL zu der Website, die mittels Iframe eingebunden werden soll.",
                                        label="URL",
                                        required=True,
                                    ),
                                ),
                                (
                                    "allowFullScreen",
                                    wagtail.core.blocks.BooleanBlock(
                                        label="Vollbild erlauben?", required=False
                                    ),
                                ),
                                (
                                    "height",
                                    wagtail.core.blocks.DecimalBlock(
                                        default="1000", help_text="in px", label="Höhe"
                                    ),
                                ),
                                (
                                    "width",
                                    wagtail.core.blocks.DecimalBlock(
                                        default="1000",
                                        help_text="in px",
                                        label="Breite",
                                    ),
                                ),
                            ]
                        ),
                    ),
                    (
                        "video_link",
                        wagtail.core.blocks.StructBlock(
                            [
                                (
                                    "url",
                                    wagtail.core.blocks.URLBlock(
                                        help_text="URL zu dem Video, auf das verlinkt wird",
                                        label="URL",
                                        required=True,
                                    ),
                                ),
                                (
                                    "image",
                                    wagtail.images.blocks.ImageChooserBlock(
                                        label="Bild (schwarz wenn nichts angegeben)",
                                        required=False,
                                    ),
                                ),
                                (
                                    "caption",
                                    wagtail.core.blocks.CharBlock(
                                        label="Bild-Unterschrift", required=False
                                    ),
                                ),
                            ]
                        ),
                    ),
                ],
                blank=True,
                verbose_name="Inhalt",
            ),
        ),
    ]
