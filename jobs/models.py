from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator
from django import forms

from wagtail.admin.edit_handlers import (
    FieldPanel,
    StreamFieldPanel,
    MultiFieldPanel,
    HelpPanel,
)
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.core.fields import StreamField
from wagtail.search import index

from core.blocks import StandardStreamBlock
from core.models import BasePage, StandardPage

from .fields import ChoiceArrayField


class JobOfferIndexPage(BasePage):
    subpage_types = ["JobOfferPage"]
    max_count = 1

    heading = models.CharField("Überschrift", max_length=255, blank=True)
    highlight_in_heading = models.CharField(
        "Hervorhebungen in der Überschrift",
        help_text="Wiederhole Text aus der Überschrift der farblich hervorgehoben werden soll",
        blank=True,
        max_length=255,
    )
    subtitle = models.CharField("Untertitel", max_length=255, blank=True)

    before_jobs = StreamField(
        StandardStreamBlock,
        blank=True,
        verbose_name="Intro-Text (wenn Jobs vorhanden)",
        help_text="Wird als Text vor der Liste der Stellenanzeigen angezeigt. Aber nur wenn es auch Stellenanzeigen gibt.",
    )

    after_jobs = StreamField(
        StandardStreamBlock,
        blank=True,
        verbose_name="Outro-Text (wenn Jobs vorhanden)",
        help_text="Wird als Text nach der Liste der Stellenanzeigen angezeigt. Aber nur wenn es auch Stellenanzeigen gibt.",
    )

    empty = StreamField(
        StandardStreamBlock(),
        blank=True,
        null=True,
        verbose_name="Wenn keine Jobs",
        help_text="Wird angezeigt, wenn es keine Stellenanzeigen gibt.",
    )

    def get_context(self, request):
        context = super().get_context(request)
        context["jobs"] = JobOfferPage.objects.all().live()
        return context

    search_fields = BasePage.search_fields + [
        index.SearchField("heading"),
        index.SearchField("subtitle"),
        index.SearchField("before_jobs"),
        index.SearchField("after_jobs"),
    ]

    content_panels = [
        MultiFieldPanel(
            [
                FieldPanel("title"),
                FieldPanel("heading"),
                FieldPanel("highlight_in_heading"),
                FieldPanel("subtitle"),
            ],
            "Kopf",
        ),
        StreamFieldPanel("before_jobs"),
        HelpPanel(
            template="jobs/admin_add_job_button.html",
            heading="Stellenauschreibung erstellen",
        ),
        StreamFieldPanel("after_jobs"),
        StreamFieldPanel("empty"),
    ]

    class Meta:
        verbose_name = "Auflistung von Stellenausschreibungen"
        verbose_name_plural = "Auflistungen von Stellenausschreibungen"


class JobOfferPage(StandardPage):
    parent_page_types = ["JobOfferIndexPage"]
    subpage_types = ["core.StandardPage"]

    valid_through = models.DateTimeField(
        "Bewerbungsfrist",
        blank=True,
        null=True,
        validators=[
            MinValueValidator(timezone.now, message="Sollte in der Zukunft liegen")
        ],
    )
    job_title = models.CharField("Job-Titel", max_length=255)
    job_location = models.CharField(
        "Job-Ort", max_length=255, blank=True, default="Hannover"
    )
    hiring_organization_name = models.CharField(
        "Arbeitgeber", max_length=255, default="JANUN e.V."
    )
    hiring_organization_url = models.URLField(
        "Website des Arbeitgebers", blank=True, default="https://www.janun.de/"
    )
    EMPLOYMENT_TYPE_CHOICES = [
        ("FULL_TIME", "Vollzeit"),
        ("PART_TIME", "Teilzeit"),
        ("CONTRACTOR", "Auftragnehmer"),
        ("TEMPORARY", "befristet"),
        ("INTERN", "Praktikum"),
        ("VOLUNTEER", "Freiwilligendienst"),
        ("PER_DIEM", "tageweise"),
        ("OTHER", "anderes"),
    ]
    employment_type = ChoiceArrayField(
        models.CharField(max_length=20, choices=EMPLOYMENT_TYPE_CHOICES),
        verbose_name="Art der Anstellung",
        blank=True,
        null=True,
    )
    base_salary_amount = models.DecimalField(
        "Grundgehalt", blank=True, null=True, decimal_places=2, max_digits=10
    )
    BASE_SALARY_UNIT_CHOICES = [
        ("HOUR", "pro Stunde"),
        ("DAY", "pro Tag"),
        ("WEEK", "pro Woche"),
        ("MONTH", "pro Monat"),
        ("YEAR", "pro Jahr"),
    ]
    base_salary_unit = models.CharField(
        "Zeitraum für Grundgehalt",
        max_length=10,
        default="MONTH",
        choices=BASE_SALARY_UNIT_CHOICES,
    )
    auto_unpublish = models.BooleanField(
        "Automatisch depublizieren",
        help_text="Depubliziert die Seite automatisch nach der Bewerbungsfrist",
        default=True,
    )

    def get_employment_type_display(self) -> [str]:
        result = []
        for employment_type in self.employment_type:
            for choice in self.EMPLOYMENT_TYPE_CHOICES:
                if employment_type == choice[0]:
                    result.append(choice[1])
        return result

    @property
    def structured_data(self):
        return {
            "@type": "JobPosting",
            "title": self.job_title,
            "description": str(self.body),
            "datePosted": self.first_published_at,
            "validThrough": self.valid_through,
            "hiringOrganization": {
                "@type": "Organization",
                "name": self.hiring_organization_name,
                "sameAs": self.hiring_organization_url,
            },
            "jobLocation": {"@type": "Place", "address": self.job_location},
            "employmentType": self.employment_type,
            "baseSalary": {
                "@type": "MonetaryAmount",
                "currency": "EUR",
                "value": {
                    "@type": "QuantitativeValue",
                    "value": self.base_salary_amount,
                    "unitText": self.base_salary_unit,
                },
            },
        }

    def save(self, *args, **kwargs):
        if self.valid_through and self.auto_unpublish:
            self.expire_at = self.valid_through
        super().save(*args, **kwargs)

    content_panels = [
        FieldPanel("title"),
        FieldPanel("subtitle"),
        ImageChooserPanel("feed_image"),
        MultiFieldPanel(
            [
                HelpPanel(
                    "<p>Sorgt für eine bessere Platzierung als Jobanzeige bei Google und co.</p>"
                ),
                FieldPanel("job_title"),
                FieldPanel("job_location"),
                FieldPanel("hiring_organization_name"),
                FieldPanel("hiring_organization_url"),
                FieldPanel("valid_through"),
                FieldPanel("auto_unpublish"),
                FieldPanel("employment_type", widget=forms.CheckboxSelectMultiple),
                FieldPanel("base_salary_amount"),
                FieldPanel("base_salary_unit"),
            ],
            heading="Infos",
        ),
        StreamFieldPanel("body"),
    ]

    class Meta:
        verbose_name = "Stellenausschreibung"
        verbose_name_plural = "Stellenausschreibungen"
