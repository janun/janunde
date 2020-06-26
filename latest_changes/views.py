from wagtail.admin.views.reports import PageReportView
from wagtail.core.models import Page


class LatestChangesView(PageReportView):
    template_name = "reports/latest_changes.html"
    title = "Letzte Änderungen"
    header_icon = "date"

    def get_queryset(self):
        self.queryset = Page.objects.order_by("-last_published_at")
        return super().get_queryset()
