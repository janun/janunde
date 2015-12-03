from .base import *

# Unset Debug
DEBUG = False

# Load special local settings if specifieds
try:
    from .local import *
except ImportError:
    pass


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


# Parse database configuration from $DATABASE_URL
import dj_database_url
DATABASES['default'] =  dj_database_url.config()

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']

# Get secret key from environment variable
SECRET_KEY = os.environ['SECRET_KEY']

# staticfiles settings (whitenoise)
STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

COMPRESS_OFFLINE = True
COMPRESS_CSS_FILTERS = [
    'compressor.filters.css_default.CssAbsoluteFilter',
    'compressor.filters.cssmin.CSSMinFilter',
]
COMPRESS_CSS_HASHING_METHOD = 'content'
