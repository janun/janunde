from django.db.models import Count

from wagtail.admin.views.reports import ReportView
from django.views.generic import TemplateView

# import django_filters
from request.models import Request


# class RequestFilter(django_filters.FilterSet):
#     time_period =
#     class Meta:
#         model = Request


class StatisticView(TemplateView):
    template_name = "statistic/statistic.html"
    title = "Statistik"
    header_icon = "table"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["hits_today"] = Request.objects.today().count()
        context["hits_this_week"] = Request.objects.this_week().count()
        context["hits_this_month"] = Request.objects.this_month().count()
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
            Request.objects.exclude(referer__startswith=self.request.site.root_url)
            .exclude(referer="")
            .values("referer")
            .annotate(Count("referer"))
            .order_by("-referer__count")[:10]
        )
        return context


class BrowseRequestsView(ReportView):
    template_name = "statistic/browse_requests.html"
    title = "Statistik"
    header_icon = "table"
    queryset = Request.objects.today()
    context_object_name = "requests"
    paginate_by = 200

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["hits_today"] = Request.objects.today().count()
        return context

