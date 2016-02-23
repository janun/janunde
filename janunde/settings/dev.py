from .base import *

try:
    from .local import *
except ImportError:
    pass
    

DEBUG = True

for template_engine in TEMPLATES:
    template_engine['OPTIONS']['debug'] = True

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Get secret key from environment variable
# but with a default (as opposed to production)
SECRET_KEY = os.environ.get(
    'SECRET_KEY',
    'adaeföaehraoehcröcahömthcartmhghfdsgjhdfguhrg5zut3zu52z43jkjcoi;a!yfe'
)

INSTALLED_APPS += [
    'wagtail.contrib.wagtailstyleguide',
]
