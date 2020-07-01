# from django.test import TestCase
from unittest import TestCase
from .management.commands.wagtail_ping_google import ping_google


class PingGoogleTestCase(TestCase):
    def test_ping_google(self):
        ping_google("https://example.com")
