from django.db import models
from django.utils.text import slugify

from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailadmin.edit_handlers import (FieldPanel, InlinePanel,
                                                ObjectList, PageChooserPanel,
                                                StreamFieldPanel, FieldRowPanel,
                                                TabbedInterface, MultiFieldPanel)
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailsearch import index

from core.blocks import StandardStreamBlock
from core.models import BasePage
from core.images import AttributedImage as Image



class PersonPage(BasePage):
    first_name = models.CharField("Vorname", max_length=255)
    last_name = models.CharField("Nachname", max_length=255, blank=True)
    text = StreamField(
        StandardStreamBlock(),
        blank=True,
        verbose_name="Text",
    )

    photo = models.ForeignKey(
        Image,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    content_panels = [
        MultiFieldPanel([
            FieldPanel('first_name'),
            FieldPanel('last_name'),
        ]),
        ImageChooserPanel('photo'),
        StreamFieldPanel('text'),
    ]

    search_fields = [
        index.SearchField('first_name', partial_match=True),
        index.SearchField('last_name', partial_match=True),
    ]



    def clean(self):
        super().clean()
        self.title = "%s %s" % (self.first_name, self.last_name)
        self.slug = slugify(self.title)
