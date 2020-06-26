from django.conf.urls import url
from django.urls import reverse

from wagtail.core import hooks
from wagtail.admin.menu import MenuItem

from .views import LatestChangesView


@hooks.register("register_admin_urls")
def register_latest_changes_url():
    return [
        url(r"^latest_changes/$", LatestChangesView.as_view(), name="latest_changes"),
    ]


@hooks.register("register_reports_menu_item")
def register_latest_changes_menu_item():
    return MenuItem(
        "Letzte Änderungen",
        reverse("latest_changes"),
        classnames="icon icon-date",
        order=100,
    )
