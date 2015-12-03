from django.apps import apps
from .utils import this_app

from django.contrib.staticfiles.finders import AppDirectoriesFinder as DjangoStaticFilesFinder

class StaticFilesFinder(DjangoStaticFilesFinder):
    source_dir = this_app.absolute_styles_dir

    def __init__(self, *args, **kwargs):
        super(StaticFilesFinder, self).__init__(app_names=(this_app.name,) ,*args, **kwargs)

    def list(self, ignore_patterns):
        super(StaticFilesFinder, self).list(ignore_patterns=('*.html',) ,*args, **kwargs)


from django.template.loaders.app_directories import Loader as DjangoTemplateLoader

class TemplateLoader(DjangoTemplateLoader):
    def get_template_sources(self, template_name, template_dirs=None):
        ret = super(TemplateLoader, self).get_template_sources(
            template_name,
            template_dirs=[this_app.absolute_styles_dir],
        )
        return ret
