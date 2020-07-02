from django import template

from banners.models import Banner

register = template.Library()


@register.inclusion_tag("banners/banners.html", takes_context=True)
def banners(context):
    """Render banners"""
    return {
        "banners": Banner.get_by_request(context["request"]),
        "request": context["request"],
    }
