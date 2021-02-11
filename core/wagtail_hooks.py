from django.utils.html import format_html_join
from django.conf import settings

from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register


from .models import Article


class ArticleModelAdmin(ModelAdmin):
    model = Article
    menu_icon = "doc-full"
    list_per_page = 10
    menu_order = 202
    add_to_settings_menu = False
    list_display = ("title", "author", "first_published_at")
    list_filter = ("first_published_at",)
    search_fields = ("title", "body")
    ordering = ("-first_published_at",)


modeladmin_register(ArticleModelAdmin)
