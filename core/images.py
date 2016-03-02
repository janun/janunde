from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.utils.html import format_html
from wagtail.wagtailimages.models import (AbstractImage, AbstractRendition,
                                          Image)


def _(str):
    """dummy translation"""
    return str


class AttributedImage(AbstractImage):
    """
    image model with optional attribution attributes
    """
    original_title = models.CharField(_("Original Titel"),
                                      max_length=255, blank=True)
    author = models.CharField(_("Autor"), max_length=255, blank=True)
    author_url = models.URLField(_("Autor-Website"),
                                 max_length=255, blank=True)
    source = models.URLField(_("Quelle"), max_length=255, blank=True)
    license = models.CharField(_("Lizenz"), max_length=255, blank=True)
    license_url = models.URLField(_("Lizenz-Website"),
                                  max_length=255, blank=True)

    admin_form_fields = Image.admin_form_fields + (
        'original_title', 'author', 'author_url', 'source', 'license',
        'license_url'
    )

    @property
    def author_html(self):
        if not self.author:
            return ""
        if not self.author_url:
            return format_html(_("von {author}"), author=self.author)
        return format_html(
            _('von <a href="{author_url}">{author}</a>'),
            author_url=self.author_url, author=self.author
        )

    @property
    def title_html(self):
        if not self.original_title:
            title = self.title
        else:
            title = self.original_title
        if not self.source:
            return format_html(_("„{title}“"), title=title)
        return format_html(
            '<a href="{source}">„{title}“</a>',
            source=self.source, title=title
        )

    @property
    def license_html(self):
        if not self.license:
            return ""
        if not self.license_url:
            return self.license
        return format_html(
            '<a href="{license_url}">{license}</a>',
            license_url=self.license_url, license=self.license
        )

    @property
    def attribution(self):
        attribution = format_html(_("Photo: {title}"), title=self.title_html)
        if self.author_html:
            attribution += format_html("<br> {0}", self.author_html)
        if self.license_html:
            attribution += format_html("<br> ({0})", self.license_html)
        return attribution


class AttributedRendition(AbstractRendition):
    image = models.ForeignKey(AttributedImage, related_name='renditions')

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
