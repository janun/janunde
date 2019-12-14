# https://github.com/wagtail/wagtail/issues/2457

from django.urls import reverse
from django import template
from wagtail.images.views.serve import generate_signature


def generate_image_url(image, filter_spec):
    signature = generate_signature(image.id, filter_spec)
    url = reverse("wagtailimages_serve", args=(signature, image.id, filter_spec))
    url += image.file.name[len("original_images/") :]
    return url


register = template.Library()


@register.filter()
def imageurl(image, filter_spec):
    return generate_image_url(image, filter_spec)
