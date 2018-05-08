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
from wagtail.wagtailcore.models import Orderable, PageManager

from core.blocks import StandardStreamBlock
from core.models import BasePage, HeaderMixin
from core.images import AttributedImage as Image

from phonenumber_field.modelfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberInternationalFallbackWidget





class ContactIndex(BasePage, HeaderMixin):
    subpage_types = ['PersonPage', 'OfficePage']
    parent_page_types = ['core.HomePage']

    class Meta:
        verbose_name = "Auflistung von Kontakten"

    def get_context(self, request):
        context = super().get_context(request)
        context['people'] = PersonPage.objects.descendant_of(self).live()
        context['offices'] = OfficePage.objects.descendant_of(self).live()
        return context

    content_panels = [
        FieldPanel('title'),
        MultiFieldPanel(HeaderMixin.panels, "Header"),
    ]






# class PersonPageContactPossibility(Orderable):
#     page = ParentalKey(PersonPage, related_name='contact_possibilities')
#     contact = models.CharField(max_length=255)
#
#     panels = [
#         FieldPanel('contact'),
#     ]


class OfficePageManager(PageManager):
    def get_queryset(self):
         return super().get_queryset().order_by('title')

from core.forms import ShortTitleForm

class OfficePage(BasePage):
    partial_template_name = "contact/_office.html"
    base_form_class = ShortTitleForm

    photo = models.ForeignKey(
        Image,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    text = StreamField(
        StandardStreamBlock(),
        blank=True,
        verbose_name="Text",
    )

    mail = models.EmailField("E-Mail", blank=True)
    phone = PhoneNumberField("Telefonnummer", blank=True)
    address = models.CharField("Adresse", blank=True, max_length=255)

    objects = OfficePageManager()

    content_panels = [
        FieldPanel('title'),
        ImageChooserPanel('photo'),
        FieldPanel('address'),
        FieldPanel('mail'),
        FieldPanel('phone', widget=PhoneNumberInternationalFallbackWidget),
        StreamFieldPanel('text'),
    ]

    search_fields = BasePage.search_fields + [
        index.SearchField('text'),
        index.SearchField('mail'),
        #index.SearchField('phone'), # currently unable to serialize
        index.SearchField('address'),
    ]

    class Meta:
        verbose_name = "Büro"
        verbose_name_plural = "Büros"


class PersonPageManager(PageManager):
    def get_queryset(self):
         return super().get_queryset().order_by('title')

class PersonPage(BasePage):
    partial_template_name = "contact/_person.html"

    text = StreamField(
        StandardStreamBlock(),
        blank=True,
        verbose_name="Text",
    )
    role = models.CharField("Rolle", max_length=255, blank=True)
    mail = models.EmailField("E-Mail", blank=True)
    phone = PhoneNumberField("Telefonnummer", blank=True)

    office = models.ForeignKey(
        OfficePage,
        null=True,
        blank=True,
        related_name='people',
        on_delete=models.SET_NULL,
        verbose_name="Zugehöriges Büro",
    )

    photo = models.ForeignKey(
        Image,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    objects = PersonPageManager()

    search_fields = BasePage.search_fields + [
        index.SearchField('text'),
        index.SearchField('mail'),
        #index.SearchField('phone'), # currently unable to serialize
        index.SearchField('role'),
    ]

    content_panels = [
        FieldPanel('title'),
        ImageChooserPanel('photo'),
        FieldPanel('role'),
        FieldPanel('mail'),
        FieldPanel('phone', widget=PhoneNumberInternationalFallbackWidget),
        StreamFieldPanel('text'),
        FieldPanel('office'),
    ]

    class Meta:
        verbose_name = "Person"
        verbose_name_plural = "Personen"
