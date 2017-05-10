from django.conf import settings
from django.conf.urls import include, url
from django.views.defaults import page_not_found, server_error
from django.views.generic.base import RedirectView, TemplateView

from django.contrib import admin

from wagtail.wagtailadmin import urls as wagtailadmin_urls
from wagtail.wagtailcore import urls as wagtail_urls
from wagtail.wagtaildocs import urls as wagtaildocs_urls
from wagtail.wagtailsearch.urls.frontend import search
from wagtail.contrib.wagtailsitemaps.views import sitemap

from acme_challenge import urls as acme_challenge_urls

from core.views import tags
from core.addmultiple import add

from wagtail.wagtailimages.views.serve import ServeView



urlpatterns = [
    url(r'^', include(acme_challenge_urls)),

    url(r'^404/$', page_not_found, kwargs={'exception': Exception("Page not Found")} ),
    url(r'^500/$', server_error ),

    url(r'^admin/images/multiple/add/$', add, name='add_multiple'),
    url(r'^admin/', include(wagtailadmin_urls)),

    url(r'^django-admin/', include(admin.site.urls)),
    url(r'^documents/', include(wagtaildocs_urls)),

    url(r'^images/([^/]*)/(\d*)/([^/]*)/[^/]*$', ServeView.as_view(), name='wagtailimages_serve'),

    url(r'^sitemap\.xml$', sitemap, name='sitemap'),
    url(r'^robots\.txt$', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),

    url(r'^search/', search, {
            'results_per_page': 9,
            'template': "search/search_results.html",
            'template_ajax': "search/_search_results.html",
        }, name="search"),

    url(r'^thema/(?P<tagname>\w+)/$', tags, name='tags'),
    url(r'^lueneburg', RedirectView.as_view(url='/netzwerk-projekte/janun-lüneburg/') ),
    url(r'^scp', RedirectView.as_view(url='/netzwerk-projekte/janun-landesbüro/silent-climate-parade/') ),
    url(r'^herbstspektakel', RedirectView.as_view(url='/netzwerk-projekte/janun-landesbüro/herbstspektakel/') ),
]


if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    import debug_toolbar

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += [url(r'^__debug__/', include(debug_toolbar.urls)),]


urlpatterns += [url(r'', include(wagtail_urls))]
