import urllib

from django import template
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
from django.http import HttpRequest

from wagtail.embeds import embeds
from wagtail.embeds.exceptions import EmbedException

from core.models import Banner

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


# Banner snippets
@register.inclusion_tag("core/banners.html", takes_context=True)
def banners(context):
    return {
        "banners": Banner.objects.all(),
        "request": context["request"],
    }


@register.simple_tag
def query_transform(request: HttpRequest, delete="", replace=True, **kwargs):
    """Template tag to edit querystrings

    Preserve anything already in the query string and just set the keys that you specify.

    Example: <a href="{% url 'view_name' %}?{% query_transform request a=5 b=6 %}">

    Args:
        request: Django request object (containing Django QueryDict object)
        delete: single key that should be deleted from querystring
        replace: wether existing keys in querystring should be replaced with keys from kwargs
        kwargs: dict of keys with which to update the queryset

    Returns:
        urlencoded querystring"""
    updated = request.GET.copy()

    if delete and delete in updated:
        updated.pop(delete)

    if replace:
        for key, value in kwargs.items():
            updated[key] = value
    else:
        updated.update(kwargs)

    return updated.urlencode()


@register.simple_tag
def highlight(value, search, klass="font-bold"):
    """Highlight search in value

    Example:
        {% highlight "This is a test" "test" %}
        'This is a <span class="font-bold">test</span>'"""
    if not search:
        return value
    esc = conditional_escape
    result = esc(value).replace(
        search, f"""<span class="{esc(klass)}">{esc(search)}</span>"""
    )
    return mark_safe(result)


@register.filter
def ancestors(obj):
    """Get the ancestors of obj excluding Root and Homepage"""
    return obj.get_ancestors()[2:]
