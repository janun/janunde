from wagtail.core.models import Page


class HomePage(Page):
    """
    The HomePage or startpage
    (gets created by a migration)
    """

    is_creatable = False

    class Meta:
        verbose_name = "Startseite"
