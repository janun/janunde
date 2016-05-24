import hashlib
import datetime
from django.utils.http import urlquote
from django.template.defaultfilters import striptags



def get_add_mail():
    add_mail_subject = 'Vorschlag für eine Veranstaltung auf janun.de'
    add_mail_address = 'veranstaltungen@janun.de'
    add_mail_body = """Hallo!

Ich möchte eine Veranstaltung für janun.de vorschlagen.

Titel:
Von:
Bis:
Beschreibungstext:
Link:

> Wenn Du ein Bild zur Veranstaltung hast, hänge es einfach an die E-Mail an.
> Wir werden Deine E-Mail schnellstmöglichst bearbeiten und dann eine Veranstaltung auf janun.de erstellen.
> Vielen Dank für Deinen Vorschlag!

Viele Grüße"""

    return "mailto:{}?subject={}&body={}".format( add_mail_address,
        urlquote(add_mail_subject), urlquote(add_mail_body) )


def get_plain_text_content(html_content):
    content = str(html_content).replace("\n", "").replace("  ", "")
    content = content.replace("<br>", "\n").replace("<p>", "").replace("</p>", "\n\n")
    content = striptags(content).replace("  ", "").strip()
    return content


def export_event_to_google_link(event):
    # TODO: different url if external event
    url = event.full_url
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
        params['details'] = get_plain_text_content(event.content) + '\n\n' + url
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
    ical_event.add('dtstart', event.start_datetime.astimezone(pytz.utc))
    if event.end_datetime:
        ical_event.add('dtend', event.end_datetime.astimezone(pytz.utc))
    ical_event.add('dtstamp', event.latest_revision_created_at.astimezone(pytz.utc))
    if event.content:
        ical_event.add('description', get_plain_text_content(event.content))
    if event.location:
        ical_event.add('location', event.location)
    # TODO: different url if external event
    ical_event.add('url', event.full_url)
    cal.add_component(ical_event)
    return cal.to_ical()
