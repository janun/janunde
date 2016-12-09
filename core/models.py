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

from core.fields import FacebookProfileURLField, PrettyURLField
from phonenumber_field.modelfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberInternationalFallbackWidget


from .blocks import StandardStreamBlock
from .images import AttributedImage as Image


COLOR_CHOICES = [
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
        ).order_by('-start_datetime')


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


class PublishedAtFromGoLiveAtMixin(object):
    """
    set the first_published_at date to the go_live_at
    attribute on live pages on save.
    Thus enabling editors to create pages in the past
    """

    def clean(self):
        super().clean()
        if self.live and self.go_live_at:
            self.first_published_at = self.go_live_at

    class Meta:
        abstract = True


class FallbackImageMixin(object):
    """
    of main_image_field is not set, set it to a random image,
    that's tagged with fallback_image_tag
    """
    main_image_field = "main_image"
    fallback_image_tag = ""

    def clean(self):
        super().clean()
        if not self.fallback_image_tag:
            self.fallback_image_tag = type(self).__name__.lower() + "-fallback"
        if not self.__getattribute__(self.main_image_field):
            self.__setattr__(
                self.main_image_field,
                Image.objects.filter(tags__name=self.fallback_image_tag).order_by('?').first()
            )

    class Meta:
        abstract = True


class HeaderMixin(models.Model):
    """
    A Page with big heading bar,
    containing a heading and a header_image
    typically for top-level pages

    templates of subclasses should include core/_pageheader.html
    """
    heading = models.CharField(
        "Überschrift",
        max_length=255,
        blank=True,
    )
    header_image = models.ForeignKey(
        Image,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='+',
        verbose_name="Header-Bild",
    )
    panels =  [
        FieldPanel('heading', classname='title'),
        ImageChooserPanel('header_image'),
    ]
    def get_image(self):
        if self.header_image:
            return self.header_image
    class Meta:
        abstract = True


class StandardPage(BasePage):
    """
    simple "just a page"
    """
    title_color = models.CharField(
        "Titelfarbe",
        choices=COLOR_CHOICES,
        max_length=255,
        default='green',
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

    tags = ClusterTaggableManager("Tags",
        through=JanunTag, blank=True,
        help_text=""
    )

    search_fields = BasePage.search_fields + [
        index.SearchField('subtitle'),
        index.SearchField('body'),
    ]

    content_panels =  [
        MultiFieldPanel([
            FieldPanel('title', classname='title'),
            FieldPanel('title_color', classname=''),
        ], heading="Titel"),
        FieldPanel('subtitle'),
        StreamFieldPanel('body'),
        #FieldPanel('tags'),
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


    def get_description(self):
        if self.search_description:
            return self.search_description
        return "JANUN ist das Jugendumweltnetzwerk Niedersachsen"


class GroupManager(PageManager):
    def get_queryset(self):
         return super().get_queryset().order_by('title')

class Group(BasePage):
    parent_page_types = ['GroupIndexPage', 'Group']
    subpage_types = ['Project', 'StandardPage', 'Group']
    # title is auto added

    subtitle = models.CharField("Untertitel",
        max_length=80,
        null=True,
        blank=True,
        help_text="Z.B. eine sehr kurze Beschreibung"
    )

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


    contact_mail = models.EmailField(
        "E-Mail",
        null=True,
        blank=True,
    )
    contact_name = models.CharField(
        "Name",
        max_length=255,
        null=True,
        blank=True,
    )
    contact_phone = PhoneNumberField(
        "Telefonnummer",
        null=True,
        blank=True,
    )
    facebook_url = FacebookProfileURLField(
        "Facebook-Profil",
        null=True,
        blank=True,
    )
    website = PrettyURLField(
        "externe Website",
        null=True,
        blank=True,
    )

    address = models.CharField(
        "Adresse",
        help_text="Adresse, an dem die Gruppe zu finden ist",
        max_length=255,
        null=True,
        blank=True,
        # TODO: change this into a real location somehow
    )

    objects = GroupManager()

    search_fields = BasePage.search_fields + [
        index.SearchField('subtitle'),
        index.SearchField('body'),
        index.SearchField('address'),
        index.SearchField('contact_mail'),
        index.SearchField('contact_name'),
        index.SearchField('website'),
    ]

    def get_image(self):
        return self.logo

    def get_description(self):
        if self.search_description:
            return self.search_description
        if self.subtitle:
            return self.subtitle
        from django.utils.html import strip_tags
        for block in self.body:
            if block.block_type == 'paragraph':
                return strip_tags(block.value.source)

    def get_parent_group(self):
        return Group.objects.parent_of(self).first()

    edit_handler = TabbedInterface([
        ObjectList([
            FieldPanel('title', classname="full title"),
            FieldPanel('subtitle'),
            ImageChooserPanel('logo'),
            FieldPanel('facebook_url'),
            FieldPanel('website'),
            FieldPanel('address'),
            MultiFieldPanel([
                FieldPanel('contact_name'),
                FieldPanel('contact_mail'),
                FieldPanel(
                    'contact_phone',
                    widget=PhoneNumberInternationalFallbackWidget
                ),
            ], heading="Kontakt"),

            StreamFieldPanel('body'),

        ], heading=_("Name und Logo"))
    ])

    partial_template_name = "core/_group.html"

    class Meta:
        verbose_name = _("Gruppe")
        verbose_name_plural = _("Gruppen")


class Project(Group):
    subpage_types = []
    parent_page_types = ['Group']

    objects = GroupManager()


class GroupIndexPage(BasePage, HeaderMixin):
    # title is auto added
    subpage_types = ['Group', 'Project']
    parent_page_types = ['HomePage']

    class Meta:
        verbose_name = _("Auflistung von Gruppen")

    def get_context(self, request):
        context = super().get_context(request)

        context['groups'] = Group.objects.child_of(self).live()

        country_group = Group.objects.filter(title="JANUN Landesbüro").first()
        if country_group:
            context['countrywide_projects'] = Project.objects.descendant_of(country_group).live()
            context['groups'] = context['groups'].exclude(pk=country_group.pk)
        else:
            context['countrywide_projects'] = []

        context['other_projects'] = Project.objects.descendant_of(self).live().exclude(
            pk__in=[p.pk for p in context['countrywide_projects']]
        )

        return context

    def get_description(self):
        if self.search_description:
            return self.search_description
        return "Auflistung aller JANUN-Gruppen"

    content_panels = [
        FieldPanel('title'),
        MultiFieldPanel(HeaderMixin.panels, "Header"),
    ]


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
        context['articles'] = Article.objects.child_of(self).live()
        return context

    def get_description(self):
        if self.search_description:
            return self.search_description
        return "Auflistung von Artikeln bei JANUN"



class ArticleManager(PageManager):
    def get_queryset(self):
         return super().get_queryset().order_by('-first_published_at')


class Article(FallbackImageMixin, PublishedAtFromGoLiveAtMixin, StandardPage):
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

    author = models.ForeignKey(
        'contact.PersonPage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='pages',
        verbose_name="Autor_in",
    )

    content_panels = [
        MultiFieldPanel([
            FieldPanel('title', classname='title'),
            FieldPanel('title_color', classname=''),
        ], heading="Titel"),
        FieldPanel('subtitle'),
        FieldPanel('author'),
        ImageChooserPanel('main_image'),
        StreamFieldPanel('body'),
        #FieldPanel('tags'),
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
