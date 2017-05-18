from wagtail.wagtailcore import blocks
from wagtail.wagtailcore.blocks.field_block import FieldBlock

from wagtail.wagtailembeds.blocks import EmbedBlock
from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtaildocs.blocks import DocumentChooserBlock

from wagtail.contrib.table_block.blocks import TableBlock

from .fields import PrettyURLField
from .images import AttributedImage as Image
from wagtail.wagtailcore.models import Collection
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


class ImageCarouselBlock(blocks.StructBlock):
    image = ImageChooserBlock(
        label="Bild"
    )
    caption = blocks.CharBlock(
        label="opt. Beschrift.",
        required=False
    )
    class Meta:
        icon = 'image'
        label = 'Bild'


class ImagesBlock(blocks.ListBlock):

    def get_context(self, value, parent_context=None):
       context = super(ImagesBlock, self).get_context(value, parent_context=parent_context)
       count = len(context['self'])
       context['aspect'] = 66.66
       context['srcset'] = 'fill-300x200 fill-600x400 fill-900x600 fill-1200x800'
       if count == 1:
           context['srcset'] = 'width-320 width-640 width-960 width-1280'
           context['sizes'] = '(min-width: 830px) 830px, 100vw'
           context['multiple'] = 1
           context['aspect'] = context['self'][0].get('image').aspect
       elif count % 4 == 0:
            context['sizes'] = '(min-width: 830px) 208px, 100vw'
            context['multiple'] = 4
       elif count % 3 == 0 or count in (5,7,10):
           context['sizes'] = '(min-width: 830px) 267px, 100vw'
           context['multiple'] = 3
       elif count % 2 == 0:
           context['sizes'] = '(min-width: 830px) 405px, 100vw'
           context['multiple'] = 2
       else:
           context['sizes'] = '(min-width: 830px) 405px, 50vw'
           context['multiple'] = 2
       return context

    class Meta:
        template = "blocks/several_images.html",
        label = "Bilder"
        icon = "image"


def get_image_gallery_choices():
    return [
        (collection.id, collection.name)
        for collection in Collection.objects.all()
        if collection.name != "Root"
    ]

class ImageGalleryBlock(blocks.StructBlock):

    collection = blocks.ChoiceBlock(
        label = "Sammlung",
        choices = get_image_gallery_choices,
        help_text="Die Bilder aus der Sammlung werden dann als Gallerie angezeigt."
    )

    def get_gallery_images(self, collection, tags=None):
        images = None
        try:
            images = Image.objects.filter(collection__id=collection).order_by('-created_at')
        except Exception as e:
            pass
        if images and tags:
            images = images.filter(tags__name__in=tags).distinct()
        return images

    def get_context(self, value, parent_context=None):
       context = super().get_context(value, parent_context=parent_context)
       context['images'] = self.get_gallery_images(value['collection'])
       return context

    class Meta:
        template = "blocks/gallery.html",
        form_template = 'blocks/gallery_form.html'
        label = "Gallerie"
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
    several_images = ImagesBlock(ImageCarouselBlock)
    gallery = ImageGalleryBlock()
    embed = OurEmbedBlock()
    button = Button()
    attachment = Attachment()
    table = TableBlock()
