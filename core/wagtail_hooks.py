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
            //'halloheadings': {formatBlocks: []},
            'hallolists': {},
            //'hallohr': {},
            'halloreundo': {},
            'hallowagtaillink': {},
            'hallorequireparagraphs': {},
            'hallowagtaildoclink': {},
          };
        </script>
    """


# hide images and embeds
# they should be done using streamfield
@hooks.register('insert_editor_css')
def editor_css():
    return '<style>.hallowagtailimage, ' \
        '.hallowagtailembeds { display: none; }</style>'
