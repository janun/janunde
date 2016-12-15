import hashlib
import datetime
from django.utils.http import urlquote


def export_event_to_google_link(event):
    # TODO: different url if external event
    url = event.full_url
    if event.all_day:
        datetime_format = "%Y%m%d"
    else:
        datetime_format = "%Y%m%dT%H%M%SZ"
    link = "http://www.google.com/calendar/event?action=TEMPLATE&"
    # since end_datetime is mandatory, get start_datetime + 30 min
    end_datetime = event.end_datetime or event.start_datetime + datetime.timedelta(minutes=30)
    params = {
        'text': event.title,
        'dates': event.start_datetime.strftime(datetime_format) + "/" + end_datetime.strftime(datetime_format),
        'sprop': url, # doesnt work anymore with google?
    }
    if event.location:
        params['location'] = event.location
    if event.content:
        params['details'] = event.get_description() + '\n\n' + url
    cons_params = [param[0] + "=" +  urlquote(param[1]) for param in params.items()]
    return link + "&".join(cons_params)


def export_event_to_ical(event):
    from icalendar import Event, Calendar
    import pytz
    cal = Calendar()
    cal.add('prodid', '-//janun.de//')
    cal.add('version', '2.0')
    ical_event = Event()
    ical_event.add('uid', event.slug + "@" + "janun.de")
    ical_event.add('summary', event.title)
    if event.all_day:
        ical_event.add('dtstart', event.start_datetime.astimezone(pytz.utc).date())
    else:
        ical_event.add('dtstart', event.start_datetime.astimezone(pytz.utc))
    if event.end_datetime:
        if event.all_day:
            ical_event.add('dtend', event.end_datetime.astimezone(pytz.utc).date())
        else:
            ical_event.add('dtend', event.end_datetime.astimezone(pytz.utc))
    ical_event.add('dtstamp', event.latest_revision_created_at.astimezone(pytz.utc))
    if event.content:
        ical_event.add('description', event.get_description())
    if event.location:
        ical_event.add('location', event.location)
    # TODO: different url if external event
    ical_event.add('url', event.full_url)
    cal.add_component(ical_event)
    return cal.to_ical()
