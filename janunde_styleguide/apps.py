from django.apps import AppConfig
import os


# We have some important settings stored here
# you can use them like this:
#
#   from django.apps import apps
#   apps.get_app_config('janunde_styleguide').absolute_styles_dir
#
class JanundeStyleguideConfig(AppConfig):
    name = 'janunde_styleguide'
    verbose_name = 'janun.de Styleguide'

    styles_dir = 'styles'

    @property
    def absolute_styles_dir(self):
        return os.path.join(self.path, self.styles_dir)
