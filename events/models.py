import datetime

from itertools import groupby

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q
from django.http import Http404, HttpResponse
from django.utils import timezone
from modelcluster.contrib.taggit import ClusterTaggableManager
from wagtail.wagtailadmin.edit_handlers import (FieldPanel, MultiFieldPanel,
                                                ObjectList, StreamFieldPanel,
                                                TabbedInterface,
                                                InlinePanel, FieldRowPanel)
from wagtail.wagtailadmin.widgets import AdminDateTimeInput
from wagtail.wagtailcore.fields import StreamField, RichTextField
from wagtail.wagtailcore.models import Page, PageManager, PageQuerySet
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtaildocs.edit_handlers import DocumentChooserPanel
from wagtail.wagtaildocs.models import Document

from wagtail.wagtailsearch import index

from core.blocks import StandardStreamBlock
from core.fields import FacebookEventURLField, PrettyURLField
from core.images import AttributedImage as Image
from core.models import BasePage, Group, JanunTag, HeaderMixin
from phonenumber_field.modelfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberInternationalFallbackWidget

from wagtail.wagtailforms.models import AbstractEmailForm, AbstractFormField
from modelcluster.fields import ParentalKey
from django.shortcuts import render


class SeminarFormPage(BasePage):
    subpage_types = []
    parent_page_types = ['events.EventIndexPage']

    description = StreamField(
        StandardStreamBlock(),
        blank=True,
        verbose_name="Erklärung",
    )

    richtlinie = models.ForeignKey(
        Document,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='+',
        verbose_name="Seminarabrechnungsrichtlinie",
        help_text="Wird im Formular verlinkt"
    )

    content_panels = [
        FieldPanel('title'),
        StreamFieldPanel('description'),
        DocumentChooserPanel('richtlinie'),
    ]

    class Meta:
        verbose_name = "Formular zur Seminaranmeldung"

    def serve(self, request):
        from events.forms import SeminarForm

        if request.method == 'POST':
            form = SeminarForm(request.POST, request.FILES, richtlinie=self.richtlinie)
            if form.is_valid():
                from django.core.mail import send_mail, EmailMessage
                from django.template.loader import render_to_string
                attachments = []
                if request.FILES:
                    image = request.FILES['image']
                    attachments = [(image.name, image.read(), image.content_type)]
                    
                EmailMessage(
                    subject="Antrag auf Förderung für %s" % form.cleaned_data['title'],
                    body=render_to_string("events/seminar_form_page/thankyou_mail.txt", form.cleaned_data),
                    from_email='website@janun.de',
                    to=[form.cleaned_data['contact_mail']],
                    reply_to=["seminare@janun.de"],
                    attachments=attachments,
                ).send(fail_silently=True)

                EmailMessage(
                    subject="Antrag auf Förderung für %s" % form.cleaned_data['title'],
                    body=render_to_string("events/seminar_form_page/new_seminar_mail.txt", form.cleaned_data),
                    from_email='website@janun.de',
                    to=["seminare@janun.de"],
                    reply_to=[form.cleaned_data['contact_mail']],
                    attachments=attachments,
                ).send(fail_silently=True)

                return render(request, 'events/seminar_form_page/thankyou.html', {
                    'self': self,
                    'form': form
                })
        else:
            form = SeminarForm(richtlinie=self.richtlinie)

        return render(request, 'events/seminar_form_page/apply.html', {
            'self': self,
            'form': form,
        })


class EventIndexPage(BasePage, HeaderMixin):
    """
    lists events
    """
    subpage_types = ['EventPage', 'SeminarFormPage']
    parent_page_types = ['core.HomePage']

    content_panels = [
        FieldPanel('title'),
        MultiFieldPanel(HeaderMixin.panels, "Header"),
    ]

    class Meta:
        verbose_name = "Auflistung von Veranstaltungen"
        verbose_name_plural = "Auflistungen von Veranstaltungen"

    def get_context(self, request):
        context = super().get_context(request)

        # search stuff
        search_query = request.GET.get('query', None)
        search = request.GET.get('search', 0)

        # empty query= url param
        if 'query' in request.GET:
            search = 1

        # query= url param given
        if search_query:
            events = EventPage.objects.all().live().search(
                search_query#, operator="and", order_by_relevance=False
            )
            context['search_query'] = search_query
            search = 1
        else:
            events = EventPage.objects.upcoming()

        context['search'] = search
        context['events'] = events

        return context

    def get_description(self):
        if self.search_description:
            return self.search_description
        return "Veranstaltungen bei JANUN"


class EventPageManager(PageManager):

    def get_queryset(self):
         return super().get_queryset().order_by('start_datetime')

    def upcoming(self):
        now = timezone.now()
        return self.get_queryset().live().filter(
            Q(start_datetime__date__gte=now) |
            Q(end_datetime__date__gte=now, late_attendence=True),
        )

    def expired(self):
        now = timezone.now()
        return self.get_queryset().live().filter(
            Q(end_datetime__date__lt=now) |
            Q(start_datetime__date__lt=now, late_attendence=False),
        )


from core.forms import ShortTitleForm
from core.models import HyphenatedTitleMixin

# TODO: rebase this to PageBase
class EventPage(Page, HyphenatedTitleMixin):
    """
    represents an event
    """
    subpage_types = []
    parent_page_types = ['EventIndexPage']
    base_form_class = ShortTitleForm
    og_type = 'article'

    event_page_tags = ClusterTaggableManager("Tags",
        through=JanunTag, blank=True,
        help_text=""
    )

    subtitle = models.CharField(
        verbose_name="Untertitel",
        max_length=255,
        null=True,
        blank=True,
    )

    main_image = models.ForeignKey(
        Image,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='+',
        verbose_name="Bild",
        help_text="Bitte kein Gruppen- oder JANUN-Logo!"
    )
    start_datetime = models.DateTimeField(
        "Startzeit",
    )
    end_datetime = models.DateTimeField(
        "Endzeit",
        null=True,
        blank=True
    )
    all_day = models.BooleanField(
        "ganztägig",
        default=False,
    )
    late_attendence = models.BooleanField(
        "späte Teilnahme möglich",
        help_text="Ist es auch möglich z.B. erst am zweiten Tag zu kommen?",
        default=False
    )
    related_group = models.ForeignKey(
        Group,
        null=True,
        blank=True,
        related_name='event_pages',
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
    facebook_event_url = FacebookEventURLField(
        "Facebook-Event",
        null=True,
        blank=True,
    )
    website_url = PrettyURLField(
        "externe Website",
        help_text="z.B. auf der Veranstalter-Homepage",
        null=True,
        blank=True,
    )
    contact_mail = models.EmailField(
        "E-Mail",
        null=True,
        blank=True,
    )
    contact_name = models.CharField(
        "Name",
        max_length=255,
        null=True,
        blank=True,
    )
    contact_phone = PhoneNumberField(
        "Telefonnummer",
        null=True,
        blank=True,
    )
    content = StreamField(
        StandardStreamBlock(),
        blank=True,
        verbose_name="Inhalt",
    )
    COLOR_CHOICES = (
        ('green', "Grün"),
        ('red', "Rot"),
        ('blue', "Blau"),
        ('orange', "Orange"),
    )
    color = models.CharField(
        "Farbe als Ersatz für Bild",
        help_text="Die Veranstaltung bekommt diese Farbe, "
                  "falls es kein Bild gibt.",
        choices=COLOR_CHOICES,
        null=True,
        blank=True,
        max_length=18
        # TODO: Validation: Must be present if no main_image
    )
    location = models.CharField(
        "Ort",
        help_text="Ort, an dem die Veranstaltung stattfindet",
        max_length=255,
        null=True,
        blank=True,
        # TODO: change this into a real location somehow
    )
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
        from django.utils.text import Truncator
        import html2text
        h = html2text.HTML2Text()
        h.ignore_links = True
        for block in self.content:
            if block.block_type == 'paragraph':
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
                raise ValidationError({
                    'end_datetime':
                    "Endzeit muss nach Startzeit liegen."
                })

        # get fallback image
        if not self.main_image:
            self.main_image = Image.objects.filter(tags__name='event-fallback').order_by('?').first()

        # there must not be organizer and related_group
        if self.organizer and self.related_group:
            raise ValidationError({
                'organizer':"Veranstalter oder JANUN-Gruppe, nicht beides."
            })

    search_fields = BasePage.search_fields + [
        # title is in here by default
        index.SearchField('subtitle'),
        index.SearchField('content'),
        index.SearchField('location'),
        index.SearchField('organizer'),
        index.RelatedFields('related_group', [
            index.SearchField('title'),
        ]),
    ]

    edit_handler = TabbedInterface([
        ObjectList([
            FieldPanel('title', classname="full title"),
            FieldPanel('subtitle', classname=""),
            #FieldPanel('event_page_tags'),
            InlinePanel(
                'highlight',
                label="Highlight",
                help_text="""Du kannst diese Veranstaltung highlighten.
                             Sie wird dann für den angegeben Zeitraum
                             auf der Startseite angezeigt."""
            ),
            StreamFieldPanel('content'),
        ], heading="Titel und Inhalt"),
        ObjectList([
            MultiFieldPanel(
                [
                    FieldPanel(
                        'start_datetime',
                        widget=AdminDateTimeInput(format="%d.%m.%Y %H:%M")
                    ),
                    FieldPanel(
                        'end_datetime',
                        widget=AdminDateTimeInput(format="%d.%m.%Y %H:%M")
                    ),
                    FieldPanel('all_day'),
                    FieldPanel('late_attendence'),
                ],
                classname="",
                heading="Datum"
            ),
            FieldPanel('location'),
            MultiFieldPanel(
                [
                    FieldPanel('website_url'),
                    FieldPanel('facebook_event_url')
                ],
                heading="Links",
            )
        ], heading="Datum, Ort, Links"),
        ObjectList([
            ImageChooserPanel('main_image'),
            FieldPanel('color'),
        ], heading="Bild"),
        ObjectList([
            MultiFieldPanel([
                FieldPanel('organizer'),
                FieldPanel('related_group'),
            ], heading="Veranstalter"),
            MultiFieldPanel([
                FieldPanel('contact_name'),
                FieldPanel('contact_mail'),
                FieldPanel(
                    'contact_phone',
                    widget=PhoneNumberInternationalFallbackWidget
                ),
            ], heading="Kontakt"),
            FieldPanel('register_url'),
        ], heading="Veranstalter, Kontakt")
    ])

    def serve(self, request):
        if "format" in request.GET:
            if request.GET['format'] == 'ical':
                # Export to ical format
                from .utils import export_event_to_ical
                response = HttpResponse(
                    export_event_to_ical(self),
                    content_type='text/calendar',
                )
                response['Content-Disposition'] = 'attachment; filename=' + \
                    self.slug.encode("ascii", errors="replace").decode() + '.ics'
                return response
            else:
                raise Http404
        else:
            # Display event page as usual
            return super(EventPage, self).serve(request)

    def create_google_calendar_link(self):
        from .utils import export_event_to_google_link
        return export_event_to_google_link(self)

    class Meta:
        verbose_name = "Veranstaltung"
        verbose_name_plural = "Veranstaltungen"
