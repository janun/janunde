from django.test import TestCase
from django.db import models

from wagtail.wagtailcore.models import Page
from wagtail.wagtailimages.models import Image
from wagtail.wagtailimages.tests.utils import get_test_image_file

from core.models import FallbackImageMixin

# TODO: Test not working )-:

class TestPage(Page, FallbackImageMixin):
    main_image = models.ForeignKey(
        Image,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='+',
    )

    class Meta:
        app_label = 'core'


class FallbackImageMixinTestCase(TestCase):
    def setUp(self):
        homepage = Page.objects.get(title="Startseite")
        self.image = Image.objects.create(
            title="Test image",
            file=get_test_image_file(),
            tags="testpage-fallback"
        )
        self.test_page = homepage.add_child(
            instance=TestPage(title="Test Seite")
        )

    def test_fallback_image(self):
        pass
