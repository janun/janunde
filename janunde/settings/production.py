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

# save staticfiles using whitenoise
STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

# save media files in S3
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_KEY']
AWS_STORAGE_BUCKET_NAME = os.environ['S3_BUCKET']
AWS_QUERYSTRING_AUTH = False


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
