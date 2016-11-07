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
from wagtail.wagtailcore.models import Orderable, Page, PageManager
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
            models.Q(highlighted_page__live=True),
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
        'contact.PersonPage',
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
    ]

    settings_panels = [
        FieldPanel('author'),
    ] + BasePage.settings_panels

    promote_panels = [
        InlinePanel(
            'highlight',
            label=_("Highlight"),
            help_text="""Du kannst diese Seite highlighten.
                         Sie wird dann für den angegeben Zeitraum
                         auf der Startseite angezeigt."""
        ),
    ] + BasePage.promote_panels

    def get_image(self):
        for block in self.body:
            if block.block_type == 'image':
                return block.value['image']

    def get_description(self):
        if self.search_description:
            return self.search_description
        from django.utils.html import strip_tags
        for block in self.body:
            if block.block_type == 'paragraph':
                return strip_tags(block.value.source)

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
        from events.models import EventPage

        highlights = Highlight.objects.active()
        context['highlights'] = highlights[:6]

        upcoming_events = EventPage.objects.upcoming().exclude(
            pk__in=[h.highlighted_page.pk for h in highlights]
        )
        context['upcoming_events'] = upcoming_events[:3]
        context['more_upcoming_events'] = upcoming_events.count() > 3

        articles = Article.objects.live().exclude(
            pk__in=[h.highlighted_page.pk for h in highlights]
        )
        context['articles'] = articles[:3]
        context['more_articles'] = articles.count() > 3
        return context


    edit_handler = TabbedInterface([
        ObjectList([
            FieldPanel('title', classname="full title"),
        ], heading=_("Inhalt"))
    ])


class Group(BasePage):
    # title is auto added

    body = StreamField(
        StandardStreamBlock(),
        blank=True,
        verbose_name=_("Inhalt"),
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

    def get_image(self):
        return self.logo

    edit_handler = TabbedInterface([
        ObjectList([
            FieldPanel('title', classname="full title"),
            ImageChooserPanel('logo'),
            StreamFieldPanel('body'),
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
        verbose_name = _("Sammlung von Artikeln")

    def get_context(self, request):
        context = super().get_context(request)
        context['articles'] = Article.objects.child_of(self) \
            .live().order_by('-first_published_at')
        return context



class ArticleManager(PageManager):
    def get_queryset(self):
         return super().get_queryset().order_by('first_published_at')


class Article(StandardPage):
    """
    An Article
    """
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

    @property
    def partial_template_name(self):
        return "core/_article.html"

    def get_image(self):
        return self.main_image

    def get_description(self):
        if self.search_description:
            return self.search_description
        from django.utils.html import strip_tags
        for block in self.body:
            if block.block_type == 'paragraph':
                return strip_tags(block.value.source)

    related_group = models.ForeignKey(
        Group,
        null=True,
        blank=True,
        related_name='articles',
        on_delete=models.SET_NULL,
        verbose_name=_("Zugehörige Gruppe"),
        help_text=_("Eine JANUN-Gruppe, die diesem Artikel zugeordnet ist")
    )

    content_panels = [
        MultiFieldPanel([
            FieldPanel('title', classname='title'),
            FieldPanel('title_color', classname=''),
        ], heading="Titel"),        ImageChooserPanel('main_image'),
        FieldPanel('subtitle'),
        StreamFieldPanel('body'),
        FieldPanel('tags'),
    ]

    promote_panels = [
        FieldPanel('related_group', 'core.Group'),
    ] + StandardPage.promote_panels

    settings_panels = [
    ] + StandardPage.settings_panels


    objects = ArticleManager()

    class Meta:
        verbose_name = _("Artikel")
        verbose_name_plural = _("Artikel")
