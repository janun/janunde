import datetime
from urllib.request import urlopen
from urllib.parse import urlencode

from django.core.management.base import BaseCommand
from django.utils import timezone

from wagtail.core.models import Page

PING_URL = "https://www.google.com/webmasters/tools/ping"


def ping_google(sitemap_url, ping_url=PING_URL):
    # using own version so we dont need django site framework
    params = urlencode({"sitemap": sitemap_url})
    urlopen("%s?%s" % (ping_url, params))


class Command(BaseCommand):
    help = (
        "Ping Google with sitemap.xml if change in wagtail pages in the last n minutes"
    )

    def add_arguments(self, parser):
        parser.add_argument("sitemap_url", nargs=1)
        parser.add_argument("minutes", nargs="?", default="10")

    def handle(self, *args, **options):
        minutes = int(options["minutes"])
        time = timezone.now() - datetime.timedelta(minutes=minutes)
        if Page.objects.filter(last_published_at__gte=time).exists():
            ping_google(sitemap_url=options["sitemap_url"])
