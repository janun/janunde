from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from modelcluster.fields import ParentalKey
from wagtail.wagtailadmin.edit_handlers import (FieldPanel, InlinePanel,
                                                MultiFieldPanel,
                                                FieldRowPanel,
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
    """dummy trans

    TODO: real translation?
    """
    return str


class BasePage(Page):
    """basic functionality for all our pages

    Every page has a (short) partial and a medium partial template:
     * The short partial can be used for listings where object density is high.
     * The medium partial gives more insight into the content of the page.
    """
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


class Group(BasePage):
    # title is auto added
    class Meta:
        verbose_name = _("Gruppe")
        verbose_name_plural = _("Gruppen")


class GroupIndexPage(BasePage):
    # title is auto added
    subpage_types = ['Group']
    parent_page_types = ['HomePage']

    class Meta:
        verbose_name = _("Auflistung von Gruppen")

    def get_context(self, request):
        context = super().get_context(request)
        context['groups'] = Group.objects.child_of(self).live()
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

    related_group = models.ForeignKey(
        Group,
        null=True,
        blank=True,
        related_name='articles',
        on_delete=models.SET_NULL,
        verbose_name=_("Zugehörige Gruppe"),
        help_text=_("Eine JANUN-Gruppe, die diesem Artikel zugeordnet ist")
    )

    search_fields = StandardPage.search_fields + (
        index.SearchField('highlight'),
        index.FilterField('first_published_at'),
        index.FilterField('latest_revision_created_at'),
    )

    content_panels = [
        FieldPanel('title', classname='full title'),
        ImageChooserPanel('main_image'),
        StreamFieldPanel('body'),
    ]

    related_panels = [
        FieldPanel('related_group', 'core.Group'),
        InlinePanel('related_pages', label=_("Zugehörige Seiten")),
    ]

    settings_panels =  [
        FieldPanel('highlight'),
    ] + Page.promote_panels + Page.settings_panels

    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading=_("Inhalt")),
        ObjectList(related_panels, heading=_("Zugehöriges")),
        ObjectList(settings_panels, heading=_("Einstellungen"),
                   classname='settings'),
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


class EventPage(Page):
    """
    represents an event
    """
    subpage_types = []
    parent_page_types = ['EventIndexPage']

    main_image = models.ForeignKey(
        Image,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='+',
        verbose_name=_("Poster"),
        help_text=_("Poster oder Bild für diese Veranstaltung."
                    "Bitte kein Gruppen- oder JANUN-Logo!")
    )
    start_datetime = models.DateTimeField(_("Startzeit"))
    end_datetime = models.DateTimeField(_("Endzeit"),
                                        null=True,
                                        blank=True)
    related_group = models.ForeignKey(
        Group,
        null=True,
        blank=True,
        related_name='event_pages',
        on_delete=models.SET_NULL,
        verbose_name=_("Zugehörige Gruppe"),
        help_text=_("Eine JANUN-Gruppe, "
                    "die dieser Veranstaltung zugeordnet ist")
    )
    facebook_event_url = models.URLField(
        _("Facebook Event"),
        help_text=_("Die URL zum Facebook-Event dieser Veranstaltung"),
        null=True,
        blank=True,
        # TODO: validation so its only a Facebook Event URL
    )
    website_url = models.URLField(
        _("externe Website"),
        help_text=_("Die URL einer externen Website zu dieser Veranstaltung"),
        null=True,
        blank=True,
    )
    contact_mail = models.EmailField(
        _("Kontakt E-Mail"),
        help_text=_("Die E-Mail-Adresse, "
                    "um Kontakt für diese Veranstaltung aufzunehmen"),
        null=True,
        blank=True,
    )
    content = StreamField(
        StandardStreamBlock(),
        blank=True,
        verbose_name=_("Inhalt"),
    )
    COLOR_CHOICES = (
        ('rgb(70, 187, 0)', _("Grün")),
        ('rgb(196, 23, 55)', _("Rot")),
        ('rgb(0, 118, 164)', _("Blau")),
        ('rgb(233, 88, 34)', _("Orange")),
    )
    color = models.CharField(
        _("Farbe"),
        help_text=_("Farbe, die diese Veranstaltung bekommt, "
                    "falls kein Poster angegeben ist."),
        choices=COLOR_CHOICES,
        null=True,
        blank=True,
        max_length=18
        # TODO: Validation: Must be present if no main_image
    )
    location = models.CharField(
        _("Ort"),
        help_text=_("Ort, an dem die Veranstaltung stattfindet"),
        max_length=255,
        # TODO: change this into a real location somehow
    )

    search_fields = BasePage.search_fields + (
        #title is in here by default
        index.SearchField('content'),
        index.SearchField('start_datetime'),
        index.SearchField('end_datetime'),
        index.FilterField('first_published_at'),
        index.FilterField('latest_revision_created_at'),
    )

    edit_handler = TabbedInterface([
        ObjectList([
            FieldPanel('title', classname="full title"),
            StreamFieldPanel('content'),
        ], heading=_("Titel und Inhalt")),
        ObjectList([
            MultiFieldPanel(
                [
                    FieldPanel('start_datetime'),
                    FieldPanel('end_datetime'),
                ],
                classname="",
                heading="Datum"
            ),
            FieldPanel('location'),
            MultiFieldPanel(
                [
                    FieldPanel('contact_mail'),
                    FieldPanel('website_url'),
                    FieldPanel('facebook_event_url')
                ],
                heading="Links und E-Mail",
                classname="collapsible collapsed"
            )
        ], heading=_("Datum, Ort und Links")),
        ObjectList([
            ImageChooserPanel('main_image'),
            FieldPanel('color'),
        ], heading=_("Poster und Gestaltung")),
    ])

    partial_template_name = 'core/_partial.html'
    medium_partial_template_name = 'core/_medium_partial.html'

    class Meta:
        verbose_name = _("Veranstaltung")
        verbose_name_plural = _("Veranstaltungen")
