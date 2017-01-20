from wagtail.wagtailcore import hooks
from wagtail.wagtailimages import image_operations


# add the operation to convert an image to jpg to the image tag
class ConvertToJPGOperation(image_operations.Operation):
    def construct(self):
        pass

    def run(self, willow, image):
        willow.original_format = 'jpeg'


@hooks.register('register_image_operations')
def register_image_operations():
    return [
        ('jpg', ConvertToJPGOperation),
    ]


# limit the richttext editor
# no headings
# no horizontal line
@hooks.register('insert_editor_js')
def editor_js():
    return """
        <script>
          halloPlugins = {
            'halloformat': {},
            'halloheadings': {formatBlocks: ['p', 'h2']},
            'hallolists': {},
            //'hallohr': {},
            'halloreundo': {},
            'hallowagtaillink': {},
            'hallorequireparagraphs': {},
            'hallowagtaildoclink': {},
            'halloblacklist': {tags: ['img', 'html']},
          };
        </script>
    """

# https://github.com/torchbox/wagtail/issues/2483
@hooks.register('insert_editor_js')
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


# hide images and embeds
# they should be done using streamfield
@hooks.register('insert_editor_css')
def editor_css():
    return '<style>' \
        '.hallowagtailimage, .hallowagtailembeds { display: none; }' \
        '.object .object-help { opacity: 1 } // always show help' \
        '</style>'



from wagtail.contrib.modeladmin.options import (
    ModelAdmin, ModelAdminGroup, modeladmin_register)
from .models import Article


class ArticleModelAdmin(ModelAdmin):
    model = Article
    menu_icon = 'doc-full'
    list_per_page = 10
    menu_order = 202
    add_to_settings_menu = False
    list_display = ('title', 'author', 'first_published_at')
    list_filter = ('first_published_at',)
    search_fields = ('title', 'author', 'body')
    ordering = ('first_published_at',)

modeladmin_register(ArticleModelAdmin)
