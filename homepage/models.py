from django.db import models

from wagtail.core.models import Page


class HomePage(Page):
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
