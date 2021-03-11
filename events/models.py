import datetime
from urllib.parse import quote

from django.core.exceptions import ValidationError
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import models
from django.db.models import Q
from django import forms
from django.http import Http404, HttpResponse
from django.utils import timezone
from django.utils.text import Truncator

from wagtail.admin.edit_handlers import (
    FieldPanel,
    MultiFieldPanel,
    ObjectList,
    StreamFieldPanel,
    TabbedInterface,
    FieldRowPanel,
    PageChooserPanel,
    InlinePanel,
)
from wagtail.admin.widgets import AdminDateTimeInput
from wagtail.core.fields import StreamField
from wagtail.core.models import Page, PageManager
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index
from wagtail.snippets.models import register_snippet

from modelcluster.fields import ParentalManyToManyField, ParentalKey

from phonenumber_field.modelfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberInternationalFallbackWidget

import html2text

from core.blocks import StandardStreamBlock
from core.fields import FacebookEventURLField, PrettyURLField
from core.images import AttributedImage as Image
from core.models import BasePage, Group
from core.forms import ShortTitleForm
from core.models import HyphenatedTitleMixin

from .utils import export_event_to_ical, export_event_to_google_link


class EventIndexPage(BasePage):
    """
    lists events
    """

    subpage_types = ["EventPage"]
    parent_page_types = ["core.HomePage"]
    max_count_per_parent = 1

    heading = models.CharField("Überschrift", max_length=255)

    content_panels = [
        FieldPanel("title"),
        FieldPanel("heading"),
    ]

    class Meta:
        verbose_name = "Auflistung von Veranstaltungen"
        verbose_name_plural = "Auflistungen von Veranstaltungen"

    def get_context(self, request):
        context = super().get_context(request)
        past = request.GET.get("past", None)
        typ = request.GET.get("typ", None)
        q = request.GET.get("q", "").strip()
        try:
            year = int(request.GET.get("year", None))
        except TypeError:
            year = None
        try:
            month = int(request.GET.get("month", None))
        except TypeError:
            month = None

        # search /w pagination
        if q:
            events = EventPage.objects.live().order_by("-start_datetime")
            if typ:
                events = events.filter(event_type__name=typ)
            events = events.search(q, order_by_relevance=False)

            context["search_count"] = len(events)
            paginator = Paginator(events, 25)
            page = request.GET.get("page")
            try:
                events = paginator.page(page)
            except PageNotAnInteger:
                events = paginator.page(1)
            except EmptyPage:
                events = paginator.page(paginator.num_pages)

        # past events
        elif past:
            events = EventPage.objects.expired().order_by("-start_datetime")
            if typ:
                events = events.filter(event_type__name=typ)
            if events:
                context["months"] = events.dates("start_datetime", "month")
                months = list(context["months"])
                if not year or not month:
                    year = months[-1].year
                    month = months[-1].month
                events = events.filter(
                    start_datetime__year=year, start_datetime__month=month
                )

        # upcoming events
        else:
            events = EventPage.objects.upcoming()
            if typ:
                events = events.filter(event_type__name=typ)

        # get next/previous possible month
        if past and year and month and events:
            first_of_month = datetime.date(year, month, 1)
            if first_of_month in months:
                month_index = months.index(first_of_month)
                try:
                    context["next_month"] = months[month_index + 1]
                except IndexError:
                    context["next_month"] = None
                try:
                    context["prev_month"] = months[month_index - 1]
                except IndexError:
                    context["prev_month"] = None

        context["year"] = year
        context["month"] = month
        context["events"] = events
        context["past"] = past
        context["q"] = q

        context["types"] = (
            EventType.objects.filter(seminars__isnull=False).order_by("name").distinct()
        )
        context["active_type"] = typ
        return context

    @property
    def last_change(self) -> datetime.datetime:
        try:
            last_child = EventPage.objects.live().latest("last_published_at")
        except EventPage.DoesNotExist:
            last_child = None
        if last_child and last_child.last_published_at > self.last_published_at:
            return last_child.last_published_at
        return self.last_published_at

    def get_sitemap_urls(self, request=None) -> list:
        """https://docs.wagtail.io/en/v2.9/reference/contrib/sitemaps.html"""
        return [
            {
                "location": self.get_full_url(request),
                "lastmod": self.last_change,
                "changefreq": "daily",
            }
        ]

    def get_description(self):
        if self.search_description:
            return self.search_description
        return "Veranstaltungen bei JANUN"


class EventPageManager(PageManager):
    def get_queryset(self):
        return super().get_queryset().order_by("start_datetime")

    def upcoming(self):
        now = timezone.now()
        return (
            self.get_queryset()
            .live()
            .filter(Q(start_datetime__date__gte=now) | Q(end_datetime__date__gte=now))
        )

    def expired(self):
        now = timezone.now()
        return (
            self.get_queryset()
            .live()
            .filter(Q(start_datetime__date__lt=now) | Q(end_datetime__date__lt=now))
        )


class EventPageForm(ShortTitleForm):
    class Media:
        css = {"all": ("events/css/admin-location-form.css",)}
        js = ("events/js/admin-location-form.js",)


@register_snippet
class EventType(models.Model):
    name = models.CharField("Name", max_length=255)

    panels = [
        FieldPanel("name"),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Veranstaltungsart"
        verbose_name_plural = "Veranstaltungsarten"


class EventPageGroup(models.Model):
    """model that saves the relation from EventPages to Groups, showing a PageChooserPanel"""

    eventpage = ParentalKey(
        "events.EventPage", on_delete=models.CASCADE, related_name="related_groups"
    )
    group = models.ForeignKey(
        "core.Group", on_delete=models.CASCADE, related_name="event_pages"
    )

    panels = [
        PageChooserPanel("group"),
    ]

    class Meta:
        unique_together = ("eventpage", "group")


class EventPage(Page, HyphenatedTitleMixin):
    """
    represents an event
    """

    subpage_types = ["core.StandardPage", "core.FormPage"]
    parent_page_types = ["EventIndexPage"]
    base_form_class = EventPageForm
    og_type = "article"

    subtitle = models.CharField(
        verbose_name="Untertitel", max_length=255, null=True, blank=True,
    )

    main_image = models.ForeignKey(
        Image,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
        verbose_name="Bild",
        help_text="Bitte kein Gruppen- oder JANUN-Logo!",
    )
    start_datetime = models.DateTimeField("Startzeit",)
    end_datetime = models.DateTimeField("Endzeit", null=True, blank=True)
    all_day = models.BooleanField("ganztägig", default=False)
    related_group = models.ForeignKey(
        Group,
        null=True,
        blank=True,
        related_name="+",
        on_delete=models.SET_NULL,
        verbose_name="JANUN-Gruppe",
        help_text="(alt)",
    )
    organizer = models.CharField(
        "Veranstalter",
        null=True,
        blank=True,
        help_text="Name des externen Veranstalters, falls externe Veranstaltung",
        max_length=255,
    )
    event_type = ParentalManyToManyField(
        EventType,
        blank=True,
        related_name="seminars",
        verbose_name="Art der Veranstaltung",
    )
    facebook_event_url = FacebookEventURLField("Facebook-Event", null=True, blank=True,)
    website_url = PrettyURLField(
        "externe Website",
        help_text="z.B. auf der Veranstalter-Homepage",
        null=True,
        blank=True,
    )
    contact_mail = models.EmailField("E-Mail", null=True, blank=True,)
    contact_name = models.CharField("Name", max_length=255, null=True, blank=True,)
    contact_phone = PhoneNumberField("Telefonnummer", null=True, blank=True,)
    content = StreamField(StandardStreamBlock(), blank=True, verbose_name="Inhalt",)
    location = models.CharField(
        "Ort", help_text="Altes Ortsfeld", max_length=255, null=True, blank=True,
    )
    location_name = models.CharField(
        "Name",
        help_text="Name des Veranstaltungsortes",
        max_length=255,
        null=True,
        blank=True,
    )
    location_address = models.TextField(
        "Adresse", help_text="Straße, Hausnummer etc.", null=True, blank=True,
    )
    location_postcode = models.CharField(
        "Postleitzahl", max_length=255, null=True, blank=True
    )
    location_city = models.CharField("Stadt", max_length=255, null=True, blank=True)
    location_country = models.CharField("Land", max_length=255, null=True, blank=True)

    register_url = PrettyURLField(
        "Link zu Anmelde-Formular",
        help_text="z.B. auf der externen Seite oder bei einem Formularservice",
        null=True,
        blank=True,
    )

    @property
    def related_group_names(self):
        return ", ".join(
            [pagegroup.group.title for pagegroup in self.related_groups.all()]
        )

    @property
    def start(self):
        start = timezone.localtime(self.start_datetime)
        if self.all_day:
            return start.date()
        return start

    @property
    def end(self):
        if not self.end_datetime:
            return None
        end = timezone.localtime(self.end_datetime)
        if self.all_day:
            return end.date()
        return end

    @property
    def multipledays(self):
        if not self.end:
            return False
        if self.all_day:
            if self.start != self.end:
                return True
        else:
            if self.start.date() != self.end.date():
                return True
        return False

    def get_address(self, with_name=True) -> str:
        address_components = [
            self.location_name if with_name else None,
            self.location_address,
            "%s %s" % (self.location_postcode or "", self.location_city or ""),
            self.location_country,
        ]
        components = filter(bool, address_components)
        address = (", ".join(components)).strip()
        return address

    address = property(get_address)

    @property
    def googlemaps(self) -> str:
        if self.address:
            return "https://www.google.de/maps/search/%s" % quote(self.address)
        elif self.location:
            return "https://www.google.de/maps/search/%s" % quote(self.location)
        return None

    @property
    def openstreetmap(self) -> str:
        if self.address:
            return "https://www.openstreetmap.org/search?query=%s" % quote(
                self.get_address(with_name=False)
            )
        elif self.location:
            return "https://www.openstreetmap.org/search?query=%s" % quote(
                self.location
            )
        return None

    @property
    def month(self):
        """The 1st of month of the month the event is starting in"""
        return datetime.date(self.start_datetime.year, self.start_datetime.month, 1)

    objects = EventPageManager()

    def get_image(self):
        return self.main_image

    def get_description(self):
        if self.search_description:
            return self.search_description
        if self.subtitle:
            return self.subtitle
        h = html2text.HTML2Text()
        h.ignore_links = True
        for block in self.content:
            if block.block_type == "paragraph":
                text = h.handle(block.value.source)
                return Truncator(text).words(25)

    def clean(self):
        # append number to slug if already in use
        i = 2
        slug = self.slug
        while not Page._slug_is_available(slug, self.get_parent(), self):
            slug = "-".join([self.slug, str(i)])
            i += 1
        self.slug = slug

        super().clean()

        # end_datetime
        if self.end_datetime:
            if self.end_datetime < self.start_datetime:
                raise ValidationError(
                    {"end_datetime": "Endzeit muss nach Startzeit liegen."}
                )

        # get fallback image
        if not self.main_image:
            self.main_image = (
                Image.objects.filter(tags__name="event-fallback").order_by("?").first()
            )

        # there must not be organizer and related_group
        if self.organizer and self.related_group:
            raise ValidationError(
                {"organizer": "Veranstalter oder JANUN-Gruppe, nicht beides."}
            )

    search_fields = BasePage.search_fields + [
        # title is in here by default
        index.FilterField("start_datetime"),  # enables sorting
        index.SearchField("subtitle"),
        index.SearchField("content"),
        index.SearchField("location"),
        index.SearchField("location_name"),
        index.SearchField("location_address"),
        index.SearchField("location_city"),
        index.SearchField("location_country"),
        index.SearchField("organizer"),
        # index.RelatedFields("related_groups", [index.SearchField("title"),]),
        index.RelatedFields("event_type", [index.SearchField("name"),]),
    ]

    edit_handler = TabbedInterface(
        [
            ObjectList(
                [
                    FieldPanel("title", classname="full title"),
                    FieldPanel("subtitle", classname=""),
                    FieldPanel("event_type", widget=forms.CheckboxSelectMultiple),
                    StreamFieldPanel("content"),
                ],
                heading="Titel und Inhalt",
            ),
            ObjectList(
                [
                    MultiFieldPanel(
                        [
                            FieldPanel(
                                "start_datetime",
                                widget=AdminDateTimeInput(format="%d.%m.%Y %H:%M"),
                            ),
                            FieldPanel(
                                "end_datetime",
                                widget=AdminDateTimeInput(format="%d.%m.%Y %H:%M"),
                            ),
                            FieldPanel("all_day"),
                        ],
                        classname="",
                        heading="Datum",
                    ),
                    MultiFieldPanel(
                        [
                            # FieldPanel("location"),
                            FieldPanel("location_name"),
                            FieldPanel(
                                "location_address",
                                widget=forms.Textarea(attrs={"rows": 2}),
                            ),
                            FieldRowPanel(
                                [
                                    FieldPanel("location_postcode"),
                                    FieldPanel("location_city"),
                                ]
                            ),
                            FieldPanel("location_country"),
                        ],
                        heading="Ort",
                        classname="location-panel",
                    ),
                    MultiFieldPanel(
                        [FieldPanel("website_url"), FieldPanel("facebook_event_url")],
                        heading="Links",
                    ),
                ],
                heading="Datum, Ort, Links",
            ),
            ObjectList([ImageChooserPanel("main_image"),], heading="Bild"),
            ObjectList(
                [
                    MultiFieldPanel(
                        [
                            FieldPanel("organizer"),
                            InlinePanel("related_groups", label="JANUN-Gruppe"),
                        ],
                        heading="Veranstalter",
                    ),
                    MultiFieldPanel(
                        [
                            FieldPanel("contact_name"),
                            FieldPanel("contact_mail"),
                            FieldPanel(
                                "contact_phone",
                                widget=PhoneNumberInternationalFallbackWidget,
                            ),
                        ],
                        heading="Kontakt",
                    ),
                    FieldPanel("register_url"),
                ],
                heading="Veranstalter, Kontakt",
            ),
        ]
    )

    def serve(self, request):
        if "format" in request.GET:
            if request.GET["format"] == "ical":
                # Export to ical format
                response = HttpResponse(
                    export_event_to_ical(self), content_type="text/calendar",
                )
                response["Content-Disposition"] = (
                    "attachment; filename="
                    + self.slug.encode("ascii", errors="replace").decode()
                    + ".ics"
                )
                return response
            else:
                raise Http404
        else:
            # Display event page as usual
            return super(EventPage, self).serve(request)

    def create_google_calendar_link(self):
        return export_event_to_google_link(self)

    class Meta:
        verbose_name = "Veranstaltung"
        verbose_name_plural = "Veranstaltungen"
