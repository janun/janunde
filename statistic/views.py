from django.db.models import Count, Sum
from django.views.generic import TemplateView
from django.http import HttpResponse
from django.db.models.functions import TruncHour

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
    queryset = Request.objects.all()
    context_object_name = "requests"
    paginate_by = 100
    filterset_class = RequestFilter


def plot(request):
    data = (
        Request.objects.annotate(hour=TruncHour("time"))
        .values("hour")
        .annotate(count=Count("id"))
        .order_by()
    )
    df = pandas.DataFrame.from_records(data)

    chart = (
        altair.Chart(df)
        .mark_area(
            line={"color": "darkgreen"},
            color=altair.Gradient(
                gradient="linear",
                stops=[
                    altair.GradientStop(color="white", offset=0),
                    altair.GradientStop(color="darkgreen", offset=1),
                ],
                x1=1,
                x2=1,
                y1=1,
                y2=0,
            ),
        )
        .encode(
            x=altair.X("hour:T", title="Zeitpunkt"),
            y=altair.Y("count:Q", title="Aufrufe"),
        )
        .properties(width=1000)
    )
    return HttpResponse(chart.to_json(), content_type="application/json")
