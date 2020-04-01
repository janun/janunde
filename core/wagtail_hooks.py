from django.utils.html import format_html_join
from django.conf import settings

from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register
import wagtail.admin.rich_text.editors.draftail.features as draftail_features
from wagtail.core import hooks

from .rich_text import (
    AnchorIndentifierEntityElementHandler,
    anchor_identifier_entity_decorator,
)


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


@hooks.register("register_rich_text_features")
def register_rich_text_anchor_identifier_feature(features):
    """
    Registering the `anchor-identifier` feature, which uses the `ANCHOR-IDENTIFIER` Draft.js entity type,
    and is stored as HTML with a `<span id="my-anchor">` tag.
    """
    features.default_features.append("anchor-identifier")
    feature_name = "anchor-identifier"
    type_ = "ANCHOR-IDENTIFIER"

    control = {
        "type": type_,
        "label": "#id",
        "description": "Anker",
    }

    features.register_editor_plugin(
        "draftail", feature_name, draftail_features.EntityFeature(control)
    )

    features.register_converter_rule(
        "contentstate",
        feature_name,
        {
            # Note here that the conversion is more complicated than for blocks and inline styles.
            # 'from_database_format': {'a[data-anchor][id]': AnchorIndentifierEntityElementHandler(type_)},
            "from_database_format": {
                "span[data-id]": AnchorIndentifierEntityElementHandler(type_)
            },
            "to_database_format": {
                "entity_decorators": {type_: anchor_identifier_entity_decorator}
            },
        },
    )


@hooks.register("insert_editor_js")
def insert_editor_js():
    js_files = [
        # We require this file here to make sure it is loaded before the other.
        "wagtailadmin/js/draftail.js",
        "core/scripts/wagtail_draftail_anchor.js",
    ]
    js_includes = format_html_join(
        "\n",
        '<script src="{0}{1}"></script>',
        ((settings.STATIC_URL, filename) for filename in js_files),
    )
    return js_includes
