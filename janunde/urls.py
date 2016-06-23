from django.conf import settings
from django.conf.urls import include, url
from django.views.defaults import page_not_found, server_error
from wagtail.wagtailadmin import urls as wagtailadmin_urls
from wagtail.wagtailcore import urls as wagtail_urls
from wagtail.wagtaildocs import urls as wagtaildocs_urls

from core.views import search, acme_challenge

urlpatterns = [
    url(r'^404/$', page_not_found),
    url(r'^500/$', server_error),

    url(r'^.well-known/acme-challenge/', acme_challenge), # for letsencrypt

    url(r'^admin/', include(wagtailadmin_urls)),
    url(r'^documents/', include(wagtaildocs_urls)),

    url(r'^search/$', search, name='search'),

    url(r'^styleguide/', include('styleguide.urls')),

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
