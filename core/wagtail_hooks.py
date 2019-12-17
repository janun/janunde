from wagtail.core import hooks
from wagtail.images import image_operations
from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register

from .models import Article


# add the operation to convert an image to jpg to the image tag
class ConvertToJPGOperation(image_operations.Operation):
    def construct(self):
        pass

    def run(self, willow, image):
        willow.original_format = "jpeg"


@hooks.register("register_image_operations")
def register_image_operations():
    return [
        ("jpg", ConvertToJPGOperation),
    ]


# https://github.com/torchbox/wagtail/issues/2483
@hooks.register("insert_editor_js")
def change_datetimepicker_format():
    return """
    <script>
      function initDateTimeChooser(id, opts) {
        if (window.dateTimePickerTranslations) {
            $('#' + id).datetimepicker($.extend({
                closeOnDateSelect: true,
                format: 'd.m.Y H:i',
                scrollInput:false,
                i18n: {
                    lang: window.dateTimePickerTranslations
                },
                language: 'lang'
            }, opts || {}));
        } else {
            $('#' + id).datetimepicker($.extend({
                format: 'd.m.Y H:i'
            }, opts || {}));
        }
    }
    </script>
    """


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
