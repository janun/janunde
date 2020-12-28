from wagtail.core.fields import StreamField
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel

from core.models import BasePage

from .blocks import ContactBlocks


class ContactPage(BasePage):
    parent_page_types = ["core.HomePage"]
    max_count = 1

    content = StreamField(
        ContactBlocks(required=False), blank=True, null=True, verbose_name="Inhalt",
    )

    class Meta:
        verbose_name = "Kontaktseite"
        verbose_name_plural = "Kontaktseiten"

    content_panels = [
        FieldPanel("title"),
        StreamFieldPanel("content"),
    ]
