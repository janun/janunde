from django import template
register = template.Library()
from phonenumber_field.widgets import PhoneNumberInternationalFallbackWidget


@register.filter()
def cut(value, arg):
    return value.replace(arg, '')

@register.filter()
def prettyurl(value):
    return value.replace("http://", "").replace("https://", "").replace("www.", "")

@register.filter()
def prettyphone(value):
    widget = PhoneNumberInternationalFallbackWidget()
    return widget._format_value(value)
