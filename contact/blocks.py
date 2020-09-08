from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock


class ContactBlock(blocks.StructBlock):
    heading = blocks.CharBlock(label="Überschrift")
    text = blocks.RichTextBlock(label="Text", required=False)
    image = ImageChooserBlock(label="Bild", required=False)

    telephone = blocks.CharBlock(label="Telefon-Nummer", required=False)
    telephone_hours = blocks.CharBlock(
        label="Telefon-Nummer Öffnungszeiten", required=False
    )

    email = blocks.EmailBlock(label="E-Mail-Adresse", required=False)

    address = blocks.RichTextBlock(label="Adresse", required=False)
    address_google = blocks.URLBlock(label="Adresse bei Google", required=False)
    address_osm = blocks.URLBlock(label="Adresse bei OpenStreetMaps", required=False)
    address_directions = blocks.URLBlock(
        label="Adresse: Link zu Wegbeschreibung", required=False
    )

    link_text = blocks.CharBlock(label="Link-Text", required=False)
    link_url = blocks.URLBlock(label="Link-URL", required=False)

    class Meta:
        label = "Kontakt-Block"
        template = "contact/block.html"


class ContactBlocks(blocks.StreamBlock):
    contact_block = ContactBlock()
