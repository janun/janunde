from __future__ import unicode_literals

import datetime
import re
from dateutil import relativedelta

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q
from django.utils import timezone
from django.utils.http import urlquote
from django.http import (HttpResponse, Http404)

from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager

from taggit.models import TaggedItemBase

from wagtail.wagtailadmin.edit_handlers import (FieldPanel, InlinePanel,
                                                MultiFieldPanel,
                                                FieldRowPanel,
                                                ObjectList, PageChooserPanel,
                                                StreamFieldPanel,
                                                TabbedInterface)
from wagtail.wagtailadmin.widgets import AdminDateTimeInput
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailcore.models import Orderable, Page
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailsearch import index


from .blocks import StandardStreamBlock
from .images import AttributedImage as Image
from .fields import (PrettyURLField, FacebookEventURLField)



# TODO: How can we create a Thema conveniently?
class Thema(models.Model):
    title = models.CharField(
        "Titel",
        max_length=255,
        null=True,
        blank=True,
    ) # TODO: default to tagname

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

    tags = ClusterTaggableManager(through=JanunTag, blank=True)

    search_fields = BasePage.search_fields + [
        index.SearchField('body'),
    ]

    content_panels = BasePage.content_panels + [
        StreamFieldPanel('body'),
        FieldPanel('tags'),
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
        #help_text=_("")
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

    search_fields = StandardPage.search_fields + [
        index.SearchField('highlight'),
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
