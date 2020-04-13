from wagtail.core import blocks
from wagtail.embeds.blocks import EmbedBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.contrib.table_block.blocks import TableBlock
from wagtail.core.models import Collection

from .images import AttributedImage as Image


COLOR_CHOICES = [
    ("green", "Grün"),
    ("red", "Rot"),
    ("blue", "Blau"),
    ("orange", "Orange"),
    ("purple", "Lila"),
]


class SizeChoiceBlock(blocks.ChoiceBlock):
    choices = [
        ("text-width", "Text-Breite"),
        ("over-text-width", "Über-Text-Breite"),
    ]

    class Meta:
        label = "Breite"


class ImageBlock(blocks.StructBlock):
    image = ImageChooserBlock(label="Bild")
    caption = blocks.CharBlock(label="Bildunterschrift", required=False)
    size = SizeChoiceBlock(default="over-text-width")

    class Meta:
        label = "Bild"
        template = "blocks/image.html"
        icon = "image"


class ImageCarouselBlock(blocks.StructBlock):
    image = ImageChooserBlock(label="Bild")
    caption = blocks.CharBlock(label="opt. Beschrift.", required=False)

    class Meta:
        icon = "image"
        label = "Bild"


class ImagesBlock(blocks.ListBlock):
    def get_context(self, value, parent_context=None):
        context = super(ImagesBlock, self).get_context(
            value, parent_context=parent_context
        )
        count = len(context["self"])
        context["aspect"] = 66.66
        context["srcset"] = "fill-300x200 fill-600x400 fill-900x600 fill-1200x800"
        if count == 1:
            context["srcset"] = "width-320 width-640 width-960 width-1280"
            context["sizes"] = "(min-width: 830px) 830px, 100vw"
            context["multiple"] = 1
            context["aspect"] = context["self"][0].get("image").aspect
        elif count % 4 == 0:
            context["sizes"] = "(min-width: 830px) 208px, 100vw"
            context["multiple"] = 4
        elif count % 3 == 0 or count in (5, 7, 10):
            context["sizes"] = "(min-width: 830px) 267px, 100vw"
            context["multiple"] = 3
        elif count % 2 == 0:
            context["sizes"] = "(min-width: 830px) 405px, 100vw"
            context["multiple"] = 2
        else:
            context["sizes"] = "(min-width: 830px) 405px, 50vw"
            context["multiple"] = 2
        return context

    class Meta:
        template = ("blocks/several_images.html",)
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
        label="Sammlung",
        choices=get_image_gallery_choices,
        help_text="Die Bilder aus der Sammlung werden dann als Gallerie angezeigt.",
    )

    start_image = ImageChooserBlock(
        label="erstes Bild",
        required=False,
        help_text="Das Bild, das als erstes angezeigt wird.",
    )

    def get_gallery_images(self, collection, tags=None):
        images = None
        try:
            images = Image.objects.filter(collection__id=collection).order_by(
                "-created_at"
            )
        except Exception:
            pass
        if images and tags:
            images = images.filter(tags__name__in=tags).distinct()
        return images

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context=parent_context)
        context["images"] = list(self.get_gallery_images(value["collection"]))
        if value.get("start_image", None):
            context["images"].insert(0, value["start_image"])
        return context

    class Meta:
        template = ("blocks/gallery.html",)
        form_template = "blocks/gallery_form.html"
        label = "Gallerie"
        icon = "image"


class Button(blocks.StructBlock):
    text = blocks.CharBlock(label="Text")
    link = blocks.URLBlock(label="Link", required=False)
    mail = blocks.EmailBlock(
        label="E-Mail", help_text="wird anstelle von link benutzt", required=False
    )
    color = blocks.ChoiceBlock(label="Farbe", choices=COLOR_CHOICES, default="green")
    aslink = blocks.BooleanBlock(required=False, label="ohne Hintergrund")

    class Meta:
        label = "Button"
        icon = "link"
        template = "blocks/button.html"


class Attachment(DocumentChooserBlock):
    class Meta:
        label = "Dateianhang"
        icon = "doc-full"
        template = "blocks/attachment.html"


class OurEmbedBlock(blocks.StructBlock):
    embed = EmbedBlock(
        label="URL",
        help_text="von z.B. einem Youtube-Video, Facebook-Post, Instagram-Bild, …",
    )
    caption = blocks.CharBlock(label="opt. Beschrift.", required=False)
    size = SizeChoiceBlock(default="text-width")

    class Meta:
        label = "externe Medien"
        icon = "media"
        template = "blocks/embed.html"


class ParagraphBlock(blocks.RichTextBlock):
    class Meta:
        label = "Absatz"
        icon = "pilcrow"
        template = "blocks/paragraph.html"


class MapImage(blocks.StructBlock):
    tile_url = blocks.URLBlock(
        label="Kachel-URL",
        required=True,
        help_text="URL zu den Kacheln, aus denen das Bild besteht. Benutze {z}, {x}, {y} in der URL für die Koordinaten",
    )
    height = blocks.DecimalBlock(
        required=True, label="Höhe", help_text="in speziellen Leaflet Einheiten"
    )
    width = blocks.DecimalBlock(
        required=True, label="Breite", help_text="in speziellen Leaflet Einheiten"
    )
    attribution = blocks.CharBlock(
        label="Urheber",
        help_text="Wird unten rechts im Bild angezeigt.",
        required=False,
    )

    class Meta:
        label = "Map-Bild"
        icon = "media"
        template = "blocks/map_image.html"


class IframeBlock(blocks.StructBlock):
    url = blocks.URLBlock(
        label="URL",
        required=True,
        help_text="URL zu der Website, die mittels Iframe eingebunden werden soll.",
    )

    allowFullScreen = blocks.BooleanBlock(label="Vollbild erlauben?", required=False,)

    height = blocks.DecimalBlock(default="1000", label="Höhe", help_text="in px")
    width = blocks.DecimalBlock(default="1000", label="Breite", help_text="in px")

    class Meta:
        label = "Iframe"
        icon = "media"
        template = "blocks/iframe.html"


class VideoLink(blocks.StructBlock):
    url = blocks.URLBlock(
        label="URL", required=True, help_text="URL zu dem Video, auf das verlinkt wird"
    )

    image = ImageChooserBlock(
        label="Bild (schwarz wenn nichts angegeben)", required=False,
    )

    caption = blocks.CharBlock(label="Bild-Unterschrift", required=False)

    class Meta:
        label = "Link zu Video"
        icon = "media"
        template = "blocks/video_link.html"


class StandardStreamBlock(blocks.StreamBlock):
    paragraph = ParagraphBlock(
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
    )
    image = ImageBlock()
    several_images = ImagesBlock(ImageCarouselBlock)
    gallery = ImageGalleryBlock()
    embed = OurEmbedBlock()
    button = Button()
    attachment = Attachment()
    table = TableBlock()
    map_image = MapImage()
    iframe = IframeBlock()
    video_link = VideoLink()


class HeaderButton(blocks.StructBlock):
    text = blocks.CharBlock(label="Text")
    link = blocks.CharBlock(label="Link")
    primary = blocks.BooleanBlock(label="Primär", required=False)

    class Meta:
        label = "Button"
        icon = "link"


class HeaderBlock(blocks.StructBlock):
    background = ImageChooserBlock(label="Hintergrundbild", required=False)
    heading = blocks.CharBlock(label="Überschrift", required=False)
    highlight_in_heading = blocks.CharBlock(
        label="Hervorhebungen in der Überschrift",
        help_text="Wiederhole Text aus der Überschrift der farblich hervorgehoben werden soll",
        required=False,
    )
    text = blocks.RichTextBlock(label="Text", required=False)
    text_mobile = blocks.RichTextBlock(label="Text (mobil)", required=False)
    buttons = blocks.ListBlock(HeaderButton())

    class Meta:
        label = "Header"
        icon = "home"
        template = "blocks/header.html"


class ParagraphTwoBlock(blocks.StructBlock):
    big = blocks.BooleanBlock(label="Groß", required=False,)
    center = blocks.BooleanBlock(label="zentriert", required=False,)
    text = blocks.RichTextBlock()

    class Meta:
        label = "Absatz"
        icon = "pilcrow"
        template = "blocks/paragraph2.html"


class TeaserBlock(blocks.StructBlock):
    background = ImageChooserBlock(label="Hintergrundbild", required=False,)
    title = blocks.CharBlock(label="Titel", required=False)
    subtitle = blocks.CharBlock(label="Untertitel", required=False)
    rotate = blocks.BooleanBlock(label="gedreht", required=False)

    class Meta:
        label = "Zwischentitel"
        icon = "title"
        template = "blocks/teaser.html"


class HighlightsBlock(blocks.StructBlock):
    heading = blocks.CharBlock(label="Überschrift", required=False)
    objects = blocks.ListBlock(blocks.PageChooserBlock(), label="Objekte",)

    class Meta:
        label = "Highlights"
        icon = "pick"
        template = "blocks/highlights.html"


class EventsBlock(blocks.StructBlock):
    heading = blocks.CharBlock(label="Überschrift", required=False)

    def get_context(self, value, parent_context=None):
        # to prevent circular import
        from events.models import EventPage  # pylint: disable=import-outside-toplevel

        context = super().get_context(value, parent_context=parent_context)
        context["upcoming"] = EventPage.objects.upcoming()[:3]
        return context

    class Meta:
        label = "Veranstaltungen"
        icon = "date"
        template = "blocks/events.html"


class NewsletterSignupBlock(blocks.StructBlock):
    heading = blocks.CharBlock(label="Überschrift", required=False)
    text = blocks.RichTextBlock(label="Text", required=False)
    example_url = blocks.URLBlock(label="Link zu Beispiel-E-Mail", required=False)

    class Meta:
        label = "Newsletter-Anmeldung"
        icon = "form"
        template = "blocks/newsletter.html"


class BoxBlock(blocks.StructBlock):
    heading = blocks.CharBlock(label="Überschrift", required=False)
    text = blocks.RichTextBlock(label="Text", required=False)
    buttons = blocks.ListBlock(Button())

    class Meta:
        label = "Box"
        icon = "placeholder"
        template = "blocks/box.html"


class GapBlock(blocks.StructBlock):
    size = blocks.DecimalBlock(
        required=False,
        label="Größe",
        help_text="Größe des vertikalen Abstands in Pixeln",
    )

    class Meta:
        label = "Abstand"
        icon = "placeholder"
        template = "blocks/gap.html"


class HomepageImageBlock(blocks.StructBlock):
    image = ImageChooserBlock(label="Bild")
    caption = blocks.CharBlock(label="Bildunterschrift", required=False)

    class Meta:
        label = "Bild"
        template = "blocks/homepage_image.html"
        icon = "image"


class HomepageGroupsBlock(blocks.StructBlock):
    heading = blocks.CharBlock(label="Überschrift", required=False)
    highlight_in_heading = blocks.CharBlock(
        label="Hervorhebungen in der Überschrift",
        help_text="Wiederhole Text aus der Überschrift der farblich hervorgehoben werden soll",
        required=False,
    )

    def get_context(self, value, parent_context=None):
        # to prevent circular import
        from core.models import Group  # pylint: disable=import-outside-toplevel

        context = super().get_context(value, parent_context=parent_context)
        context["groups"] = Group.objects.all()
        return context

    class Meta:
        label = "JANUN-Gruppen"
        template = "blocks/homepage_groups.html"
        icon = "image"


class HomePageStreamBlock(blocks.StreamBlock):
    header = HeaderBlock()
    paragraph2 = ParagraphTwoBlock()
    button = Button()
    teaser = TeaserBlock()
    highlights = HighlightsBlock()
    newsletter = NewsletterSignupBlock()
    box = BoxBlock()
    gap = GapBlock()
    events = EventsBlock()
    embed = OurEmbedBlock()
    iframe = IframeBlock()
    video_link = VideoLink()
    image = HomepageImageBlock()
    groups = HomepageGroupsBlock()
