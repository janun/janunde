from django.db import models

from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel

from wagtail.admin.edit_handlers import (
    FieldPanel,
    InlinePanel,
    RichTextField,
    FieldRowPanel,
)
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.contrib.settings.models import BaseSetting, register_setting
from wagtail.core.models import Orderable


class Banner(ClusterableModel):
    """Website Banner

    TODO:
     * Field where is shown (top vs bottom)
    """

    active = models.BooleanField("aktiviert", default=True)
    text = RichTextField("Text", features=["bold", "italic", "link"])

    image = models.ForeignKey(
        "core.AttributedImage",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Bild",
        help_text="Kleines Bild, das links angezeigt werden kann. Icons o.ä.",
    )

    color = models.CharField(
        "Farbe",
        max_length=16,
        choices=[
            ("white", "Weiß"),
            ("green", "Grün"),
            ("blue", "Blau"),
            ("red", "Rot"),
            ("purple", "Lila"),
            ("black", "Schwarz"),
        ],
        default="white",
        help_text="Hintergrundfarbe des Banners",
    )

    button_text = models.CharField(
        "Button-Text",
        max_length=255,
        null=True,
        blank=True,
        help_text="Wird auf mobil nicht angezeigt",
    )
    button_link = models.URLField("Button-Link", max_length=255, null=True, blank=True)

    where = models.CharField(
        "Wo",
        max_length=100,
        choices=[
            ("everywhere", "Alle Seiten"),
            ("homepage", "Nur Startseite"),
            ("not_homepage", "Alle außer Startseite"),
        ],
        default="everywhere",
        help_text="Auf welchen Seiten soll das Banner angezeigt werden?",
    )

    panels = [
        FieldPanel("active"),
        FieldPanel("where"),
        FieldPanel("color"),
        ImageChooserPanel("image"),
        FieldPanel("text"),
        FieldRowPanel([FieldPanel("button_text"), FieldPanel("button_link"),]),
    ]

    @property
    def bg_color(self):
        COLORS = {
            "white": "bg-white",
            "green": "bg-green-600",
            "blue": "bg-blue-500",
            "red": "bg-red-500",
            "purple": "bg-purple",
            "black": "bg-gray-900",
        }
        return COLORS[self.color]

    @property
    def text_color(self):
        if self.color == "white":
            return "text-gray-900"
        return "text-white"

    @classmethod
    def get_by_request(cls, request):
        qs = cls.objects.filter(active=True)
        if request.path == "/":
            return qs.exclude(where="not_homepage")
        if request.path != "/":
            return qs.exclude(where="homepage")


class BannersSettingsBanner(Orderable, Banner):
    setting = ParentalKey(
        "banners.BannersSettings", on_delete=models.CASCADE, related_name="banners",
    )


@register_setting
class BannersSettings(BaseSetting, ClusterableModel):

    panels = [InlinePanel("banners")]

    class Meta:
        verbose_name = "Banner"
        verbose_name_plural = "Banner"
