from .base import *

DEBUG = False

try:
    from .local import *
except ImportError:
    pass


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
