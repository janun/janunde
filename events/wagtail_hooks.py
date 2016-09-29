import datetime
from django.contrib import admin
from django.db.models import Q


from wagtail.contrib.modeladmin.options import (
    ModelAdmin, ModelAdminGroup, modeladmin_register)
from .models import EventPage


class DatetimeListFilter(admin.SimpleListFilter):
    title = 'Zeitpunkt'
    parameter_name = 'start_datetime'

    def lookups(self, request, model_admin):
        return (
            ('upcoming', 'anstehend'),
            ('expired', 'abgelaufen')
        )

    def queryset(self, request, queryset):
        today = datetime.date.today()
        if self.value() == 'upcoming':
            return EventPage.objects.upcoming()
        if self.value() == 'expired':
            return EventPage.objects.expired()



class EventPageModelAdmin(ModelAdmin):
    model = EventPage
    menu_icon = 'date'
    menu_order = 200
    add_to_settings_menu = False
    list_display = ('title', 'start_datetime', 'location', 'related_group')
    list_filter = (DatetimeListFilter, 'related_group')
    search_fields = ('title', 'content', 'location')
    #ordering = ('start_datetime',)

modeladmin_register(EventPageModelAdmin)
