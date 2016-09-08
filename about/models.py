from django.db import models
from django.utils.text import slugify

from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailadmin.edit_handlers import (FieldPanel, InlinePanel,
                                                ObjectList, PageChooserPanel,
                                                StreamFieldPanel, FieldRowPanel,
                                                TabbedInterface, MultiFieldPanel)
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailsearch import index
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailcore.fields import StreamField


from core.blocks import StandardStreamBlock
from core.models import BasePage
from core.images import AttributedImage as Image



class AboutPage(BasePage):
    heading = models.CharField(
        "Überschrift",
        max_length=255,
        blank=True
    )

    intro_text = RichTextField(
        "Eingangstext",
        blank=True,
    )

    content = StreamField(
        StandardStreamBlock(),
        blank=True,
        verbose_name="Inhalt",
    )

    content_panels = [
        MultiFieldPanel([
            FieldPanel('title', classname="full"),
            FieldPanel('heading', classname="full"),
        ]),
        FieldPanel('intro_text'),
        StreamFieldPanel('content'),
    ]

    def get_image(self):
        for block in self.content:
            if block.block_type == 'image':
                return block.value['image']
