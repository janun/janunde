from django.db import models
from django.http import JsonResponse
from django.core.exceptions import ValidationError

from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel

from wagtail.admin.edit_handlers import (
    FieldPanel,
    StreamFieldPanel,
    ObjectList,
    TabbedInterface,
    HelpPanel,
    InlinePanel,
    MultiFieldPanel,
)
from wagtail.core.fields import StreamField
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index
from wagtail.admin.forms import WagtailAdminPageForm

from core.images import AttributedImage as Image
from core.blocks import StandardStreamBlock
from core.models import BasePage

from .blocks import WimmelbildStreamBlock


class WimmelbildPoint(ClusterableModel):
    """InfoPoint in a Wimmelbild"""

    latlng = models.CharField("Position", max_length=255)
    tooltip = models.CharField(
        "Tooltip", max_length=255, blank=True, help_text="Wird bei Hover angezeigt."
    )
    icon = models.ForeignKey(
        Image,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
        verbose_name="Icon",
        help_text="Am besten kleines (30x30px) transparentes PNG. Fragezeichen wenn leer",
    )
    content = StreamField(
        WimmelbildStreamBlock(required=False),
        blank=True,
        null=True,
        verbose_name="Inhalt",
    )

    panels = [
        FieldPanel("latlng", classname="latlng"),
        ImageChooserPanel("icon"),
        FieldPanel("tooltip"),
        StreamFieldPanel("content"),
    ]

    @property
    def json_dict(self):
        jd = {
            "latlng": self.latlng,
            "tooltip": self.tooltip,
            "content": self.content.stream_block.render_basic(self.content, {}),
        }
        if self.icon:
            jd["icon"] = {
                "url": self.icon.file.url,
                "width": self.icon.width,
                "height": self.icon.height,
            }
        return jd


class WimmelbildPointWimmelbildPage(WimmelbildPoint):
    setting = ParentalKey(
        "wimmelbilder.WimmelbildPage", on_delete=models.CASCADE, related_name="points",
    )


class WimmelbildPageForm(WagtailAdminPageForm):
    class Media:
        css = {"all": ("leaflet/dist/leaflet.css",)}
        js = (
            "leaflet/dist/leaflet.js",
            "wimmelbilder/admin-form.js",
        )


class WimmelbildPage(BasePage):
    base_form_class = WimmelbildPageForm

    subtitle = models.CharField("Untertitel", max_length=255, blank=True)

    feed_image = models.ForeignKey(
        Image,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
        verbose_name="Hauptbild",
        help_text="Wird in Übersichten verwendet.",
    )

    before = StreamField(
        StandardStreamBlock(required=False),
        blank=True,
        null=True,
        verbose_name="Vor dem Wimmelbild",
    )
    after = StreamField(
        StandardStreamBlock(required=False),
        blank=True,
        null=True,
        verbose_name="Nach dem Wimmelbild",
    )

    tile_url = models.URLField(
        "Kachel-URL",
        help_text="URL zu den Kacheln, aus denen das Bild besteht. Benutze {z}, {x}, {y} in der URL für die Koordinaten",
        blank=True,
    )
    width = models.IntegerField(
        "Breite", help_text="Breite des Wimmelbilds in Pixeln", blank=True, null=True
    )
    height = models.IntegerField(
        "Höhe", help_text="Höhe des Wimmelbilds in Pixeln", blank=True, null=True
    )

    search_fields = BasePage.search_fields + [
        index.SearchField("subtitle"),
        index.SearchField("before"),
        index.SearchField("after"),
    ]

    content_panels = [
        FieldPanel("title"),
        FieldPanel("subtitle"),
        ImageChooserPanel("feed_image"),
        StreamFieldPanel("before"),
        HelpPanel("Hier kommt das Wimmelbild"),
        StreamFieldPanel("after"),
    ]

    wimmelbild_panels = [
        MultiFieldPanel(
            [
                HelpPanel(
                    "Das Wimmelbild muss in Kacheln aufgeteilt werden (z.B. mit gdal2tiles) und diese dann Hochgeladen werden."
                ),
                FieldPanel("tile_url"),
                FieldPanel("width"),
                FieldPanel("height"),
            ],
            heading="Technisches",
        ),
        # HelpPanel(template="wimmelbilder/map_edit.html", heading="Übersicht über Info-Punkte"), # TODO
        InlinePanel("points", heading="Info-Punkte"),
    ]

    edit_handler = TabbedInterface(
        [
            ObjectList(content_panels, heading="Text-Inhalt"),
            ObjectList(wimmelbild_panels, heading="Wimmelbild"),
            ObjectList(BasePage.promote_panels, heading="Veröffentlichung"),
            ObjectList(
                BasePage.settings_panels, heading="Einstellungen", classname="settings"
            ),
        ]
    )

    def serve(self, request):
        """get json representation"""
        if "json" in request.GET:
            points = [p.json_dict for p in self.points.all()]
            return JsonResponse(
                {
                    "tileUrl": self.tile_url,
                    "width": self.width,
                    "height": self.height,
                    "points": points,
                },
                safe=False,
            )
        else:
            return super().serve(request)

    def clean(self):
        super().clean()
        if self.tile_url:
            if not self.width:
                raise ValidationError({"width": "Erforderlich, wenn Kacheln angegeben"})
            if not self.height:
                raise ValidationError(
                    {"height": "Erforderlich, wenn Kacheln angegeben"}
                )

    class Meta:
        verbose_name = "Wimmelbild-Seite"
        verbose_name_plural = "Wimmelbild-Seiten"
