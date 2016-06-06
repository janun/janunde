from django import template
register = template.Library()
from phonenumber_field.widgets import PhoneNumberInternationalFallbackWidget
from django.utils.safestring import mark_safe


@register.filter()
def prettyurl(value):
    return value.replace("http://", "").replace("https://", "").replace("www.", "").strip("/")

@register.filter()
def prettyphone(value):
    widget = PhoneNumberInternationalFallbackWidget()
    return widget._format_value(value)


from softhyphen.html import hyphenate

@register.filter
def softhyphen(value, language=None):
    """
    Hyphenates html.
    """
    return mark_safe(hyphenate(value, language=language))
