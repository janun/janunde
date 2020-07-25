from django import template

from banners.models import Banner

register = template.Library()


@register.inclusion_tag("banners/banners.html", takes_context=True)
def banners(context):
    """Render banners"""
    request = context.get("request", None)
    if request:
        return {
            "banners": Banner.get_by_request(request),
            "request": request,
        }
    return {}
