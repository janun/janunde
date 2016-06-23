import os

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render
from wagtail.wagtailcore.models import Page
from wagtail.wagtailsearch.models import Query

from django.http import HttpResponse
from django.http import Http404


def acme_challenge(request):
    if not 'ACME_CHALLENGE' in os.environ:
        raise Http404
    if request.path == '/.well-known/acme-challenge/%s' % os.environ['ACME_CHALLENGE']:
        return HttpResponse(os.environ['ACME_RESPONSE'])
    else:
        raise Http404


def search(request):
    search_query = request.GET.get('query', None)
    page = request.GET.get('page', 1)

    # Search
    if search_query:
        search_results = Page.objects.live().specific().search(search_query)
        query = Query.get(search_query)

        # Record hit
        query.add_hit()
    else:
        search_results = Page.objects.none()

    # Pagination
    paginator = Paginator(search_results, 10)
    try:
        search_results = paginator.page(page)
    except PageNotAnInteger:
        search_results = paginator.page(1)
    except EmptyPage:
        search_results = paginator.page(paginator.num_pages)

    return render(request, 'core/search.html', {
        'search_query': search_query,
        'search_results': search_results,
    })
