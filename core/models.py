from __future__ import unicode_literals

from django.db import models
from wagtail.wagtailadmin.edit_handlers import (FieldPanel, InlinePanel,
                                                MultiFieldPanel,
                                                StreamFieldPanel)
from wagtail.wagtailcore import blocks
from wagtail.wagtailcore.fields import RichTextField, StreamField
from wagtail.wagtailcore.models import Page
from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailsearch import index


class HomePage(Page):
    """
    The HomePage or startpage
    (gets created by a migration)
    """
    is_creatable = False

    class Meta:
        verbose_name = "Startseite"

    def get_context(self, request):
        context = super(HomePage, self).get_context(request)
        # get all highlighted articles
        context['highlights'] = Article.objects.filter(highlight=True).live().order_by('-first_published_at')
        return context


class ImageBlock(ImageChooserBlock):
    class Meta:
        template = 'blocks/image.html'


class Current(Page):
    """
    lists all current articles
    """
    subpage_types = ['Article']
    parent_page_types = ['HomePage']

    class Meta:
        verbose_name = "Aktuelles"

    def get_context(self, request):
        context = super(Current, self).get_context(request)
        # get all non-highlighted articles
        context['articles'] = Article.objects.child_of(self).live().order_by('-first_published_at')
        return context


class Article(Page):
    """
    An Article
    """
    subpage_types = []
    parent_page_types = ['Current']

    subheading = models.CharField("optionale Unterüberschrift", max_length=255, blank=True, null=True)

    body = StreamField([
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageBlock()),
    ], blank=True, help_text = "Inhalt des Artikels")

    highlight = models.BooleanField(
        "Highlight",
        help_text = "Ist dies ein ge-highlighteter Artikel? Falls ja, taucht es z.B. auf der Startseite auf.",
        default=False
    )

    main_image = models.ForeignKey(
        'wagtailimages.Image',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='+',
        verbose_name="Hauptbild",
        help_text="Bild, das den Artikel repräsentiert. Wird in Übersichten verwendet."
    )

    dont_crop = models.BooleanField(
        "Hauptbild nicht abschneiden",
        help_text = "Normalerweise wird das Hauptbild beschnitten, um besser auf die Seite zu passen. Falls ja, wird das Seitenverhältnis des Hauptbildes beibehalten.",
        default=False
    )

    search_fields = Page.search_fields + (
        index.SearchField('subheading'),
        index.SearchField('body'),
        index.SearchField('highlight'),
        index.FilterField('first_published_at'),
        index.FilterField('latest_revision_created_at'),
    )

    content_panels = [
        MultiFieldPanel([
            FieldPanel('title'),
            FieldPanel('subheading'),
            FieldPanel('highlight'),
        ], heading="Titeleinstellungen"),

        MultiFieldPanel([
            ImageChooserPanel('main_image'),
            FieldPanel('dont_crop'),
        ], heading="Bildeinstellungen"),

        StreamFieldPanel('body'),
    ]

    class Meta:
        verbose_name = "Artikel"
        verbose_name_plural = "Artikel"
