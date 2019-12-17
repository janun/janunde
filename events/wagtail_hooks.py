from django.contrib import admin

from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register

from .models import EventPage


class DatetimeListFilter(admin.SimpleListFilter):
    title = "Zeitpunkt"
    parameter_name = "start_datetime"

    def lookups(self, request, model_admin):
        return (("upcoming", "anstehend"), ("expired", "abgelaufen"))

    def queryset(self, request, queryset):
        if self.value() == "upcoming":
            return EventPage.objects.upcoming()
        if self.value() == "expired":
            return EventPage.objects.expired()


class EventPageModelAdmin(ModelAdmin):
    model = EventPage
    menu_icon = "date"
    list_per_page = 10
    menu_order = 200
    add_to_settings_menu = False
    list_display = ("title", "start_datetime", "location", "related_group")
    list_filter = (DatetimeListFilter, "related_group")
    search_fields = ("title", "content", "location")


modeladmin_register(EventPageModelAdmin)
