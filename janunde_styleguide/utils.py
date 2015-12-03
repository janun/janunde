import os
from django.conf import settings
from django.apps import apps

this_app = apps.get_app_config('janunde_styleguide')

absolute_styles_dir = this_app.absolute_styles_dir

def get_pages():
    """generates a list of pages [(name, rel_path), ...]"""
    pages = []
    for (dirpath, dirnames, filenames) in os.walk(absolute_styles_dir):
        for filename in filenames:
            if filename == '_doc.html':
                path = os.path.relpath(dirpath, absolute_styles_dir)
                name = os.path.basename(os.path.normpath(dirpath))
                pages.append( (name, path) )
    return pages
