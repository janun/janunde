from django import template
register = template.Library()
from phonenumber_field.widgets import PhoneNumberInternationalFallbackWidget
from django.utils.safestring import mark_safe
import urllib

from wagtail.wagtailembeds import embeds
from wagtail.wagtailembeds.exceptions import EmbedException

@register.filter()
def prettyurl(value):
    return urllib.parse.urlparse(value).netloc


@register.filter()
def prettyphone(value):
    widget = PhoneNumberInternationalFallbackWidget()
    return widget._format_value(value)


from softhyphen.html import hyphenate

@register.filter()
def softhyphen(value, language=None):
    return mark_safe(hyphenate(value, language=language))


@register.filter
def get_embed(url, max_width=None):
    try:
        return embeds.get_embed(url, max_width=max_width)
    except EmbedException:
        return ''
