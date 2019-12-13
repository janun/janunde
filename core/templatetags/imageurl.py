# https://github.com/wagtail/wagtail/issues/2457

from django.core.urlresolvers import reverse
from wagtail.images.views.serve import generate_signature
from django import template

def generate_image_url(image, filter_spec):
    signature = generate_signature(image.id, filter_spec)
    url = reverse('wagtailimages_serve', args=(signature, image.id, filter_spec))
    url += image.file.name[len('original_images/'):]
    return url

register = template.Library()

@register.filter()
def imageurl(image, filter_spec):
    return generate_image_url(image, filter_spec)
