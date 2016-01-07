from __future__ import unicode_literals

from django.db import models

from wagtail.wagtailcore.models import Page

from current.models import Article


class HomePage(Page):
    """The HomePage or startpage
    is intented to be 1x on a site
    It gets created automatically by migrations as child of root page
    """
    is_creatable = False

    class Meta:
        verbose_name = "Startseite"

    def get_context(self, request):
        context = super(HomePage, self).get_context(request)
        # get all highlighted articles
        context['highlights'] = Article.objects.filter(highlight=True).live()
        return context
