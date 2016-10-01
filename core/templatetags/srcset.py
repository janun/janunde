from django import template
from wagtail.wagtailimages.shortcuts import get_rendition_or_not_found

register = template.Library()

@register.filter()
def srcset(image, filter_specs):
    """
    generate a list of image renditions suitable for html5 srcset
    usage:
        srcset="{{ image|srcset:'width-320|jpg width-640|jpg' }}"
    """
    sources = {}
    for filter_spec in filter_specs.split(' '):
        rendition = get_rendition_or_not_found(image, filter_spec)
        if not rendition.width in sources:
            sources[rendition.width] = "%s %iw" % (rendition.url, rendition.width)

    return ', '.join(sources.values())
