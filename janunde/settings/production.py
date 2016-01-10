from .base import *

# Set Debug after environment variable
DEBUG = os.environ.get('DJANGO_DEBUG', '').lower() in ('yes', 'true', '1')

# Load special local settings if specified
try:
    from .local import *
except ImportError:
    pass


# Security Settings
# We could disable newer browsers not to use this site without ssl
# for specified number of seconds
# but only if we not wanted them to be able to use non-ssl!
#SECURE_HSTS_SECONDS = 0
# Send the header: x-content-type-options: nosniff
SECURE_CONTENT_TYPE_NOSNIFF = True
# Send the header: x-xss-protection: 1; mode=block
SECURE_BROWSER_XSS_FILTER = True
# redirect http to https
SECURE_SSL_REDIRECT = True
# use a secure-only session cookie
SESSION_COOKIE_SECURE = True
# secure-only CSRF cookie
CSRF_COOKIE_SECURE = True
# HttpOnly CSRF cookie
CSRF_COOKIE_HTTPONLY = True
# no x frames
X_FRAME_OPTIONS = 'DENY'
# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
# Allow all host headers
ALLOWED_HOSTS = ['*']

# Get secret key from environment variable
SECRET_KEY = os.environ['SECRET_KEY']

# Parse database configuration from $DATABASE_URL
import dj_database_url
DATABASES['default'] =  dj_database_url.config()

# save staticfiles using whitenoise
STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

# compress files via django-compress before starting app
COMPRESS_ENABLED = True
COMPRESS_OFFLINE = True
COMPRESS_CSS_HASHING_METHOD = 'content'

# minify
#HTML_MINIFY = True

# Use the cached template loader
TEMPLATES[0]['OPTIONS']['loaders'] = (
    ('django.template.loaders.cached.Loader', (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )),
)
TEMPLATES[0]['APP_DIRS'] = False

# CACHE
MIDDLEWARE_CLASSES = ('django.middleware.cache.UpdateCacheMiddleware',) + MIDDLEWARE_CLASSES
MIDDLEWARE_CLASSES = MIDDLEWARE_CLASSES + ('django.middleware.cache.FetchFromCacheMiddleware',)

#CACHE_MIDDLEWARE_ALIAS
#CACHE_MIDDLEWARE_SECONDS
CACHE_MIDDLEWARE_KEY_PREFIX = ''
