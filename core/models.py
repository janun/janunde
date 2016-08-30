from __future__ import unicode_literals

from django.db import models
from django.utils import timezone

from datetime import timedelta

from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey
from taggit.models import TaggedItemBase
from wagtail.wagtailadmin.edit_handlers import (FieldPanel, InlinePanel,
                                                ObjectList, PageChooserPanel,
                                                StreamFieldPanel, FieldRowPanel,
                                                TabbedInterface, MultiFieldPanel)
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailcore.models import Orderable, Page
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailsearch import index
from wagtail.wagtailsnippets.models import register_snippet
from wagtail.wagtailsnippets.edit_handlers import SnippetChooserPanel

from .blocks import StandardStreamBlock
from .images import AttributedImage as Image


COLOR_CHOICES = [
    ('brown', 'Braun'),
    ('green', 'Grün'),
    ('red', 'Rot'),
    ('blue', 'Blau'),
    ('orange', 'Orange'),
]


@register_snippet
class Person(models.Model):
    first_name = models.CharField("Vorname", max_length=255)
    last_name = models.CharField("Nachname", max_length=255, blank=True)
    photo = models.ForeignKey(
        Image,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    panels = [
        FieldPanel('first_name'),
        FieldPanel('last_name'),
        ImageChooserPanel('photo'),
    ]

    search_fields = [
        index.SearchField('first_name', partial_match=True),
        index.SearchField('last_name', partial_match=True),
    ]

    def __str__(self):
        return self.first_name + " " + self.last_name



# TODO: How can we create a Thema conveniently?
class Thema(models.Model):
    title = models.CharField(
        "Titel",
        max_length=255,
        null=True,
        blank=True,
    )  # TODO: default to tagname

    body = StreamField(
        StandardStreamBlock(),
        blank=True,
        verbose_name="Beschreibung",
    )

    tag = models.ForeignKey(
        'taggit.Tag',
        related_name='thema',
        # TODO: one to one (there should not be several thema to one tag)
    )


class JanunTag(TaggedItemBase):
    content_object = ParentalKey(Page, related_name='tagged_items')


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


class HighlightManager(models.Manager):
    def active(self):
        return self.get_queryset().filter(
            models.Q(start_datetime__lte=timezone.now()),
            models.Q(end_datetime__isnull=True) |
            models.Q(end_datetime__gt=timezone.now())
        )


def get_in_14_days():
    return timezone.now() + timedelta(days=14)

class Highlight(models.Model):
    """pages can be highlighted
       these can be shown on the homepage for example
       - a time interval can be set, during which the highlight will be shown
       - a custom title can be set, only for the highlighted view
    """
    highlighted_page = ParentalKey(Page, related_name='highlight')
    start_datetime = models.DateTimeField(
        "Startzeit",
        help_text="Ab wann soll das Highlight auftauchen?",
        default=timezone.now
    )
    end_datetime = models.DateTimeField(
        "Endzeit",
        help_text="Bis wann soll das Highlight auftauchen?",
        default=get_in_14_days
    )
    title_override = models.CharField(
        "Überschreib-Titel",
        help_text="Wird statt des Titels des Originals angezeigt.",
        max_length=255,
        blank=True,
    )

    def title():
        doc = "title"
        def fget(self):
            if self.title_override:
                return self.title_override
            else:
                return self.highlighted_page.title
        def fset(self, value):
            self.title_override = value
        def fdel(self):
            del self.title_override
        return locals()
    title = property(**title())

    objects = HighlightManager()


class StandardPage(BasePage):
    """
    simple "just a page"
    """
    title_color = models.CharField(
        "Titelfarbe",
        choices=COLOR_CHOICES,
        null=True,
        blank=True,
        max_length=255,
        default='brown',
        help_text="Der Titel wird in dieser Farbe angezeigt."
    )

    subtitle = models.CharField(
        "Untertitel",
        max_length=255,
        blank=True
    )

    body = StreamField(
        StandardStreamBlock(),
        blank=True,
        verbose_name=_("Inhalt"),
    )

    author = models.ForeignKey(
        'core.Person',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='pages',
        verbose_name="Autor_in",
    )

    tags = ClusterTaggableManager("Tags",
        through=JanunTag, blank=True,
        help_text=""
    )

    search_fields = BasePage.search_fields + [
        index.SearchField('body'),
    ]

    content_panels =  [
        MultiFieldPanel([
            FieldPanel('title', classname='title'),
            FieldPanel('title_color', classname=''),
        ], heading="Titel"),
        FieldPanel('subtitle'),
        StreamFieldPanel('body'),
        FieldPanel('tags'),
        SnippetChooserPanel('author'),
    ]

    promote_panels = [
        InlinePanel(
            'highlight',
            label=_("Highlight"),
            help_text="""Du kannst diese Seite highlighten.
                         Sie wird dann für den angegeben Zeitraum
                         auf der Startseite angezeigt."""
        ),
    ] + BasePage.promote_panels

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
        context['highlights'] = Highlight.objects.active() \
            .order_by('start_datetime')
        return context


class Group(BasePage):
    # title is auto added

    abbr = models.CharField(
        _("Abkürzung"),
        help_text=_("Nur zwei Zeichen"),
        max_length=2,
        null=True,
        blank=True,
    )

    logo = models.ForeignKey(
        Image,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='+',
        verbose_name=_("Logo"),
        # help_text=_("")
    )

    def clean(self):
        super().clean()
        if not self.abbr:
            self.abbr = self.title[:2]

    edit_handler = TabbedInterface([
        ObjectList([
            FieldPanel('title', classname="full title"),
            FieldPanel('abbr', classname=""),
            ImageChooserPanel('logo'),
        ], heading=_("Name und Logo"))
    ])

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

    search_fields = StandardPage.search_fields + [
        index.FilterField('first_published_at'),
        index.FilterField('latest_revision_created_at'),
    ]

    content_panels = [
        FieldPanel('title', classname='full title'),
        ImageChooserPanel('main_image'),
        StreamFieldPanel('body'),
    ]

    related_panels = [
        FieldPanel('related_group', 'core.Group'),
    ]

    settings_panels = [
        InlinePanel('highlight'),
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
