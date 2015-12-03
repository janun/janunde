from django.core.management.base import BaseCommand, CommandError
import os
from django.conf import settings

def get_scss_files(pattern_dir, all_scss):
    paths = []
    for (dirpath, dirnames, filenames) in os.walk(pattern_dir):
        for filename in filenames:
            if not filename.endswith('.scss'):
                continue
            path = os.path.join(dirpath, filename)
            if path == all_scss:
                continue
            paths.append(path)
    return paths

def update_all_scss(pattern_dir, all_scss):
    """updates all.scss"""
    file = open(all_scss, 'w')
    file.truncate
    for path in get_scss_files(pattern_dir, all_scss):
        path = os.path.relpath(path, os.path.dirname(all_scss))
        file.write( '@import "{}";\n'.format(path) )


class Command(BaseCommand):
    help = 'updates the pattern librarys all.scss'
    pattern_dir = os.path.join(settings.BASE_DIR, 'styles', 'patterns')
    all_scss = os.path.join(settings.BASE_DIR, 'styles', 'patterns', 'all_janunde_styles.scss')

    def handle(self, *args, **options):
        update_all_scss(self.pattern_dir, self.all_scss)
        self.stdout.write('Updated %s' % self.all_scss)
