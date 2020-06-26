from django.db.models import Count
from django.views.generic import TemplateView
from django.http import HttpResponse
from django.db.models.functions import TruncHour

from wagtail.admin.views.reports import SpreadsheetExportMixin

import django_filters
import pandas
import altair
from django_filters.views import FilterView

from request.models import Request


class StatisticView(TemplateView):
    template_name = "statistic/statistic.html"
    title = "Statistik"
    header_icon = "table"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        unique_visits = (
            Request.objects.exclude(referer__startswith=self.request.site.root_url)
            .exclude(
                referer__startswith=self.request.site.root_url.replace("https", "http")
            )
            .exclude(referer__startswith=self.request.site.root_url.replace("www", ""))
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


class BrowseRequestsView(FilterView, SpreadsheetExportMixin):
    template_name = "statistic/browse_requests.html"
    title = "Statistik"
    header_icon = "table"
    queryset = Request.objects.all()
    context_object_name = "requests"
    paginate_by = 100
    filterset_class = RequestFilter

    list_export = [
        "time",
        "method",
        "path",
        "referer",
        "response",
        "user_agent",
        "browser",
        "user",
        "language",
        "ip",
    ]

    def filter_queryset(self, queryset):
        # used for exports
        filters = self.filterset_class(self.request.GET, queryset=queryset)
        queryset = filters.qs
        return filters, queryset

    def dispatch(self, request, *args, **kwargs):
        # used for exports
        self.is_export = self.request.GET.get("export") in self.FORMATS
        if self.is_export:
            self.paginate_by = None
            return self.as_spreadsheet(
                self.filter_queryset(self.get_queryset())[1],
                self.request.GET.get("export"),
            )
        return super().dispatch(request, *args, **kwargs)


def plot(request):
    filtered = RequestFilter(request.GET, queryset=Request.objects.all())
    data = (
        filtered.qs.annotate(hour=TruncHour("time"))
        .values("hour")
        .annotate(count=Count("id"))
        .order_by()
    )
    df = pandas.DataFrame.from_records(data)

    chart = (
        altair.Chart(df)
        .mark_bar(color="green")
        .encode(
            x=altair.X("hour:T", title="Zeitpunkt"),
            y=altair.Y("count:Q", title="Aufrufe pro Stunde"),
            tooltip=[
                altair.Tooltip("hour", format="%d.%m. %H Uhr", title="Zeitpunkt"),
                altair.Tooltip("count", title="Aufrufe"),
            ],
        )
        .properties(width=1000)
        .interactive()
    )
    return HttpResponse(chart.to_json(), content_type="application/json")
