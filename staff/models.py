from django.db import models

from wagtail.core.fields import StreamField
from wagtail.admin.edit_handlers import (
    FieldPanel,
    StreamFieldPanel,
    RichTextField,
    HelpPanel,
    MultiFieldPanel,
)
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index

from phonenumber_field.modelfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberInternationalFallbackWidget

from core.images import AttributedImage as Image
from core.models import BasePage
from core.blocks import StandardStreamBlock


class Employee(BasePage):
    parent_page_types = ["StaffListing"]

    text = StreamField(
        StandardStreamBlock(required=False), null=True, blank=True, verbose_name="Text",
    )
    role = models.CharField("Rolle", max_length=255, blank=True)
    mail = models.EmailField("E-Mail", blank=True)
    phone = PhoneNumberField("Telefonnummer", blank=True)
    phone_hours = models.CharField(
        "Kommentar zu Telefonnummer",
        blank=True,
        max_length=255,
        help_text="Z.B. Erreichbarkeit",
    )

    DEPARTMENT_CHOICES = [
        ("ljb", "Landesbüro Hannover"),
        ("lgb", "Landesbüro Lüneburg"),
        ("goe", "Landesbüro Göttingen"),
        ("old", "Landesbüro Oldenburg"),
        ("brueter", "Vorstand (Brüter)"),
    ]
    department = models.CharField(
        "Abteilung", choices=DEPARTMENT_CHOICES, default="ljb", max_length=255
    )

    photo = models.ForeignKey(
        Image, null=True, blank=True, on_delete=models.SET_NULL, related_name="+"
    )

    search_fields = BasePage.search_fields + [
        index.SearchField("text"),
        index.SearchField("mail"),
        index.SearchField("role"),
    ]

    content_panels = [
        FieldPanel("title"),
        ImageChooserPanel("photo"),
        FieldPanel("department"),
        FieldPanel("role"),
        FieldPanel("mail"),
        MultiFieldPanel(
            [
                FieldPanel("phone", widget=PhoneNumberInternationalFallbackWidget),
                FieldPanel("phone_hours"),
            ],
            heading="Telefon",
        ),
        StreamFieldPanel("text"),
    ]

    class Meta:
        verbose_name = "Mitarbeiter*in"
        verbose_name_plural = "Mitarbeiter*innen"


class StaffListing(BasePage):
    subpage_types = ["Employee"]
    max_count = 1

    heading = models.CharField(
        "Überschrift", max_length=50, default="Mitarbeiter*innen"
    )
    intro = RichTextField("Intro", blank=True)
    image = models.ForeignKey(
        Image,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
        verbose_name="Bild",
    )
    outro = RichTextField("Outro", blank=True)

    content_panels = [
        FieldPanel("title"),
        FieldPanel("heading"),
        FieldPanel("intro"),
        ImageChooserPanel("image"),
        HelpPanel(
            "An dieser Stelle kommen die Mitarbeiter*innen, die als Unterseiten angelegt sind.",
            heading="Mitarbeiter*innen",
        ),
        FieldPanel("outro"),
    ]

    class Meta:
        verbose_name = "Auflistung von Mitarbeiter*innen"
        verbose_name_plural = "Auflistungen von Mitarbeiter*innen"

    def get_context(self, request):
        context = super().get_context(request)
        context["people"] = []
        for department_db, department in Employee.DEPARTMENT_CHOICES:
            people = Employee.objects.filter(department=department_db).order_by("title")
            if people:
                context["people"].append({"department": department, "people": people})
        return context
