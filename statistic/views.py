from django.db.models import Count
from django.views.generic import TemplateView

import django_filters
from django_filters.views import FilterView

from request.models import Request


class StatisticView(TemplateView):
    template_name = "statistic/statistic.html"
    title = "Statistik"
    header_icon = "table"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        unique_visits = Request.objects.exclude(
            referer__startswith=self.request.site.root_url
        )

        context["visits_today"] = unique_visits.today().count()
        context["visits_this_week"] = unique_visits.this_week().count()
        context["visits_this_month"] = unique_visits.this_month().count()
        context["top_paths"] = (
            Request.objects.filter(response__lt=400)
            .values("path")
            .annotate(Count("path"))
            .order_by("-path__count")[:10]
        )
        context["top_error_paths"] = (
            Request.objects.filter(response__gte=400)
            .values("path", "response")
            .annotate(Count("path"))
            .order_by("-path__count")[:10]
        )
        context["top_referers"] = (
            unique_visits.exclude(referer="")
            .values("referer")
            .annotate(Count("referer"))
            .order_by("-referer__count")[:10]
        )
        return context


class RequestFilter(django_filters.FilterSet):
    class Meta:
        model = Request
        fields = ("path", "response", "referer")


class BrowseRequestsView(FilterView):
    template_name = "statistic/browse_requests.html"
    title = "Statistik"
    header_icon = "table"
    queryset = Request.objects.today()
    context_object_name = "requests"
    paginate_by = 200
    filterset_class = RequestFilter
