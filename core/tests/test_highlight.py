from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from wagtail.core.models import Page
from core.models import StandardPage, Highlight

class HighlightTestCase(TestCase):

    def setUp(self):
        homepage = Page.objects.get(title="Startseite")
        seite = homepage.add_child(
            instance=StandardPage(title="Einfache Seite")
        )
        Highlight.objects.create(highlighted_page=seite)
        Highlight.objects.create(
            highlighted_page=seite,
            title_override="Guck dir die Seite an!"
        )

    def test_highlights_exists_and_active(self):
        self.assertEqual(Highlight.objects.active().count(), 2)

    def test_highlight_starts_now(self):
        highlight = Highlight.objects.first()
        self.assertEqual(
            highlight.start_datetime.strftime("%Y-%m-%d %H:%M:%S"),
            timezone.now().strftime("%Y-%m-%d %H:%M:%S")
        )

    def test_highlight_ends_in_14_days(self):
        highlight = Highlight.objects.first()
        self.assertEqual(
            highlight.end_datetime.strftime("%Y-%m-%d %H:%M:%S"),
            (timezone.now() + timedelta(days=14)).strftime("%Y-%m-%d %H:%M:%S")
        )

    def test_title_defaults_to_highlighted_page(self):
        highlight = Highlight.objects.first()
        self.assertEqual(highlight.title, highlight.highlighted_page.title)

    def test_title_can_be_overriden(self):
        highlight = Highlight.objects.last()
        self.assertEqual(highlight.title, highlight.title_override)
