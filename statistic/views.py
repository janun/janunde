import datetime

from django.db.models import Count
from django.views.generic import TemplateView
from django.http import HttpResponse
from django.db.models.functions import TruncHour
from django.urls import reverse

from wagtail.admin.views.reports import SpreadsheetExportMixin
from wagtail.core.models import Site

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
        queryset = Request.objects.exclude(user__isnull=False)  # exclude logged in

        site = Site.find_for_request(self.request)

        unique_visits = (
            queryset.exclude(referer__startswith=site.root_url)
            .exclude(
                referer__startswith=site.root_url.replace("https", "http")
            )
            .exclude(referer__startswith=site.root_url.replace("www", ""))
        )

        context["visits_today"] = unique_visits.today().count()
        context["visits_this_week"] = unique_visits.this_week().count()
        context["visits_this_month"] = unique_visits.this_month().count()

        context["top_paths"] = (
            queryset.filter(response__lt=400)
            .values("path")
            .annotate(Count("path"))
            .order_by("-path__count")[:10]
        )

        context["top_referers"] = (
            unique_visits.exclude(referer="")
            .values("referer")
            .annotate(Count("referer"))
            .order_by("-referer__count")[:10]
        )

        context["top_error_paths"] = (
            queryset.filter(response__gte=400)
            .values("path", "response")
            .annotate(Count("path"))
            .order_by("-path__count")[:10]
        )
        return context


class FilterSetWithInitials:
    """Mixin enabling a FilterSets filters to have initial values"""

    def __init__(self, data=None, *args, **kwargs):
        if data is None:
            data = {}
        data = data.copy()
        for name, f in self.base_filters.items():
            initial = f.extra.get("initial")
            if not data.get(name) and initial is not None:
                data[name] = initial
        super().__init__(data, *args, **kwargs)


class RequestFilter(FilterSetWithInitials, django_filters.FilterSet):
    logged_in = django_filters.BooleanFilter(
        field_name="user",
        lookup_expr="isnull",
        label="Eingeloggt",
        exclude=True,
        initial=False,
    )
    path = django_filters.Filter(label="Seite")
    referer = django_filters.Filter(label="Herkunft")
    time = django_filters.DateTimeFromToRangeFilter()

    class Meta:
        model = Request
        fields = ("path", "time", "referer", "logged_in")


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
    """Create json data for plot using Vega/Altair"""
    filtered = RequestFilter(request.GET, queryset=Request.objects.all())
    data = (
        filtered.qs.annotate(hour=TruncHour("time"))
        .values("hour")
        .annotate(count=Count("id"))
        .order_by()
    )
    df = pandas.DataFrame.from_records(data)

    def get_url(hour: pandas.Timestamp):
        """generate url to browse page"""
        nexthour = hour + datetime.timedelta(hours=1)
        return (
            reverse("statistic_browse")
            + f"?time_after={hour.strftime('%d.%m.%Y %H:%M')}&time_before={nexthour.strftime('%d.%m.%Y %H:%M')}"
        )

    df["url"] = df["hour"].apply(get_url)

    chart = (
        altair.Chart(df)
        .mark_bar(color="green")
        .encode(
            x=altair.X("hour:T", title="Zeitpunkt"),
            y=altair.Y("count:Q", title="Aufrufe pro Stunde"),
            href="url:N",
            tooltip=[
                altair.Tooltip("hour", format="%d.%m. %H Uhr", title="Zeitpunkt"),
                altair.Tooltip("count", title="Aufrufe"),
            ],
        )
        .properties(width=1000)
    )
    return HttpResponse(chart.to_json(), content_type="application/json")
