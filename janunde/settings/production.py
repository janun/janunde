import os

from .base import *

try:
    from .local import *
except ImportError:
    pass


# Set Debug after environment variable
DEBUG = os.environ.get('DJANGO_DEBUG', '').lower() in ('yes', 'true', '1')

# Set SSL after environment variable, defaulting to true
SSL = os.environ.get('SSL', '').lower() not in ('no', 'false', '0')

# Security Settings
SECRET_KEY = os.environ['SECRET_KEY']

if SSL:
    # disable usage of non-ssl connection
    SECURE_HSTS_SECONDS = 3600

# Send the header: x-content-type-options: nosniff
SECURE_CONTENT_TYPE_NOSNIFF = True
# Send the header: x-xss-protection: 1; mode=block
SECURE_BROWSER_XSS_FILTER = True
# redirect http to https
SECURE_SSL_REDIRECT = SSL
# use a secure-only session cookie
SESSION_COOKIE_SECURE = SSL
# secure-only CSRF cookie
CSRF_COOKIE_SECURE = SSL
# HttpOnly CSRF cookie
CSRF_COOKIE_HTTPONLY = True
# no x frames
X_FRAME_OPTIONS = 'DENY'
# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']

# save media files in S3
if 'AWS_ACCESS_KEY' in os.environ:
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
    AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY']
    AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_KEY']
    AWS_STORAGE_BUCKET_NAME = os.environ['S3_BUCKET']
    AWS_QUERYSTRING_AUTH = False
    AWS_HEADERS = {  # see http://developer.yahoo.com/performance/rules.html#expires
            'Expires': 'Thu, 31 Dec 2099 20:00:00 GMT',
            'Cache-Control': 'max-age=94608000',
        }


# Use the cached template loader
TEMPLATES[0]['OPTIONS']['loaders'] = (
    ('django.template.loaders.cached.Loader', (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )),
)
TEMPLATES[0]['APP_DIRS'] = False

# CACHE
# (cannot be used until we have a cache backend??)
#MIDDLEWARE_CLASSES = ('django.middleware.cache.UpdateCacheMiddleware',) + MIDDLEWARE_CLASSES
#MIDDLEWARE_CLASSES = MIDDLEWARE_CLASSES + ('django.middleware.cache.FetchFromCacheMiddleware',)

#CACHE_MIDDLEWARE_ALIAS
#CACHE_MIDDLEWARE_SECONDS
#CACHE_MIDDLEWARE_KEY_PREFIX = ''


BONSAI_URL = os.environ.get('BONSAI_URL', '')
SEARCHBOX_SSL_URL = os.environ.get('SEARCHBOX_SSL_URL', '')

if SEARCHBOX_SSL_URL:
    import certifi
    WAGTAILSEARCH_BACKENDS = {
        'default': {
            'BACKEND': 'wagtail.wagtailsearch.backends.elasticsearch',
            'URLS': [SEARCHBOX_SSL_URL ],
            'INDEX': 'wagtail',
            'TIMEOUT': 5,
            'ca_certs': certifi.where(),
        }
    }

elif BONSAI_URL:
    import certifi
    WAGTAILSEARCH_BACKENDS = {
        'default': {
            'BACKEND': 'wagtail.wagtailsearch.backends.elasticsearch2',
            'URLS': [BONSAI_URL ],
            'INDEX': 'wagtail',
            'TIMEOUT': 5,
            'ca_certs': certifi.where(),
        }
    }


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
        },
    },
}


ROLLBAR_ACCESS_TOKEN = os.environ.get('ROLLBAR_ACCESS_TOKEN', '')
ROLLBAR_ACCESS_TOKEN_JS = os.environ.get('ROLLBAR_ACCESS_TOKEN_JS', '')
if ROLLBAR_ACCESS_TOKEN:
    ROLLBAR = {
        'access_token': ROLLBAR_ACCESS_TOKEN,
        'environment': 'development' if DEBUG else 'production',
        'branch': 'production',
        'root': '/',
    }


BETABANNER = os.environ.get('BETABANNER', '').lower() in ('yes', 'true', '1')
FREESURVEYCREATOR_ID = os.environ.get('FREESURVEYCREATOR_ID', '')
PIWIK_URL = os.environ.get('PIWIK_URL', '')
MOUSEFLOW_ID = os.environ.get('MOUSEFLOW_ID', '')
GOOGLE_VERIFICATION_ID = os.environ.get('GOOGLE_VERIFICATION_ID', '')

EMAIL_HOST = os.environ.get('EMAIL_HOST', '')
EMAIL_PORT = os.environ.get('EMAIL_PORT', '')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
EMAIL_USE_SSL = os.environ.get('EMAIL_USE_SSL', '').lower() in ('yes', 'true', '1')
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', '').lower() in ('yes', 'true', '1')
