from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register
from .models import Employee


class EmployeeModelAdmin(ModelAdmin):
    model = Employee
    menu_icon = "user"
    menu_order = 201
    list_per_page = 10
    add_to_settings_menu = False
    list_display = ("title", "department", "role", "last_published_at", "has_unpublished_changes")
    list_filter = ("department",)
    search_fields = ("title",)
    ordering = ("title",)


modeladmin_register(EmployeeModelAdmin)
