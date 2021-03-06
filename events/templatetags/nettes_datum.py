import datetime
from django import template
from django.template.defaultfilters import date as date_filter
from django.utils.safestring import mark_safe
from django.utils.html import conditional_escape

register = template.Library()


@register.filter(expects_localtime=True)
def format_month(date):
    today = datetime.date.today()
    if date.year == today.year:
        return date_filter(date, "F")
    else:
        return date_filter(date, "F Y")


@register.filter(needs_autoescape=True)
def grey_span(text, autoescape=True):
    if autoescape:
        esc = conditional_escape
    else:
        esc = lambda x: x
    return mark_safe('<span class="text-gray-600">{}</span>'.format(esc(text)))


def maybe_year(value, today):
    if value.year != today.year:
        return date_filter(value, "d.m.Y")
    else:
        return date_filter(value, "d.m.")


@register.filter(expects_localtime=True)
def nettes_datum(value, short=False):
    try:
        tzinfo = getattr(value, "tzinfo", None)
        value = datetime.date(value.year, value.month, value.day)
    except AttributeError:
        # Passed value wasn't a date object
        return value
    except ValueError:
        # Date arguments out of range
        return value
    today = datetime.datetime.now(tzinfo).date()
    delta = value - today
    datum = maybe_year

    if delta.days == 0:
        if short:
            return "heute"
        return mark_safe("heute" + grey_span(", " + datum(value, today)))
    if delta.days == 1:
        if short:
            return "morgen"
        return mark_safe("morgen" + grey_span(", " + datum(value, today)))
    if delta.days == -1:
        if short:
            return "gestern"
        return mark_safe("gestern" + grey_span(", " + datum(value, today)))
    if 1 < delta.days < 7:
        if short:
            return date_filter(value, "l")
        return mark_safe(
            date_filter(value, "l") + grey_span(", " + datum(value, today))
        )
    if short:
        return date_filter(value, "D") + ", " + datum(value, today)
    return date_filter(value, "l") + ", " + datum(value, today)
