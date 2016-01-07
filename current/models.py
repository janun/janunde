from django.db import models
from django.db.models import BooleanField

from wagtail.wagtailcore.models import Page
from wagtail.wagtailsearch import index
from wagtail.wagtailcore.fields import RichTextField, StreamField
from wagtail.wagtailcore import blocks
from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtailadmin.edit_handlers import FieldPanel, MultiFieldPanel, InlinePanel, StreamFieldPanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel


class Current(Page):
    """lists all current articles
    will be created automatically by migrations as child of homepage
    """
    class Meta:
        verbose_name = "Aktuelles"

    subpage_types = ['current.Article']
    is_creatable = False

    def get_context(self, request):
        context = super(Current, self).get_context(request)
        # get all non-highlighted articles
        context['articles'] = Article.objects.child_of(self).live()
        return context


class Article(Page):
    """An Article
    """
    class Meta:
        verbose_name = "Artikel"
        verbose_name_plural = "Artikel"

    body = StreamField([
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
    ], blank=True, help_text = "Inhalt des Artikels")

    highlight = BooleanField(
        "Highlight",
        help_text = "Falls ja, taucht es z.B. auf der Startseite auf."
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

    search_fields = Page.search_fields + (
        index.SearchField('body'),
        index.SearchField('highlight'),
        index.FilterField('first_published_at'),
        index.FilterField('latest_revision_created_at'),
    )

    content_panels = Page.content_panels + [
        FieldPanel('highlight'),
        ImageChooserPanel('main_image'),
        StreamFieldPanel('body'),
    ]

    parent_page_types = ['current.Current']
    subpage_types = []
