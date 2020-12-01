from django.db import models

from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import (
    FieldPanel,
    StreamFieldPanel,
    MultiFieldPanel,
)
from wagtail.core.models import PageManager
from wagtail.images.edit_handlers import ImageChooserPanel


from core.images import AttributedImage as Image
from core.models import BasePage, StandardPage, Group


class GridCalendar(BasePage):

    subpage_types = ["CalendarEntry"]
    parent_page_types = ["core.HomePage"]

    main_image = models.ForeignKey(
        Image,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
        verbose_name="Bild für Übersichten",
        help_text="Bild, das den Artikel repräsentiert. Wird in Übersichten verwendet.",
    )

    heading = models.CharField("Überschrift", max_length=255)
    highlight_in_heading = models.CharField(
        "Hervorhebungen in der Überschrift",
        help_text="Wiederhole Text aus der Überschrift der farblich hervorgehoben werden soll",
        blank=True,
        max_length=255,
    )

    intro = RichTextField("Intro-Text", blank=True)

    show_placeholder_for_unpublished = models.BooleanField(
        "Zeige Platzhalter für unveröffentlichte Einträge",
        default=False,
        help_text="Normalerweise werden unveröffentlichte Einträge gar nicht angezeigt",
    )

    def get_description(self):
        return self.heading

    content_panels = [
        MultiFieldPanel(
            [
                FieldPanel("title"),
                FieldPanel("heading"),
                FieldPanel("highlight_in_heading"),
            ],
            heading="Titel",
        ),
        ImageChooserPanel("main_image"),
        FieldPanel("intro"),
        FieldPanel("show_placeholder_for_unpublished"),
    ]

    class Meta:
        verbose_name = "Kalender/Rasteransicht"

    def get_context(self, request):
        context = super().get_context(request)
        entries = CalendarEntry.objects.child_of(self)
        if not self.show_placeholder_for_unpublished:
            entries = entries.live()
        context["entries"] = entries
        return context


class CalendarEntry(StandardPage):
    parent_page_types = ["GridCalendar"]

    main_image = models.ForeignKey(
        Image,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
        verbose_name="Bild für Übersichten",
        help_text="Bild, das den Artikel repräsentiert. Wird in Übersichten verwendet.",
    )

    related_group = models.ForeignKey(
        Group,
        null=True,
        blank=True,
        related_name="gridcal_entries",
        on_delete=models.SET_NULL,
        verbose_name="Zugehörige Gruppe",
        help_text="Eine JANUN-Gruppe, die diesem Eintrag zugeordnet ist",
    )

    content_panels = [
        MultiFieldPanel(
            [FieldPanel("title", classname="title"), FieldPanel("subtitle")],
            heading="Titel",
        ),
        FieldPanel("related_group"),
        ImageChooserPanel("main_image"),
        StreamFieldPanel("body"),
    ]

    class Meta:
        verbose_name = "Kalendereintrag"
        verbose_name_plural = "Kalendereinträge"
