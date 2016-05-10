from django.test import TestCase


class BasicTestCase(TestCase):
    def test_getting_root(self):
        self.client.get('/')


from .templatetags.nettes_datum import nettes_datum
import datetime

class TestNettesDatum(TestCase):

    def test_the_day_before_yesterday(self):
        datum = datetime.datetime.now() - datetime.timedelta(days=2)
        self.assertEquals( nettes_datum( datum ), "Vorgestern" )

    def test_yesterday(self):
        datum = datetime.datetime.now() - datetime.timedelta(days=1)
        self.assertEquals( nettes_datum( datum ), "Gestern" )

    def test_today(self):
        today = datetime.date.today()
        self.assertEquals( nettes_datum( today ), "Heute" )

    def test_tomorrow(self):
        tomorrow = datetime.date.today() + datetime.timedelta(days=1)
        self.assertEquals( nettes_datum( tomorrow ), "Morgen" )

    def test_the_day_after_tomorrow(self):
        the_day_after_tomorrow = datetime.date.today() + datetime.timedelta(days=2)
        self.assertEquals( nettes_datum( the_day_after_tomorrow ), "Übermorgen" )

    def test_this_week(self):
        # this daytime might not always be correct
        daytime = datetime.datetime.now() + datetime.timedelta(days=3)
        self.assertEquals( nettes_datum( daytime ), "diesen WOCHENTAG" )

    def test_next_week(self):
        # this daytime might not always be correct
        daytime = datetime.datetime.now() + datetime.timedelta(days=10)
        self.assertEquals( nettes_datum( daytime ), "nächsten WOCHENTAG" )
