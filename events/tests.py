import datetime

from django.test import TestCase
from django.utils import timezone

from wagtail.core.models import Page

from .models import EventPage


class EventPageTestCase(TestCase):
    def setUp(self):
        homepage = Page.objects.get(title="Startseite")

        third_okt = timezone.make_aware(datetime.datetime(2016, 10, 3, 0, 1))
        homepage.add_child(
            instance=EventPage(
                title="3rd October", start_datetime=third_okt, all_day=True,
            )
        )
        self.whole_day_event = EventPage.objects.get(title="3rd October")

    def test_start_property(self):
        self.assertEqual(self.whole_day_event.start, datetime.date(2016, 10, 3))

    def test_short_times(self):
        pass
