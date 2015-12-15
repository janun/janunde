from __future__ import unicode_literals

from django.db import models

from wagtail.wagtailcore.models import Page


class HomePage(Page):
    """The HomePage or startpage
    is intented to be 1x on a site
    It gets created automatically
    """
    is_creatable = False
