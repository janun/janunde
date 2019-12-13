from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from wagtail.core.models import Page
from core.models import StandardPage, Highlight

# the most basic test...
class BasicTestCase(TestCase):
    def test_getting_root(self):
        self.client.get('/')
