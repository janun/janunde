from wagtail.wagtailcore import blocks
from wagtail.wagtailcore.blocks.field_block import FieldBlock

from wagtail.wagtailembeds.blocks import EmbedBlock
from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtaildocs.blocks import DocumentChooserBlock

from wagtail.contrib.table_block.blocks import TableBlock

from .fields import PrettyURLField
#from .models import COLOR_CHOICES

def _(str):
    """dummy trans"""
    return str

COLOR_CHOICES = [
    ('green', 'Grün'),
    ('red', 'Rot'),
    ('blue', 'Blau'),
    ('orange', 'Orange'),
]

class SizeChoiceBlock(blocks.ChoiceBlock):
    choices = [
        ('text-width', 'Text-Breite'),
        ('over-text-width', 'Über-Text-Breite'),
        ('screen-width', 'Bildchirm-Breite')
    ]
    class Meta:
        default = 'over-text-width'
        label = "Größe"


class ImageBlock(blocks.StructBlock):
    image = ImageChooserBlock(label="Bild")
    caption = blocks.CharBlock(
        label="opt. Beschrift.",
        required=False
    )
    size = SizeChoiceBlock()
    class Meta:
        label = _("Bild")
        template = 'blocks/image.html'
        icon = "image"


class Button(blocks.StructBlock):
    text = blocks.CharBlock(label="Text")
    link = blocks.URLBlock(label="Link")
    color = blocks.ChoiceBlock(
        label="Farbe", choices=COLOR_CHOICES, default="green"
    )
    class Meta:
        label = _("Button")
        icon = "link"
        template = 'blocks/button.html'


class Attachment(DocumentChooserBlock):
    class Meta:
        label = _("Dateianhang")
        icon = "doc-full"
        template = 'blocks/attachment.html'


class OurEmbedBlock(blocks.StructBlock):
    embed = EmbedBlock(
        label="URL",
        help_text="von z.B. einem Youtube-Video, Facebook-Post, Instagram-Bild, …"
    )
    caption = blocks.CharBlock(
        label="opt. Beschrift.",
        required=False
    )
    size = SizeChoiceBlock(default="text-width")
    class Meta:
        label = _("externe Medien")
        icon = "media"
        template = 'blocks/embed.html'


class ParagraphBlock(blocks.RichTextBlock):
    class Meta:
        label = "Absatz"
        icon = "pilcrow"
        template = 'blocks/paragraph.html'



class StandardStreamBlock(blocks.StreamBlock):
    paragraph = ParagraphBlock()
    image = ImageBlock()
    embed = OurEmbedBlock()
    button = Button()
    attachment = Attachment()
    table = TableBlock()
