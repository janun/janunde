from django.db import models
from wagtail.images.models import AbstractImage, AbstractRendition, Image


class AttributedImage(AbstractImage):
    """
    image model with optional attribution attributes
    """

    attribution = models.CharField("Quellenangabe", max_length=255, blank=True)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    @property
    def aspect(self):
        return self.height / self.width * 100

    admin_form_fields = Image.admin_form_fields + ("attribution",)


class AttributedRendition(AbstractRendition):
    image = models.ForeignKey(
        AttributedImage, related_name="renditions", on_delete=models.CASCADE
    )

    @property
    def aspect(self):
        return self.height / self.width * 100

    class Meta:
        unique_together = (("image", "filter_spec", "focal_point_key"),)
