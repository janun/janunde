from .base import *


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

for template_engine in TEMPLATES:
    template_engine['OPTIONS']['debug'] = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '#jzmpp6wgxxl1#v$#zhvd=50ga=zskelu-synaw+qa1#1zk=#r'


EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


try:
    from .local import *
except ImportError:
    pass

INSTALLED_APPS += [
    'wagtail.contrib.wagtailstyleguide',
]
