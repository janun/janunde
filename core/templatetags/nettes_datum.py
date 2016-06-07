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


def is_in_this_week(date):
    """returns the last day of this week"""
    today = datetime.date.today()
    return today <= date <= today + datetime.timedelta(days=6)


# def is_in_next_week(date):
#     """returns the last day of this week"""
#     end_of_next_week = today + datetime.timedelta(days=6 - today.weekday() + 7)
#     begin_of_next_week = today + datetime.timedelta(days=7-today.weekday())
#     return begin_of_next_week <= date <= end_of_next_week


def is_in_last_week(date):
    """returns the last day of this week"""
    today = datetime.date.today()
    end_of_last_week = today + datetime.timedelta(days=6 - today.weekday() - 7)
    begin_of_last_week = today + datetime.timedelta(days=0-today.weekday() - 7)
    return begin_of_last_week <= date <= end_of_last_week


@register.filter(needs_autoescape=True)
def add_tooltip(date, text, autoescape=True):
    if autoescape:
        esc = conditional_escape
    else:
        esc = lambda x: x
    return mark_safe('<span title="{}">{}</span>'.format(
        date_filter(date, "SHORT_DATE_FORMAT"),
        esc(text)
    ))


@register.filter(needs_autoescape=True)
def grey_span(text, autoescape=True):
    if autoescape:
        esc = conditional_escape
    else:
        esc = lambda x: x
    return mark_safe('<span class="color-grey">{}</span>'.format(esc(text)))


@register.filter(expects_localtime=True)
def nettes_datum_grey_date(our_date):
    return nettes_datum(our_date, grey_date=True)


@register.filter(expects_localtime=True)
def nettes_datum(our_date, show_date=False, tooltip=True, grey_date=False):
    """
    generate a nice looking/readable date in German
    """
    today = datetime.date.today()
    tomorrow = today + datetime.timedelta(days=1)
    if type(our_date) is datetime.datetime:
        our_date = our_date.date()
    wochentag = date_filter(our_date, "l")

    text = ""
    if is_in_last_week(our_date):
        text = "letzter {}".format( wochentag )
    elif our_date == today - datetime.timedelta(days=2):
        text = "vorgestern"
    elif our_date == today - datetime.timedelta(days=1):
        text = "gestern"
    elif our_date == today:
        text = "heute"
    elif our_date == tomorrow:
        text = "morgen"
    # elif our_date == tomorrow + datetime.timedelta(days=1):
    #     text = "übermorgen"
    elif is_in_this_week(our_date):
        text = wochentag
    # elif is_in_next_week(our_date):
    #     text = "nächsten {}".format( wochentag )
    else:
        tooltip = False # already has date
        if grey_date:
            text = mark_safe("{}., {}".format(
                date_filter(our_date, "D"),
                grey_span(date_filter(our_date, "d.m."))
            ))
        else:
            text = "{}., {}".format(
                date_filter(our_date, "D"),
                date_filter(our_date, "d.m.")
            )

    if tooltip:
        text = add_tooltip(our_date, text)
    return text
