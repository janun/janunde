from django.db import models

from wagtail.wagtailcore.models import Page
from wagtail.wagtailsearch import index
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, MultiFieldPanel, InlinePanel
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
         # get all articles that are children
        context['articles'] = Article.objects.child_of(self).live()
        return context


class Article(Page):
    """An Article"""
    class Meta:
        verbose_name = "Artikel"

    body = RichTextField()

    search_fields = Page.search_fields + (
        index.SearchField('body'),
    )

    content_panels = Page.content_panels + [
        FieldPanel('body', classname="full"),
    ]

    parent_page_types = ['current.Current']
    subpage_types = []
