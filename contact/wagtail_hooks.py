from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register
from .models import PersonPage


class PersonPageModelAdmin(ModelAdmin):
    model = PersonPage
    menu_icon = "user"
    menu_order = 201
    list_per_page = 10
    add_to_settings_menu = False
    list_display = ("title", "role")
    list_filter = ("role",)
    search_fields = ("title",)
    ordering = ("title",)


modeladmin_register(PersonPageModelAdmin)
