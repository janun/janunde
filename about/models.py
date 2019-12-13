from django.db import models
from django.utils.text import slugify

from wagtail.core.fields import StreamField
from wagtail.admin.edit_handlers import (FieldPanel, InlinePanel,
                                                ObjectList, PageChooserPanel,
                                                StreamFieldPanel, FieldRowPanel,
                                                TabbedInterface, MultiFieldPanel)
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index
from wagtail.core.fields import RichTextField
from wagtail.core.fields import StreamField


from core.blocks import StandardStreamBlock
from core.models import HeaderMixin, BasePage
from core.images import AttributedImage as Image



class AboutPage(BasePage, HeaderMixin):

    content = StreamField(
        StandardStreamBlock(),
        blank=True,
        verbose_name="Inhalt",
    )

    content_panels = [
        FieldPanel('title'),
        MultiFieldPanel(HeaderMixin.panels, "Header"),
        StreamFieldPanel('content'),
    ]

    def get_image(self):
        if super().get_image():
            return super().get_image()
        for block in self.content:
            if block.block_type == 'image':
                return block.value['image']

    def get_description(self):
        if self.search_description:
            return self.search_description
        from django.utils.text import Truncator
        import html2text
        h = html2text.HTML2Text()
        h.ignore_links = True
        for block in self.content:
            if block.block_type == 'paragraph':
                text = h.handle(block.value.source)
                return Truncator(text).words(25)
