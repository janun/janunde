from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.utils.html import format_html
from wagtail.wagtailimages.models import (AbstractImage, AbstractRendition,
                                          Image)


class AttributedImage(AbstractImage):
    """
    image model with optional attribution attributes
    """
    attribution = models.CharField("Quellenangabe", max_length=255, blank=True)

    @property
    def aspect(self):
        return self.height / self.width * 100;

    admin_form_fields = Image.admin_form_fields + (
        'attribution',
    )


class AttributedRendition(AbstractRendition):
    image = models.ForeignKey(AttributedImage, related_name='renditions')

    @property
    def aspect(self):
        return self.height / self.width * 100;

    class Meta:
        unique_together = (
            ('image', 'filter', 'focal_point_key'),
        )


# Delete the source image file when an image is deleted
@receiver(pre_delete, sender=AttributedImage)
def image_delete(sender, instance, **kwargs):
    instance.file.delete(False)


# Delete the rendition image file when a rendition is deleted
@receiver(pre_delete, sender=AttributedRendition)
def rendition_delete(sender, instance, **kwargs):
    instance.file.delete(False)


# Do feature detection when a user saves an image without a focal point
# @receiver(pre_save, sender=AttributedImage)
# def image_feature_detection(sender, instance, **kwargs):
#    # Make sure the image doesn't already have a focal point
#    if not instance.has_focal_point():
#        # Set the focal point
#        instance.set_focal_point(instance.get_suggested_focal_point())
