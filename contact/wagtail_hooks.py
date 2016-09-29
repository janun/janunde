import datetime
from django.contrib import admin
from django.db.models import Q


from wagtail.contrib.modeladmin.options import (
    ModelAdmin, ModelAdminGroup, modeladmin_register)
from .models import PersonPage


class PersonPageModelAdmin(ModelAdmin):
    model = PersonPage
    menu_icon = 'user'
    menu_order = 201
    add_to_settings_menu = False
    list_display = ('title', 'role')
    list_filter = ('role',)
    search_fields = ('title',)
    ordering = ('title',)

modeladmin_register(PersonPageModelAdmin)
