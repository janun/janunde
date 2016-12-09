from django.conf import settings
from django.conf.urls import include, url
from django.views.defaults import page_not_found, server_error
from django.views.generic.base import RedirectView
from django.contrib import admin

from wagtail.wagtailadmin import urls as wagtailadmin_urls
from wagtail.wagtailcore import urls as wagtail_urls
from wagtail.wagtaildocs import urls as wagtaildocs_urls
from wagtail.wagtailsearch.urls.frontend import search

from acme_challenge import urls as acme_challenge_urls

from core.views import tags


urlpatterns = [
    url(r'^', include(acme_challenge_urls)),

    url(r'^404/$', page_not_found, kwargs={'exception': Exception("Page not Found")} ),
    url(r'^500/$', server_error ),

    url(r'^admin/', include(wagtailadmin_urls)),
    url(r'^django-admin/', include(admin.site.urls)),
    url(r'^documents/', include(wagtaildocs_urls)),

    url(r'^search/', search, {
            'results_per_page': 10,
            'template': "search/search_results.html",
            'template_ajax': "search/_search_results.html",
        }, name="search"),

    url(r'^thema/(?P<tagname>\w+)/$', tags, name='tags'),
    url(r'', include(wagtail_urls)),
]


# TODO: do we still need this?
if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
