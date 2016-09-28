from django.db import models
from django.utils.text import slugify

from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailadmin.edit_handlers import (FieldPanel, InlinePanel,
                                                ObjectList, PageChooserPanel,
                                                StreamFieldPanel, FieldRowPanel,
                                                TabbedInterface, MultiFieldPanel)
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailsearch import index

from modelcluster.fields import ParentalKey
from wagtail.wagtailcore.models import Orderable

from core.blocks import StandardStreamBlock
from core.models import BasePage
from core.images import AttributedImage as Image

from phonenumber_field.modelfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberInternationalFallbackWidget





class ContactIndex(BasePage):
    subpage_types = ['PersonPage']
    parent_page_types = ['core.HomePage']

    class Meta:
        verbose_name = "Auflistung von Kontakten"

    def get_context(self, request):
        context = super().get_context(request)
        context['people'] = PersonPage.objects.child_of(self).live().order_by('title')
        return context






# class PersonPageContactPossibility(Orderable):
#     page = ParentalKey(PersonPage, related_name='contact_possibilities')
#     contact = models.CharField(max_length=255)
#
#     panels = [
#         FieldPanel('contact'),
#     ]



class PersonPage(BasePage):
    text = StreamField(
        StandardStreamBlock(),
        blank=True,
        verbose_name="Text",
    )
    role = models.CharField("Rolle", max_length=255, blank=True)
    mail = models.EmailField("E-Mail", blank=True)
    phone = PhoneNumberField("Telefonnummer", blank=True)

    photo = models.ForeignKey(
        Image,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    content_panels = [
        FieldPanel('title'),
        ImageChooserPanel('photo'),
        FieldPanel('role'),
        FieldPanel('mail'),
        FieldPanel('phone', widget=PhoneNumberInternationalFallbackWidget),
        StreamFieldPanel('text'),
    ]

    search_fields = [
        index.SearchField('title', partial_match=True),
    ]
