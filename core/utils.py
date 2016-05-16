import hashlib
import datetime

def start_of_this_week():
    pass

def end_of_this_week():
    pass


def export_event(event, format='ical'):
    """Export EventPage to ical format"""
    ICAL_DATE_FORMAT = '%Y%m%dT%H%M%S'

    if format != 'ical':
        return

    # Begin event
    # VEVENT format: http://www.kanzaki.com/docs/ical/vevent.html
    ical_components = [
        'BEGIN:VCALENDAR',
        'VERSION:2.0',
    ]

    def add_slashes(string):
        string.replace('"', '\\"')
        string.replace('\\', '\\\\')
        string.replace(',', '\\,')
        string.replace(':', '\\:')
        string.replace(';', '\\;')
        string.replace('\n', '\\n')
        return string

    # Make a uid
    event_string = event.url + str(event.start_datetime)
    uid = hashlib.sha1(event_string.encode('utf-8')).hexdigest() + '@janun.de'

    # Make event
    ical_components.extend([
        'BEGIN:VEVENT',
        'UID:' + add_slashes(uid),
        'URL:' + add_slashes(event.url),
        'DTSTAMP:' + event.start_datetime.strftime(ICAL_DATE_FORMAT),
        'SUMMARY:' + add_slashes(event.title),
        #'DESCRIPTION:' + add_slashes(event.search_description), # TODO
        'LOCATION:' + add_slashes(event.location),
        'DTSTART;TZID=Europe/London:' + event.start_datetime.strftime(ICAL_DATE_FORMAT),
        'END:VEVENT',
    ])

    if event.end_datetime:
        ical_components.extend([
            'DTEND;TZID=Europe/London:' + event.end_datetime.strftime(ICAL_DATE_FORMAT)
        ])

    # Finish event
    ical_components.extend([
        'END:VCALENDAR',
    ])

    # Join components
    return '\r'.join(ical_components)
