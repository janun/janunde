import datetime

from django.core.files.images import ImageFile
from django.core.exceptions import ValidationError
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.core.mail import EmailMessage
from django.db import models
from django.db.models import Q
from django.http import Http404, HttpResponse
from django.utils import timezone
from django.utils.text import Truncator
from django.shortcuts import render
from django.template.loader import render_to_string

from wagtail.admin.edit_handlers import (
    FieldPanel,
    MultiFieldPanel,
    ObjectList,
    StreamFieldPanel,
    TabbedInterface,
    FieldRowPanel,
)
from wagtail.admin.widgets import AdminDateTimeInput
from wagtail.core.fields import StreamField
from wagtail.core.models import Page, PageManager
from wagtail.core.rich_text import RichText
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.documents.edit_handlers import DocumentChooserPanel
from wagtail.documents.models import Document
from wagtail.search import index

from phonenumber_field.modelfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberInternationalFallbackWidget

import html2text

from urllib.parse import quote

from events.forms import SeminarForm
from core.blocks import StandardStreamBlock
from core.fields import FacebookEventURLField, PrettyURLField
from core.images import AttributedImage as Image
from core.models import BasePage, Group, HeaderMixin
from core.forms import ShortTitleForm
from core.models import HyphenatedTitleMixin

from .utils import export_event_to_ical, export_event_to_google_link


class SeminarFormPage(BasePage):
    subpage_types = []
    parent_page_types = ["events.EventIndexPage"]

    description = StreamField(
        StandardStreamBlock(), blank=True, verbose_name="Erklärung",
    )

    richtlinie = models.ForeignKey(
        Document,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
        verbose_name="Seminarabrechnungsrichtlinie",
        help_text="Wird im Formular verlinkt",
    )

    datenschutz = models.ForeignKey(
        Document,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
        verbose_name="Datenschutzbedingungen",
        help_text="Wird im Formular verlinkt",
    )

    content_panels = [
        FieldPanel("title"),
        StreamFieldPanel("description"),
        DocumentChooserPanel("richtlinie"),
        DocumentChooserPanel("datenschutz"),
    ]

    class Meta:
        verbose_name = "Formular zur Seminaranmeldung"

    def create_event(self, data, image=None):
        event_index = EventIndexPage.objects.all()[0]
        event = EventPage(
            title=data["title"],
            subtitle=data["subtitle"],
            start_datetime=data["begin"],
            end_datetime=data["end"],
            location=data["location"],
            contact_name=data["website_contact_name"],
            contact_mail=data["website_contact_mail"],
            contact_phone=data["website_contact_phone"],
            related_group=data["group"],
            content=[("paragraph", RichText(data["description"]))],
        )
        if image:
            image_object = Image(
                title="Bild für " + data["title"],
                file=ImageFile(image),
                attribution=data["image_copyright"],
            )
            image_object.save()
            event.main_image = image_object
        event_index.add_child(instance=event)
        event.unpublish()
        event.save_revision(submitted_for_moderation=True)
        return event

    def serve(self, request):
        if request.method == "POST":
            form = SeminarForm(
                request.POST,
                request.FILES,
                richtlinie=self.richtlinie,
                datenschutz=self.datenschutz,
            )
            if form.is_valid():
                attachments = []
                image = None
                event = None
                if request.FILES:
                    image = request.FILES["image"]
                    attachments = [(image.name, image.read(), image.content_type)]

                if form.cleaned_data["publish"]:
                    event = self.create_event(form.cleaned_data, image)
                    form.cleaned_data["event"] = event

                EmailMessage(
                    subject="Antrag auf Förderung für %s" % form.cleaned_data["title"],
                    body=render_to_string(
                        "events/seminar_form_page/thankyou_mail.txt", form.cleaned_data
                    ),
                    from_email="website@janun.de",
                    to=[form.cleaned_data["contact_mail"]],
                    reply_to=["seminare@janun.de"],
                    attachments=attachments,
                ).send(fail_silently=True)

                EmailMessage(
                    subject="Antrag auf Förderung für %s" % form.cleaned_data["title"],
                    body=render_to_string(
                        "events/seminar_form_page/new_seminar_mail.txt",
                        form.cleaned_data,
                    ),
                    from_email="website@janun.de",
                    to=["seminare@janun.de"],
                    reply_to=[form.cleaned_data["contact_mail"]],
                    attachments=attachments,
                ).send(fail_silently=True)

                return render(
                    request,
                    "events/seminar_form_page/thankyou.html",
                    {"self": self, "form": form},
                )
        else:
            form = SeminarForm(richtlinie=self.richtlinie, datenschutz=self.datenschutz)

        return render(
            request,
            "events/seminar_form_page/apply.html",
            {"self": self, "form": form,},
        )


class EventIndexPage(BasePage, HeaderMixin):
    """
    lists events
    """

    subpage_types = ["EventPage", "SeminarFormPage"]
    parent_page_types = ["core.HomePage"]

    content_panels = [
        FieldPanel("title"),
        MultiFieldPanel(HeaderMixin.panels, "Header"),
    ]

    class Meta:
        verbose_name = "Auflistung von Veranstaltungen"
        verbose_name_plural = "Auflistungen von Veranstaltungen"

    def get_context(self, request):
        context = super().get_context(request)
        past = request.GET.get("past", None)
        q = request.GET.get("q", "")
        try:
            year = int(request.GET.get("year", None))
        except TypeError:
            year = None
        try:
            month = int(request.GET.get("month", None))
        except TypeError:
            month = None

        if q:
            events = (
                EventPage.objects.live()
                .order_by("-start_datetime")
                .search(q, order_by_relevance=False)
            )
            context["search_count"] = len(events)
            paginator = Paginator(events, 25)
            page = request.GET.get("page")
            try:
                events = paginator.page(page)
            except PageNotAnInteger:
                events = paginator.page(1)
            except EmptyPage:
                events = paginator.page(paginator.num_pages)
        elif past:
            events = EventPage.objects.expired().order_by("-start_datetime")
            context["months"] = events.dates("start_datetime", "month")
        else:
            events = EventPage.objects.upcoming()

        if year:
            events = events.filter(start_datetime__year=year)
            if month:
                events = events.filter(start_datetime__month=month)
                months = list(context["months"])
                month_index = months.index(datetime.date(year, month, 1))
                try:
                    context["next_month"] = months[month_index + 1]
                except IndexError:
                    context["next_month"] = None
                if month_index > 0:
                    try:
                        context["prev_month"] = months[month_index - 1]
                    except IndexError:
                        context["prev_month"] = None

        context["year"] = year
        context["month"] = month
        context["events"] = events
        context["past"] = past
        context["q"] = q
        return context

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


class EventPage(Page, HyphenatedTitleMixin):
    """
    represents an event
    """

    subpage_types = ["contact.PersonPage", "core.StandardPage"]
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
        related_name="event_pages",
        on_delete=models.SET_NULL,
        verbose_name="JANUN-Gruppe",
        help_text="JANUN-Gruppe, falls Veranstaltung vom JANUN-Netzwerk",
    )
    organizer = models.CharField(
        "Veranstalter",
        null=True,
        blank=True,
        help_text="externer Veranstalter, falls externe Veranstaltung",
        max_length=255,
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
    location_address = models.CharField(
        "Adresse",
        help_text="Straße, Hausnummer etc.",
        max_length=255,
        null=True,
        blank=True,
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

    partial_template_name = "events/_event_big.html"

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
        index.RelatedFields("related_group", [index.SearchField("title"),]),
    ]

    edit_handler = TabbedInterface(
        [
            ObjectList(
                [
                    FieldPanel("title", classname="full title"),
                    FieldPanel("subtitle", classname=""),
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
                            FieldPanel("location_address"),
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
                        [FieldPanel("organizer"), FieldPanel("related_group"),],
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
