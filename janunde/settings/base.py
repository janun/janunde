"""
Django settings for janunde project.

Generated by 'django-admin startproject' using Django 1.8.7.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import dj_database_url
from whitenoise.storage import CompressedManifestStaticFilesStorage


PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(PROJECT_DIR)


# Application definition
INSTALLED_APPS = [
    "core",
    "events",
    "contact",
    "about",
    "navbar",
    "jobs",
    "staff",
    "statistic",
    "latest_changes",
    "wagtail_ping_google",
    "banners",
    "wimmelbilder",
    # 'debug_toolbar',
    # 'template_profiler_panel',
    "request",
    "django_filters",
    "form_utils",
    "softhyphen",
    "wagtail.contrib.table_block",
    "wagtail.contrib.modeladmin",
    "wagtail.contrib.settings",
    "wagtail.contrib.search_promotions",
    "wagtail.contrib.forms",
    "wagtail.contrib.redirects",
    "wagtail.embeds",
    "wagtail.sites",
    "wagtail.users",
    "wagtail.snippets",
    "wagtail.documents",
    "wagtail.images",
    "wagtail.search",
    "wagtail.admin",
    "wagtail.core",
    "modelcluster",
    "storages",
    "taggit",
    "django.forms",
    "django.contrib.humanize",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sitemaps",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "statistic.middleware.StatisticMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "wagtail.core.middleware.SiteMiddleware",
    "wagtail.contrib.redirects.middleware.RedirectMiddleware",
    "django.middleware.gzip.GZipMiddleware",
]

ROOT_URLCONF = "janunde.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(PROJECT_DIR, "templates"),],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "wagtail.contrib.settings.context_processors.settings",
                "janunde.context_processors.google_verification_id",
            ],
        },
    },
]

FORM_RENDERER = "django.forms.renderers.TemplatesSetting"


CACHES = {"default": {"BACKEND": "django.core.cache.backends.dummy.DummyCache",}}


WSGI_APPLICATION = "janunde.wsgi.application"


AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {"min_length": 8,},
    },
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",},
]


# Parse database configuration from env var DATABASE_URL
DATABASES = {
    "default": dj_database_url.config(
        default="postgres://janunde:janunde@localhost/janunde_db", conn_max_age=600
    )
}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/
LANGUAGE_CODE = "de-de"
TIME_ZONE = "Europe/Berlin"
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "django_node_assets.finders.NodeModulesFinder",
)

STATICFILES_DIRS = (
    # os.path.join(PROJECT_DIR, "static"),
    # os.path.join(BASE_DIR, "node_modules"),
)

STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATIC_URL = "/static/"

NODE_MODULES_ROOT = os.path.join(BASE_DIR, "node_modules")

# save staticfiles using whitenoise


class MyCompressedManifestStaticFilesStorage(CompressedManifestStaticFilesStorage):
    manifest_strict = False


STATICFILES_STORAGE = "janunde.settings.base.MyCompressedManifestStaticFilesStorage"


MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"


# Wagtail settings
WAGTAIL_SITE_NAME = "janunde"
WAGTAILIMAGES_JPEG_QUALITY = 85
WAGTAILIMAGES_IMAGE_MODEL = "core.AttributedImage"
WAGTAILIMAGES_FORMAT_CONVERSIONS = {"bmp": "jpeg", "webp": "webp"}


TAGGIT_CASE_INSENSITIVE = True


PHONENUMBER_DEFAULT_REGION = "DE"
PHONENUMBER_DB_FORMAT = "RFC3966"

INTERNAL_IPS = (
    "0.0.0.0",
    "127.0.0.1",
)

ALLOWED_HOSTS = ["*"]

DEBUG_TOOLBAR_PANELS = [
    "debug_toolbar.panels.versions.VersionsPanel",
    "debug_toolbar.panels.timer.TimerPanel",
    "debug_toolbar.panels.settings.SettingsPanel",
    "debug_toolbar.panels.headers.HeadersPanel",
    "debug_toolbar.panels.request.RequestPanel",
    "debug_toolbar.panels.sql.SQLPanel",
    "debug_toolbar.panels.staticfiles.StaticFilesPanel",
    "debug_toolbar.panels.templates.TemplatesPanel",
    "debug_toolbar.panels.cache.CachePanel",
    "debug_toolbar.panels.signals.SignalsPanel",
    "debug_toolbar.panels.logging.LoggingPanel",
    "debug_toolbar.panels.redirects.RedirectsPanel",
    "debug_toolbar.panels.profiling.ProfilingPanel",
    "template_profiler_panel.panels.template.TemplateProfilerPanel",
]

LOGIN_REDIRECT_URL = "wagtailadmin_home"


PASSWORD_REQUIRED_TEMPLATE = "password_required.html"


# https://django-request.readthedocs.io/en/latest/settings.html
REQUEST_IGNORE_PATHS = (
    r"^admin/",
    r"^images/",
    r"wp-admin",
    r"ads\.txt",
    r"\.env",
    r"\.php$",
)

REQUEST_IGNORE_USER_AGENTS = (
    r"^$",
    r"(?i)bot",
    r"(?i)spider",
    r"(?i)spyder",
    r"(?i)crawler",
    r"(?i)parser",
    r"(?i)http",
    r"(?i)buck",
    r"(?i)qwantify",
    r"(?i)facebookexternalhit",
    r"(?i)whatsapp",
    r"(?i)http.*client",
    r"(?i)python",
    r"(?i)cortex",
    r"(?i)adreview",
    r"(?i)wordpress",
    r"Opera\/9.80 \(Windows NT 6.2; Win64; x64\) Presto\/2.12.388 Version\/12.16",
)

REQUEST_VALID_METHOD_NAMES = ("get", "post")

REQUEST_ANONYMOUS_IP = True
