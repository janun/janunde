from wagtail.wagtailcore import blocks
from wagtail.wagtailcore.blocks.field_block import FieldBlock

from wagtail.wagtailembeds.blocks import EmbedBlock
from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtaildocs.blocks import DocumentChooserBlock


from core.fields import PrettyURLField


def _(str):
    """dummy trans"""
    return str


# class PrettyURLBlock(FieldBlock):
#     def __init__(self, required=True, help_text=None, max_length=None, min_length=None, **kwargs):
#         self.field = PrettyURLField(
#             required=required,
#             help_text=help_text,
#             max_length=max_length,
#             #min_length=min_length
#         )
#         super().__init__(**kwargs)
#     class Meta:
#         icon = "site"


COLOR_CHOICES = [
    ('brown', 'Braun'),
    ('green', 'Grün'),
    ('red', 'Rot'),
    ('blue', 'Blau'),
    ('orange', 'Orange'),
]


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


class H2(blocks.StructBlock):
    title = blocks.CharBlock(label="Titel")
    color = blocks.ChoiceBlock(label="Farbe", choices=COLOR_CHOICES, default="brown")
    class Meta:
        label = _("Überschrift")
        icon = "bold"
        classname = "title"
        template = 'blocks/h2.html'


class Title(blocks.StructBlock):
    title = blocks.CharBlock(label="Titel", classname="title")
    color = blocks.ChoiceBlock(label="Farbe", choices=COLOR_CHOICES, default="brown")
    class Meta:
        label = _("Titel")
        icon = "title"
        classname = "title"
        template = 'blocks/title.html'


class Button(blocks.StructBlock):
    text = blocks.CharBlock(label="Text")
    link = blocks.URLBlock(label="Link")
    color = blocks.ChoiceBlock(label="Farbe", choices=COLOR_CHOICES, default="green")
    class Meta:
        label = _("Button")
        icon = "link"
        template = 'blocks/button.html'


class Attachment(DocumentChooserBlock):
    class Meta:
        label = _("Dateianhang")
        icon = "doc-full"
        template = 'blocks/attachment.html'


class VideoBlock(EmbedBlock):
    def __init__(self, *args, **kwargs):
        kwargs['help_text'] = _("URL von z.B. Youtube oder "
                                "Vimeo hier reinkopieren")
        super().__init__(*args, **kwargs)

    class Meta:
        label = _("externes Video")
        icon = "media"


class StandardStreamBlock(blocks.StreamBlock):
    title = Title()
    h2 = H2()
    paragraph = blocks.RichTextBlock(label=_("Absatz"), icon="pilcrow")
    image = ImageBlock()
    embedded_video = VideoBlock()
    button = Button()
    attachment = Attachment()
