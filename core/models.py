from __future__ import unicode_literals

import datetime
import re
from dateutil import relativedelta
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q
from django.utils import timezone
from django.utils.http import urlquote
from django.http import (HttpResponse, Http404)
from modelcluster.fields import ParentalKey
from wagtail.wagtailadmin.edit_handlers import (FieldPanel, InlinePanel,
                                                MultiFieldPanel,
                                                FieldRowPanel,
                                                ObjectList, PageChooserPanel,
                                                StreamFieldPanel,
                                                TabbedInterface)
from wagtail.wagtailadmin.widgets import AdminDateTimeInput
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailcore.models import Orderable, Page
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailsearch import index
from phonenumber_field.modelfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberInternationalFallbackWidget

from .blocks import StandardStreamBlock
from .images import AttributedImage as Image
from .fields import (PrettyURLField, FacebookEventURLField)



def _(str):
    """dummy trans

    TODO: real translation?
    """
    return str


class BasePage(Page):
    """basic functionality for all our pages

    Every page has a (short) partial and a medium partial template:
     * The short partial can be used for listings where object density is high.
     * The medium partial gives more insight into the content of the page.
    """
    partial_template_name = 'core/_partial.html'
    medium_partial_template_name = 'core/_medium_partial.html'

    is_creatable = False


class RelatedPage(models.Model):
    """
    every stadardpage and descendants can have a related page (any page)
    """
    related_page = models.ForeignKey(
        Page,
        null=True,
        blank=False,
        related_name='+',
        verbose_name=_("Zugehörige Seite"),
    )
    panels = [
        PageChooserPanel('related_page'),
    ]

    class Meta:
        abstract = True
        verbose_name = _("Zugehörige Seite")
        verbose_name_plural = _("Zugehörige Seiten")


class StandardPageRelatedPage(Orderable, RelatedPage):
    page = ParentalKey(Page, related_name='related_pages')


class StandardPage(BasePage):
    """
    simple "just a page"
    """
    body = StreamField(
        StandardStreamBlock(),
        blank=True,
        verbose_name=_("Inhalt"),
    )

    search_fields = BasePage.search_fields + (
        index.SearchField('body'),
    )

    content_panels = BasePage.content_panels + [
        StreamFieldPanel('body'),
        InlinePanel('related_pages', label=_("Zugehöriges")),
    ]

    class Meta:
        verbose_name = _("Einfache Seite")
        verbose_name_plural = _("Einfache Seiten")


class HomePage(BasePage):
    """
    The HomePage or startpage
    (gets created by a migration)
    """
    is_creatable = False

    class Meta:
        verbose_name = _("Startseite")

    def get_context(self, request):
        context = super().get_context(request)
        # get the last three highlighted articles
        # TODO: include events
        context['highlights'] = Article.objects.filter(highlight=True) \
            .live().order_by('-first_published_at')[:3]
        return context


class Group(BasePage):
    # title is auto added

    abbr = models.CharField(
        _("Abkürzung"),
        help_text=_("Nur zwei Zeichen"),
        max_length=2,
        null=True,
        blank=True,
    )

    logo = models.ForeignKey(
        Image,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='+',
        verbose_name=_("Logo"),
        #help_text=_("")
    )

    def clean(self):
        super().clean()
        if not self.abbr:
            self.abbr = self.title[:2]

    edit_handler = TabbedInterface([
        ObjectList([
            FieldPanel('title', classname="full title"),
            FieldPanel('abbr', classname=""),
            ImageChooserPanel('logo'),
        ], heading=_("Name und Logo"))
    ])

    class Meta:
        verbose_name = _("Gruppe")
        verbose_name_plural = _("Gruppen")


class GroupIndexPage(BasePage):
    # title is auto added
    subpage_types = ['Group']
    parent_page_types = ['HomePage']

    class Meta:
        verbose_name = _("Auflistung von Gruppen")

    def get_context(self, request):
        context = super().get_context(request)
        context['groups'] = Group.objects.child_of(self).live()
        return context


class ArticleIndexPage(BasePage):
    """
    lists articles
    """
    subpage_types = ['Article']
    parent_page_types = ['HomePage']

    class Meta:
        verbose_name = _("Auflistung von Artikeln")

    def get_context(self, request):
        context = super().get_context(request)
        context['articles'] = Article.objects.child_of(self) \
            .live().order_by('-first_published_at')
        return context


class Article(StandardPage):
    """
    An Article
    """
    subpage_types = []
    parent_page_types = ['ArticleIndexPage']

    highlight = models.BooleanField(
        _("Highlight"),
        help_text="Ist dies ein ge-highlighteter Artikel? Falls ja, "
                  "taucht es z.B. auf der Startseite auf.",
        default=False
    )

    main_image = models.ForeignKey(
        Image,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='+',
        verbose_name=_("Hauptbild"),
        help_text=_("Bild, das den Artikel repräsentiert. "
                    "Wird in Übersichten verwendet.")
    )

    related_group = models.ForeignKey(
        Group,
        null=True,
        blank=True,
        related_name='articles',
        on_delete=models.SET_NULL,
        verbose_name=_("Zugehörige Gruppe"),
        help_text=_("Eine JANUN-Gruppe, die diesem Artikel zugeordnet ist")
    )

    search_fields = StandardPage.search_fields + (
        index.SearchField('highlight'),
        index.FilterField('first_published_at'),
        index.FilterField('latest_revision_created_at'),
    )

    content_panels = [
        FieldPanel('title', classname='full title'),
        ImageChooserPanel('main_image'),
        StreamFieldPanel('body'),
    ]

    related_panels = [
        FieldPanel('related_group', 'core.Group'),
        InlinePanel('related_pages', label=_("Zugehörige Seiten")),
    ]

    settings_panels =  [
        FieldPanel('highlight'),
    ] + Page.promote_panels + Page.settings_panels

    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading=_("Inhalt")),
        ObjectList(related_panels, heading=_("Zugehöriges")),
        ObjectList(settings_panels, heading=_("Einstellungen"),
                   classname='settings'),
    ])

    class Meta:
        verbose_name = _("Artikel")
        verbose_name_plural = _("Artikel")


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
    parent_page_types = ['HomePage']

    def get_add_mail(self):
        from .utils import get_add_mail
        return get_add_mail()

    class Meta:
        verbose_name = _("Auflistung von Veranstaltungen")
        verbose_name_plural = _("Auflistungen von Veranstaltungen")

    def get_events(self):
        return EventPage.objects.child_of(self).live().order_by('start_datetime')

    def get_context(self, request):
        context = super().get_context(request)
        context['today'] = today = datetime.date.today()
        context['now'] = now = timezone.localtime(timezone.now())
        context['thisyear'] = today.year

        events = self.get_events()

        # search stuff
        search_query = request.GET.get('query', None)
        search = request.GET.get('search', 0)

        # empty query= url param
        if 'query' in request.GET:
            search = 1

        # query= url param given
        if search_query:
            events = events.search(search_query).get_queryset()
            context['search_query'] = search_query
            search = 1

        context['search'] = search


        begin_of_this_week = today - datetime.timedelta(days=today.weekday())
        end_of_this_week = today + datetime.timedelta(days=6 - today.weekday())

        begin_of_next_week = today + datetime.timedelta(days=7-today.weekday())
        end_of_next_week = today + datetime.timedelta(days=6 - today.weekday() + 7)

        begin_of_this_month = datetime.date( today.year, today.month, 1 )
        end_of_this_month = begin_of_this_month + relativedelta.relativedelta(months=1) - datetime.timedelta(days=1)

        begin_of_next_month = begin_of_this_month + relativedelta.relativedelta(months=1)
        end_of_next_month = begin_of_next_month + relativedelta.relativedelta(months=1) - datetime.timedelta(days=1)


        context['upcoming'] = upcoming = list(events.filter(
            Q(start_datetime__date__gte=today) | Q(end_datetime__date__gte=today, late_attendence=True),
        ))


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

        context['next_month'], upcoming = split_on_condition(
            upcoming,
            lambda event: event.start_datetime.date() <= end_of_next_month
        )

        def get_end_of_month(date):
            return date + relativedelta.relativedelta(months=1) + datetime.timedelta(days=-1)

        def get_this_year(upcoming):
            return list(filter(
                lambda event: event.start_datetime.date() < datetime.date(today.year+1, 1, 1),
                upcoming
            ))

        # try splitting off month by month to keep later_this_year short
        begin_next_month = end_of_next_month + datetime.timedelta(days=1)
        i = 0
        context['by_month'] = []
        while len(upcoming) > 4:
            events_next_month, upcoming = split_on_condition(
                upcoming,
                lambda event: event.start_datetime.date() <= get_end_of_month(begin_next_month)
            )
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

    subtitle = models.CharField(
        verbose_name=_("Untertitel"),
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
        verbose_name=_("Bild"),
        help_text=_("Bild für diese Veranstaltung. "
                    "Bitte kein Gruppen- oder JANUN-Logo!")
    )
    start_datetime = models.DateTimeField(
        _("Startzeit"),
    )
    end_datetime = models.DateTimeField(
        _("Endzeit"),
        null=True,
        blank=True
    )
    all_day = models.BooleanField(
        _("ganztägig"),
        default=False,
        help_text=_("Bei ganztägigen Veranstaltungen werden Uhrzeiten ignoriert."),
    )
    late_attendence = models.BooleanField(
        _("späte Teilnahme möglich"),
        help_text=_("Falls dies ein mehrtägiger Termin ist: "
                    "Ist es auch möglich z.B. erst am zweiten Tag zu kommen?"),
        default=False
    )
    related_group = models.ForeignKey(
        Group,
        null=True,
        blank=True,
        related_name='event_pages',
        on_delete=models.SET_NULL,
        verbose_name=_("Zugehörige Gruppe"),
        help_text=_("Eine JANUN-Gruppe, "
                    "die dieser Veranstaltung zugeordnet ist")
    )
    facebook_event_url = FacebookEventURLField(
        _("Facebook Event"),
        help_text=_("Die URL zum Facebook-Event dieser Veranstaltung"),
        null=True,
        blank=True,
    )
    website_url = PrettyURLField(
        _("externe Website"),
        help_text=_("Die URL einer externen Website zu dieser Veranstaltung"),
        null=True,
        blank=True,
    )
    contact_mail = models.EmailField(
        _("E-Mail"),
        help_text=_("Die E-Mail-Adresse, "
                    "um Kontakt für diese Veranstaltung aufzunehmen"),
        null=True,
        blank=True,
    )
    contact_name = models.CharField(
        _("Name"),
        max_length=255,
        null=True,
        blank=True,
    )
    contact_phone = PhoneNumberField(
        _("Telefonnummer"),
        null=True,
        blank=True,
    )
    content = StreamField(
        StandardStreamBlock(),
        blank=True,
        verbose_name=_("Inhalt"),
    )
    COLOR_CHOICES = (
        ('rgb(70, 187, 0)', _("Grün")),
        ('rgb(196, 23, 55)', _("Rot")),
        ('rgb(0, 118, 164)', _("Blau")),
        ('rgb(233, 88, 34)', _("Orange")),
    )
    color = models.CharField(
        _("Farbe"),
        help_text=_("Farbe, die diese Veranstaltung bekommt, "
                    "falls kein Poster angegeben ist."),
        choices=COLOR_CHOICES,
        null=True,
        blank=True,
        max_length=18
        # TODO: Validation: Must be present if no main_image
    )
    location = models.CharField(
        _("Ort"),
        help_text=_("Ort, an dem die Veranstaltung stattfindet"),
        max_length=255,
        null=True,
        blank=True,
        # TODO: change this into a real location somehow
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
    search_fields = BasePage.search_fields + (
        #title is in here by default
        index.SearchField('content'),
        index.SearchField('location'),
        index.RelatedFields('related_group', [
            index.SearchField('title'),
        ]),
    )

    edit_handler = TabbedInterface([
        ObjectList([
            FieldPanel('title', classname="full title"),
            FieldPanel('subtitle', classname="full title"),
            StreamFieldPanel('content'),
        ], heading=_("Titel und Inhalt")),
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
                heading="Links und E-Mail",
            )
        ], heading=_("Datum, Ort und Links")),
        ObjectList([
            ImageChooserPanel('main_image'),
            FieldPanel('color'),
        ], heading=_("Bild und Gestaltung")),
        ObjectList([
            FieldPanel('related_group'),
            MultiFieldPanel([
                FieldPanel('contact_name'),
                FieldPanel('contact_mail'),
                FieldPanel('contact_phone', widget=PhoneNumberInternationalFallbackWidget),
            ], heading="Kontakt")
        ], heading="Gruppe und Kontakt")
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
        verbose_name = _("Veranstaltung")
        verbose_name_plural = _("Veranstaltungen")
