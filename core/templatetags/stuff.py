import urllib
from django import template

from wagtail.embeds import embeds
from wagtail.embeds.exceptions import EmbedException

register = template.Library()


@register.filter()
def prettyurl(value):
    return urllib.parse.urlparse(value).netloc


@register.filter()
def pathtosearch(value):
    return value.split("/")[-2]


@register.filter
def get_embed(url, max_width=None):
    try:
        return embeds.get_embed(url, max_width=max_width)
    except EmbedException:
        return ""
