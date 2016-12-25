from django import template
register = template.Library()
from phonenumber_field.widgets import PhoneNumberInternationalFallbackWidget
import urllib
from django.template import Context

from wagtail.wagtailembeds import embeds
from wagtail.wagtailembeds.exceptions import EmbedException



@register.filter()
def prettyurl(value):
    return urllib.parse.urlparse(value).netloc


@register.filter()
def pathtosearch(value):
    return value.split('/')[-2]


@register.filter()
def prettyphone(value):
    widget = PhoneNumberInternationalFallbackWidget()
    return widget._format_value(value)


@register.filter
def get_embed(url, max_width=None):
    try:
        return embeds.get_embed(url, max_width=max_width)
    except EmbedException:
        return ''
