from wagtail.wagtailcore import blocks
from wagtail.wagtailembeds.blocks import EmbedBlock
from wagtail.wagtailimages.blocks import ImageChooserBlock


def _(str):
    """dummy trans"""
    return str


class ImageBlock(blocks.StructBlock):
    image = ImageChooserBlock(label="Bild")
    caption = blocks.CharBlock(
        label="Bildunterschrift",
        required=False
    )
    full_width = blocks.BooleanBlock(
        label="volle Breite",
        help_text="Soll das Bild auf voller Breite des Bildschirms angezeigt werden?",
        required=False
    )
    class Meta:
        label = _("Bild")
        template = 'blocks/image.html'
        icon = "image"


class H2(blocks.CharBlock):
    class Meta:
        label = _("Überschrift")
        icon = "title"
        classname = "title"
        template = 'blocks/h2.html'


class Title(blocks.StructBlock):
    title = blocks.CharBlock(label="Titel", classname="title")
    color = blocks.ChoiceBlock(label="Farbe", choices=[
        ('brown', 'Braun'),
        ('green', 'Grün'),
        ('red', 'Rot'),
        ('blue', 'Blau'),
        ('orange', 'Orange'),
    ], default="brown", classname="")

    class Meta:
        label = _("Titel")
        icon = "title"
        classname = "title"
        template = 'blocks/title.html'


class VideoBlock(EmbedBlock):
    def __init__(self, *args, **kwargs):
        kwargs['help_text'] = _("URL von z.B. Youtube oder "
                                "Vimeo hier reinkopieren")
        super().__init__(*args, **kwargs)

    class Meta:
        label = _("externes Video")
        icon = "media"


class StandardStreamBlock(blocks.StreamBlock):
    h2 = H2()
    title = Title()
    paragraph = blocks.RichTextBlock(label=_("Absatz"), icon="pilcrow")
    image = ImageBlock()
    embedded_video = VideoBlock()
