from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render

from wagtail.search.models import Query
from wagtail.core.models import Page


def search(request):
    search_query = request.GET.get("q", None)
    page = request.GET.get("page")

    if search_query:
        search_results = Page.objects.live().search(search_query)

        # Log the query so Wagtail can suggest promoted results
        Query.get(search_query).add_hit()
    else:
        search_results = Page.objects.none()

    # pagination
    paginator = Paginator(search_results, 15)
    try:
        results = paginator.page(page)
    except PageNotAnInteger:
        results = paginator.page(1)
    except EmptyPage:
        results = paginator.page(paginator.num_pages)

    return render(
        request,
        "search/search_results.html",
        {"search_query": search_query, "search_results": results},
    )
