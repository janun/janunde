import datetime
import re
from dateutil import relativedelta
from django.utils import timezone
from django.db.models import Q

from django.db import models

from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailsearch import index
from wagtail.wagtailadmin.edit_handlers import (FieldPanel, InlinePanel,
                                                MultiFieldPanel,
                                                FieldRowPanel,
                                                ObjectList, PageChooserPanel,
                                                StreamFieldPanel,
                                                TabbedInterface)
from wagtail.wagtailadmin.widgets import AdminDateTimeInput
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel

from modelcluster.contrib.taggit import ClusterTaggableManager

from phonenumber_field.modelfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberInternationalFallbackWidget


from core.models import BasePage, JanunTag, Group
from core.images import AttributedImage as Image
from core.fields import (PrettyURLField, FacebookEventURLField)
from core.blocks import StandardStreamBlock


def split_on_condition(list, func):
    list1 = []
    list2 = []
    for item in list:
        if func(item):
            list1.append(item)
        else:
            list2.append(item)
    return list1, list2


class EventIndexPage(BasePage):
    """
    lists events
    """
    subpage_types = ['EventPage']
    parent_page_types = ['core.HomePage']

    def get_add_mail(self):
        from .utils import get_add_mail
        return get_add_mail()

    class Meta:
        verbose_name = "Auflistung von Veranstaltungen"
        verbose_name_plural = "Auflistungen von Veranstaltungen"

    def get_events(self):
        return EventPage.objects.child_of(self).live().order_by('start_datetime')

    def get_context(self, request):
        context = super().get_context(request)
        today = datetime.date.today()
        context['now'] = now = timezone.localtime(timezone.now())
        context['thisyear'] = today.year

        begin_of_this_week = today - datetime.timedelta(days=today.weekday())
        end_of_this_week = today + datetime.timedelta(days=6 - today.weekday())

        begin_of_next_week = today + datetime.timedelta(days=7-today.weekday())
        end_of_next_week = today + datetime.timedelta(days=6 - today.weekday() + 7)

        begin_of_this_month = datetime.date( today.year, today.month, 1 )
        end_of_this_month = begin_of_this_month + relativedelta.relativedelta(months=1) - datetime.timedelta(days=1)

        begin_of_next_month = begin_of_this_month + relativedelta.relativedelta(months=1)
        end_of_next_month = begin_of_next_month + relativedelta.relativedelta(months=1) - datetime.timedelta(days=1)


        events = self.get_events().filter(
            Q(start_datetime__gte=today) | Q(end_datetime__gte=today, late_attendence=True),
        )

        # search stuff
        search_query = request.GET.get('query', None)
        search = request.GET.get('search', 0)

        # empty query= url param
        if 'query' in request.GET:
            search = 1

        # query= url param given
        if search_query:
            events = events.search(search_query, operator="and", order_by_relevance=False)
            context['search_query'] = search_query
            search = 1

        context['search'] = search

        context['upcoming'] = upcoming = list(events)


        # compute the events for this week
        def get_this_week(upcoming):
            return list(filter(
                lambda event: event.start_datetime.date() <= end_of_this_week,
                upcoming
            ))

        # try splitting off today, so this_week is not longer than 3 events
        if len(get_this_week(upcoming)) > 3:
            context['today'], upcoming = split_on_condition(
                upcoming,
                lambda event: event.start_datetime.date() == today
            )

        # try splitting off tomorrow
        if len(get_this_week(upcoming)) > 3:
            context['tomorrow'], upcoming = split_on_condition(
                upcoming,
                lambda event: event.start_datetime.date() == today + datetime.timedelta(days=1)
            )

        # try splitting off each day of the remaining week
        next_day = today + datetime.timedelta(days=1)
        i = 0
        context['days_of_this_week'] = []
        while len(get_this_week(upcoming)) > 3:
            events_next_day, upcoming = split_on_condition(
                upcoming,
                lambda event: event.start_datetime.date() == next_day
            )
            if events_next_day:
                context['days_of_this_week'].append(
                    [next_day, events_next_day]
                )
            next_day += datetime.timedelta(days=1)
            i += 1
            if i > 20: break


        # what is left for this week
        context['this_week'], upcoming = split_on_condition(
            upcoming,
            lambda event: event.start_datetime.date() <= end_of_this_week
        )

        context['next_week'], upcoming = split_on_condition(
            upcoming,
            lambda event: event.start_datetime.date() <= end_of_next_week
        )

        context['later_this_month'], upcoming = split_on_condition(
            upcoming,
            lambda event: event.start_datetime.date() <= end_of_this_month
        )

        def get_end_of_month(date):
            return date + relativedelta.relativedelta(months=1) + datetime.timedelta(days=-1)

        def get_this_year(upcoming):
            return list(filter(
                lambda event: event.start_datetime.date() < datetime.date(today.year+1, 1, 1),
                upcoming
            ))

        # try splitting off month by month to keep after short
        begin_next_month = end_of_this_month + datetime.timedelta(days=1)
        i = 0
        context['by_month'] = []
        while len(upcoming) > 4:
            events_next_month, upcoming = split_on_condition(
                upcoming,
                lambda event: event.start_datetime.date() <= get_end_of_month(begin_next_month)
            )
            if events_next_month:
                context['by_month'].append(
                    [begin_next_month, events_next_month]
                )
            begin_next_month += relativedelta.relativedelta(months=1)
            i += 1
            if i > 20: break

        context['after'] = upcoming

        return context


class EventPage(Page):
    """
    represents an event
    """
    subpage_types = []
    parent_page_types = ['EventIndexPage']

    event_page_tags = ClusterTaggableManager(through=JanunTag, blank=True)

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
        verbose_name="Zugehörige JANUN-Gruppe",
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
        ('rgb(70, 187, 0)', "Grün"),
        ('rgb(196, 23, 55)', "Rot"),
        ('rgb(0, 118, 164)', "Blau"),
        ('rgb(233, 88, 34)', "Orange"),
    )
    color = models.CharField(
        "Farbe als Ersatz für Bild",
        help_text="Die Veranstaltung bekommt diese Farbe, falls es kein Bild gibt.",
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
            raise ValidationError({'title': "Der Titel ist zu lang. "
            "Er darf maximal 56 Zeichen lang sein. Nutz doch den Untertitel."})

        # end_datetime
        if self.end_datetime:
            if self.end_datetime < self.start_datetime:
                raise ValidationError({'end_datetime': "Endzeit muss nach Startzeit liegen."})


    # only works with ElasticSearch
    search_fields = BasePage.search_fields + [
        #title is in here by default
        index.SearchField('content'),
        index.SearchField('location'),
        index.RelatedFields('related_group', [
            index.SearchField('title'),
        ]),
        index.FilterField('start_datetime'),
        index.FilterField('end_datetime'),
        index.FilterField('late_attendence'),
    ]

    edit_handler = TabbedInterface([
        ObjectList([
            FieldPanel('title', classname="full title"),
            FieldPanel('subtitle', classname="full title"),
            FieldPanel('event_page_tags'),
            StreamFieldPanel('content'),
        ], heading="Titel und Inhalt"),
        ObjectList([
            MultiFieldPanel(
                [
                    FieldPanel('start_datetime',
                        widget=AdminDateTimeInput(format="%d.%m.%Y %H:%M")
                    ),
                    FieldPanel('end_datetime',
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
            FieldPanel('related_group'),
            MultiFieldPanel([
                FieldPanel('contact_name'),
                FieldPanel('contact_mail'),
                FieldPanel('contact_phone', widget=PhoneNumberInternationalFallbackWidget),
            ], heading="Kontakt"),
            FieldPanel('register_url'),
        ], heading="Gruppe, Kontakt, Anmeldung")
    ])

    partial_template_name = 'core/_partial.html'
    medium_partial_template_name = 'core/_medium_partial.html'

    def serve(self, request):
        if "format" in request.GET:
            if request.GET['format'] == 'ical':
                # Export to ical format
                from .utils import export_event_to_ical
                response = HttpResponse(
                    export_event_to_ical(self),
                    content_type='text/calendar',
                )
                response['Content-Disposition'] = 'attachment; filename=' + self.slug + '.ics'
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
