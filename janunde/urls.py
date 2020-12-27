from django.conf import settings
from django.conf.urls import include, url
from django.views.defaults import page_not_found, server_error
from django.views.generic.base import RedirectView, TemplateView

from wagtail.admin import urls as wagtailadmin_urls
from wagtail.core import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls
from wagtail.contrib.sitemaps.views import sitemap
from wagtail.images.views.serve import ServeView

from core.views import search


urlpatterns = [
    url(r"^404/$", page_not_found, kwargs={"exception": Exception("Page not Found")}),
    url(r"^500/$", server_error),
    url(r"^admin/", include(wagtailadmin_urls)),
    url(r"^documents/", include(wagtaildocs_urls)),
    url(
        r"^images/([^/]*)/(\d*)/([^/]*)/[^/]*$",
        ServeView.as_view(action="redirect"),
        name="wagtailimages_serve",
    ),
    url(r"^sitemap\.xml$", sitemap, name="sitemap"),
    url(
        r"^robots\.txt$",
        TemplateView.as_view(template_name="robots.txt", content_type="text/plain"),
    ),
    url(r"^search/", search, name="search",),
    url(
        r"^lueneburg/(?P<path>.*)",
        RedirectView.as_view(url="/netzwerk-projekte/janun-lüneburg/%(path)s"),
    ),
    url(
        r"^weltbewusst-lg",
        RedirectView.as_view(
            url="/netzwerk-projekte/janun-lüneburg/weltbewusst-lüneburg-neu/"
        ),
    ),
    url(
        r"^scp",
        RedirectView.as_view(
            url="/netzwerk-projekte/janun-landesbüro/silent-climate-parade/"
        ),
    ),
    url(
        r"^herbstspektakel",
        RedirectView.as_view(
            url="/netzwerk-projekte/janun-landesbüro/herbstspektakel/"
        ),
    ),
    url(
        r"^imagine", RedirectView.as_view(url="/veranstaltungen/herbstspektakel-2017/")
    ),
    url(r"^stadttraum", RedirectView.as_view(url="/veranstaltungen/stadttraum/")),
    url(
        r"^veranstaltungen/herbstspektakel-2018",
        RedirectView.as_view(url="/veranstaltungen/stadttraum/"),
    ),
    url(
        r"^netzwerk-projekte/janun-landesbuero/(?P<path>.*)",
        RedirectView.as_view(url="/netzwerk-projekte/janun-landesbüro/%(path)s"),
    ),
    url(
        r"^netzwerk-projekte/janun-landesb%FCro/(?P<path>.*)",
        RedirectView.as_view(url="/netzwerk-projekte/janun-landesbüro/%(path)s"),
    ),
    url(r"^festival", RedirectView.as_view(url="/veranstaltungen/janun-festival/")),
    url(r"^webinare", RedirectView.as_view(url="/veranstaltungen/?typ=Online")),
]


if settings.DEBUG:
    import debug_toolbar
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [
        url(r"^__debug__/", include(debug_toolbar.urls)),
    ]


urlpatterns += [url(r"", include(wagtail_urls))]
