from wagtail.wagtailcore import hooks
from wagtail.wagtailimages import image_operations


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
