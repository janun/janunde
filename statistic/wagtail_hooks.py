from django.conf.urls import url
from django.shortcuts import reverse

from wagtail.core import hooks
from wagtail.admin.menu import MenuItem

from .views import StatisticView, BrowseRequestsView, plot


@hooks.register("register_reports_menu_item")
def register_statistic_menu_item():
    return MenuItem(
        "Statistik",
        reverse("statistic"),
        classnames="icon icon-" + StatisticView.header_icon,
        order=700,
    )


@hooks.register("register_admin_urls")
def register_statistic_url():
    return [
        url(r"^reports/statistic/$", StatisticView.as_view(), name="statistic",),
    ]


@hooks.register("register_admin_urls")
def register_browse_url():
    return [
        url(
            r"^reports/statistic/browse$",
            BrowseRequestsView.as_view(),
            name="statistic_browse",
        ),
    ]


@hooks.register("register_admin_urls")
def register_plot_url():
    return [
        url(r"^reports/statistic/plot$", plot, name="statistic_plot",),
    ]
