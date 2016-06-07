from django import template
register = template.Library()
from phonenumber_field.widgets import PhoneNumberInternationalFallbackWidget
from django.utils.safestring import mark_safe


@register.filter()
def prettyurl(value):
    url_parts = value.replace("http://", "").replace("https://", "").replace("www.", "").split("/")
    if len(url_parts) > 1:
        return url_parts[0] + "/…"
    else:
        return url_parts[0]

@register.filter()
def prettyphone(value):
    widget = PhoneNumberInternationalFallbackWidget()
    return widget._format_value(value)


from softhyphen.html import hyphenate

@register.filter()
def softhyphen(value, language=None):
    return mark_safe(hyphenate(value, language=language))
