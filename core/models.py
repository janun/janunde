from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from modelcluster.fields import ParentalKey
from wagtail.wagtailadmin.edit_handlers import (FieldPanel, InlinePanel,
                                                ObjectList, PageChooserPanel,
                                                StreamFieldPanel,
                                                TabbedInterface)
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailcore.models import Orderable, Page
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailsearch import index

from .blocks import StandardStreamBlock
from .images import AttributedImage as Image


def _(str):
    """dummy trans"""
    return str


class BasePage(Page):
    """basic functionality for all our pages"""
    partial_template_name = 'core/_partial.html'
    medium_partial_template_name = 'core/_medium_partial.html'

    is_creatable = False


class RelatedPage(models.Model):
    """
    every stadardpage and descendants can have a related page (any page)
    """
    related_page = models.ForeignKey(
        Page,
        null=True,
        blank=False,
        related_name='+',
        verbose_name=_("Zugehörige Seite"),
    )
    panels = [
        PageChooserPanel('related_page'),
    ]

    class Meta:
        abstract = True
        verbose_name = _("Zugehörige Seite")
        verbose_name_plural = _("Zugehörige Seiten")


class StandardPageRelatedPage(Orderable, RelatedPage):
    page = ParentalKey(Page, related_name='related_pages')


class StandardPage(BasePage):
    """
    simple "just a page"
    basis for most other pages
    """
    body = StreamField(
        StandardStreamBlock(),
        blank=True,
        verbose_name=_("Inhalt"),
    )

    search_fields = BasePage.search_fields + (
        index.SearchField('body'),
    )

    content_panels = BasePage.content_panels + [
        StreamFieldPanel('body'),
        InlinePanel('related_pages', label=_("Zugehöriges")),
    ]

    class Meta:
        verbose_name = _("Einfache Seite")
        verbose_name_plural = _("Einfache Seiten")


class HomePage(BasePage):
    """
    The HomePage or startpage
    (gets created by a migration)
    """
    is_creatable = False

    class Meta:
        verbose_name = _("Startseite")

    def get_context(self, request):
        context = super().get_context(request)
        # get the last three highlighted articles
        # TODO: include events
        context['highlights'] = Article.objects.filter(highlight=True) \
            .live().order_by('-first_published_at')[:3]
        return context


class ArticleIndexPage(BasePage):
    """
    lists articles
    """
    subpage_types = ['Article']
    parent_page_types = ['HomePage']

    class Meta:
        verbose_name = _("Auflistung von Artikeln")

    def get_context(self, request):
        context = super().get_context(request)
        context['articles'] = Article.objects.child_of(self) \
            .live().order_by('-first_published_at')
        return context


class Article(StandardPage):
    """
    An Article
    """
    subpage_types = []
    parent_page_types = ['ArticleIndexPage']

    highlight = models.BooleanField(
        _("Highlight"),
        help_text="Ist dies ein ge-highlighteter Artikel? Falls ja, "
                  "taucht es z.B. auf der Startseite auf.",
        default=False
    )

    main_image = models.ForeignKey(
        Image,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='+',
        verbose_name=_("Hauptbild"),
        help_text=_("Bild, das den Artikel repräsentiert. "
                    "Wird in Übersichten verwendet.")
    )

    search_fields = StandardPage.search_fields + (
        index.SearchField('highlight'),
        index.FilterField('first_published_at'),
        index.FilterField('latest_revision_created_at'),
    )

    content_panels = [
        FieldPanel('title', classname="full title"),

        ImageChooserPanel('main_image'),
        StreamFieldPanel('body'),
    ]

    related_panels = [
        InlinePanel('related_pages', label=_("Zugehöriges")),
    ]

    settings_panels =  [
        FieldPanel('highlight'),
    ] + Page.promote_panels + Page.settings_panels

    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading=_("Inhalt")),
        ObjectList(related_panels, heading=_("Zugehöriges")),
        ObjectList(settings_panels, heading=_("Einstellungen"),
                   classname="settings"),
    ])

    class Meta:
        verbose_name = _("Artikel")
        verbose_name_plural = _("Artikel")


class EventIndexPage(BasePage):
    """
    lists events
    """
    subpage_types = ['EventPage']
    parent_page_types = ['HomePage']

    class Meta:
        verbose_name = _("Auflistung von Veranstaltungen")
        verbose_name_plural = _("Auflistungen von Veranstaltungen")

    def get_context(self, request):
        context = super().get_context(request)
        now = timezone.localtime(timezone.now())
        context['upcoming'] = EventPage.objects.child_of(self) \
            .live().filter(start_datetime__gte=now).order_by('start_datetime')
        return context


class EventPage(StandardPage):
    subpage_types = []
    parent_page_types = ['EventIndexPage']

    highlight = models.BooleanField(
        _("Highlight"),
        help_text="Ist dies eine ge-highlightete Veranstaltung? "
                  "Falls ja, taucht es z.B. auf der Startseite auf.",
        default=False
    )

    main_image = models.ForeignKey(
        Image,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='+',
        verbose_name=_("Hauptbild"),
        help_text=_("Bild, das die Veranstaltung repräsentiert. "
                    "Wird in Übersichten verwendet.")
    )

    start_datetime = models.DateTimeField(_("Startzeit"))
    end_datetime = models.DateTimeField(
        _("Endzeit"),
        null=True,
        blank=True,
    )

    subpage_types = []
    parent_page_types = ['EventIndexPage']

    search_fields = StandardPage.search_fields + (
        index.SearchField('highlight'),
        index.SearchField('date_from'),
        index.SearchField('date_to'),
        index.FilterField('time_from'),
        index.FilterField('time_to'),
        index.FilterField('first_published_at'),
        index.FilterField('latest_revision_created_at'),
    )

    time_panels = [
        FieldPanel('start_datetime'),
        FieldPanel('end_datetime'),
    ]

    title_panels = [
        FieldPanel('title', classname="full title"),
        FieldPanel('highlight'),
        ImageChooserPanel('main_image'),
    ]

    content_panels = [
        StreamFieldPanel('body'),
    ]

    sidebar_content_panels = [
        InlinePanel('related_pages', label=_("Zugehöriges")),
    ]

    edit_handler = TabbedInterface([
        ObjectList(title_panels, heading=_("Titel")),
        ObjectList(time_panels, heading=_("Zeit")),
        ObjectList(content_panels, heading=_("Inhalt")),
        ObjectList(sidebar_content_panels, heading=_("Nebenbei")),
        ObjectList(Page.promote_panels, heading=_("Promotion")),
        ObjectList(Page.settings_panels, heading=_("Einstellungen"),
                   classname="settings"),
    ])

    class Meta:
        verbose_name = _("Veranstaltung")
        verbose_name_plural = _("Veranstaltungen")
