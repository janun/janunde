import datetime

from dateutil import relativedelta
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q
from django.http import Http404, HttpResponse
from django.utils import timezone
from modelcluster.contrib.taggit import ClusterTaggableManager
from wagtail.wagtailadmin.edit_handlers import (FieldPanel, MultiFieldPanel,
                                                ObjectList, StreamFieldPanel,
                                                TabbedInterface,
                                                InlinePanel)
from wagtail.wagtailadmin.widgets import AdminDateTimeInput
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailcore.models import Page, PageManager, PageQuerySet
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailsearch import index

from core.blocks import StandardStreamBlock
from core.fields import FacebookEventURLField, PrettyURLField
from core.images import AttributedImage as Image
from core.models import BasePage, Group, JanunTag, HeaderMixin
from phonenumber_field.modelfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberInternationalFallbackWidget


def split_on_condition(list, func):
    list1 = []
    list2 = []
    for item in list:
        if func(item):
            list1.append(item)
        else:
            list2.append(item)
    return list1, list2


class EventIndexPage(BasePage, HeaderMixin):
    """
    lists events
    """
    subpage_types = ['EventPage']
    parent_page_types = ['core.HomePage']

    def get_add_mail(self):
        from .utils import get_add_mail
        return get_add_mail()

    content_panels = [
        FieldPanel('title'),
        MultiFieldPanel(HeaderMixin.panels, "Header"),
    ]

    class Meta:
        verbose_name = "Auflistung von Veranstaltungen"
        verbose_name_plural = "Auflistungen von Veranstaltungen"

    def get_context(self, request):
        context = super().get_context(request)
        today = timezone.localtime(timezone.now()).date()
        context['now'] = timezone.localtime(timezone.now())
        context['thisyear'] = today.year

        end_of_this_week = today + datetime.timedelta(days=6 - today.weekday())

        end_of_next_week = today + datetime.timedelta(
            days=6 - today.weekday() + 7
        )

        begin_of_this_month = datetime.date(today.year, today.month, 1)
        end_of_this_month = begin_of_this_month + \
            relativedelta.relativedelta(months=1) - datetime.timedelta(days=1)

        # search stuff
        search_query = request.GET.get('query', None)
        search = request.GET.get('search', 0)

        # empty query= url param
        if 'query' in request.GET:
            search = 1

        # query= url param given
        if search_query:
            events = EventPage.objects.all().live().search(
                search_query, operator="and", order_by_relevance=False
            )
            context['search_query'] = search_query
            search = 1
        else:
            events = EventPage.objects.upcoming()

        context['search'] = search
        context['events'] = events

        context['past'], events = split_on_condition(
            events,
            lambda event: event.start_datetime.date() < today
        )

        # compute the events for this week
        def get_this_week(events):
            return list(filter(
                lambda event: timezone.localtime(event.start_datetime).date() <= end_of_this_week,
                events
            ))

        # try splitting off today, so this_week is not longer than 3 events
        if len(get_this_week(events)) > 3:
            context['today'], events = split_on_condition(
                events,
                lambda event: event.start_datetime.date() == today
            )

        # try splitting off tomorrow
        if len(get_this_week(events)) > 3:
            context['tomorrow'], events = split_on_condition(
                events,
                lambda event: event.start_datetime.date() ==
                today + datetime.timedelta(days=1)
            )

        # try splitting off each day of the remaining week
        next_day = today + datetime.timedelta(days=1)
        i = 0
        context['days_of_this_week'] = []
        while len(get_this_week(events)) > 3:
            events_next_day, events = split_on_condition(
                events,
                lambda event: event.start_datetime.date() == next_day
            )
            if events_next_day:
                context['days_of_this_week'].append(
                    [next_day, events_next_day]
                )
            next_day += datetime.timedelta(days=1)
            i += 1
            if i > 20:
                break

        # what is left for this week
        context['this_week'], events = split_on_condition(
            events,
            lambda event: timezone.localtime(event.start_datetime).date() <= end_of_this_week
        )

        context['next_week'], events = split_on_condition(
            events,
            lambda event: event.start_datetime.date() <= end_of_next_week
        )

        context['later_this_month'], events = split_on_condition(
            events,
            lambda event: event.start_datetime.date() <= end_of_this_month
        )

        def get_end_of_month(date):
            return date + relativedelta.relativedelta(months=1) + \
                datetime.timedelta(days=-1)

        def get_this_year(events):
            return list(filter(
                lambda event: event.start_datetime.date() <
                datetime.date(today.year+1, 1, 1),
                events
            ))

        # try splitting off month by month to keep after short
        begin_next_month = end_of_this_month + datetime.timedelta(days=1)
        i = 0
        context['by_month'] = []
        while len(events) > 4:
            events_next_month, events = split_on_condition(
                events,
                lambda event: event.start_datetime.date() <=
                get_end_of_month(begin_next_month)
            )
            if events_next_month:
                context['by_month'].append(
                    [begin_next_month, events_next_month]
                )
            begin_next_month += relativedelta.relativedelta(months=1)
            i += 1
            if i > 20:
                break

        context['after'] = events
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
        return self.get_queryset().filter(
            Q(start_datetime__date__gte=now) |
            Q(end_datetime__date__gte=now, late_attendence=True),
        )

    def expired(self):
        now = timezone.now()
        return self.get_queryset().filter(
            Q(end_datetime__date__lt=now) |
            Q(start_datetime__date__lt=now, late_attendence=False),
        )


class EventPage(Page):
    """
    represents an event
    """
    subpage_types = []
    parent_page_types = ['EventIndexPage']

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

    objects = EventPageManager()

    def get_image(self):
        return self.main_image

    def get_description(self):
        if self.search_description:
            return self.search_description
        from django.utils.html import strip_tags
        for block in self.content:
            if block.block_type == 'paragraph':
                return strip_tags(block.value.source)

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

        # title must be short
        if len(self.title) > 56:
            raise ValidationError({
                'title':
                "Der Titel ist zu lang. Er darf maximal 56 Zeichen "
                "lang sein. Nutz doch den Untertitel."
            })

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
                    self.slug + '.ics'
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
