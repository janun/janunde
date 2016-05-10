import datetime
from django import template
from django.template.defaultfilters import date as date_filter

register = template.Library()


today = datetime.date.today()
tomorrow = today + datetime.timedelta(days=1)


def is_in_this_week(date):
    """returns the last day of this week"""
    end_of_this_week = today + datetime.timedelta(days=6 - today.weekday())
    begin_of_this_week = today - datetime.timedelta(days=today.weekday())
    return begin_of_this_week <= date <= end_of_this_week

def is_in_next_week(date):
    """returns the last day of this week"""
    end_of_next_week = today + datetime.timedelta(days=6 - today.weekday() + 7)
    begin_of_next_week = today - datetime.timedelta(days=today.weekday() + 7)
    return begin_of_next_week <= date <= end_of_next_week


@register.filter()
def nettes_datum(our_date):
    """
    generate a nice looking/readable date in German
    """
    if type(our_date) is datetime.datetime:
        our_date = our_date.date()
    datum = date_filter(our_date, "SHORT_DATE_FORMAT")
    wochentag = date_filter(our_date, "l")

    if our_date == today - datetime.timedelta(days=2):
        return "vorgestern"
    if our_date == today - datetime.timedelta(days=1):
        return "gestern"
    if our_date == today:
        return "heute"
    if our_date == tomorrow:
        return "morgen"
    if our_date == tomorrow + datetime.timedelta(days=1):
        return "übermorgen"
    if is_in_this_week(our_date):
        return "diesen {}".format( wochentag )
    if is_in_next_week(our_date):
        return "nächsten {}".format( wochentag )
    return "{}, {}".format( wochentag, datum )
