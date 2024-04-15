from os import environ, path
import os
from pathlib import Path
import sentry_sdk
from django.core.management.utils import get_random_secret_key
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.templatetags.static import static
from dotenv import load_dotenv
import os

from .template import TEMPLATE_CONFIG, THEME_LAYOUT_DIR, THEME_VARIABLES
from google.oauth2 import service_account
import firebase_admin
from firebase_admin import initialize_app, credentials, storage
from google.auth import load_credentials_from_file

load_dotenv()  # take environment variables from .env.
######################################################################
# General
######################################################################
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = environ.get("SECRET_KEY", get_random_secret_key())

DEBUG = environ.get("DEBUG", "") == "1"

ALLOWED_HOSTS = [
    "beetrootapi.greatssystems.co.zw",
    "154.41.254.152",
    "localhost",
    "api",
    "127.0.0.1",
    "172.23.177.0",
]
# ALLOWED_HOSTS = ["localhost", "api", '127.0.0.1', '172.23.177.0']

# CORS_ORIGIN_ALLOW_ALL = True

CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

WSGI_APPLICATION = "backend.wsgi.application"
ASGI_APPLICATION = "backend.asgi.application"
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("127.0.0.1", 6379)],
        },
    },
}
ROOT_URLCONF = "backend.urls"
X_FRAME_OPTIONS = "SAMEORIGIN"  # allows you to use modals insated of popups
SILENCED_SYSTEM_CHECKS = ["security.W019"]  # ignores redundant warning messages
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# uncomment change here
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.join(BASE_DIR, 'beetrootappfirebaseadminsdk.json')
# FIREBASE_CREDENTIALS = service_account.Credentials.from_service_account_file(
#     os.path.join(BASE_DIR, 'beetrootappfirebaseadminsdk.json')
# )


# cred = credentials.Certificate(os.path.join(BASE_DIR, 'beetrootappfirebaseadminsdk.json'))
# firebase_admin.initialize_app(cred)

# # Configure the storage bucket
# GS_BUCKET_NAME = 'geza-marketplace-9334d.appspot.com'
# FIREBASE_BUCKET = storage.bucket(app=firebase_admin.get_app(name='media_upload_app'))
# # CSRF_TRUSTED_ORIGINS = environ.get(
# #     "CSRF_TRUSTED_ORIGINS", "http://localhost:8000"
# # ).split(",")
######################################################################
# Apps
######################################################################
INSTALLED_APPS = [
    "daphne",
    "wagtail.api.v2",
    "unfold",
    "unfold.contrib.filters",
    "unfold.contrib.import_export",
    "unfold.contrib.guardian",
    "unfold.contrib.simple_history",
    "unfold.contrib.forms",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "rest_framework.authtoken",
    "rest_framework_simplejwt",
    "drf_spectacular",
    "backend",
    # 'channels',
    "chat",
    "friends",
    "akyc.apps.AKYCConfig",
    "auth.apps.AuthConfig",
    "business.apps.BusinessPortalConfig",
    "dashboards.apps.DashboardsConfig",
    "corsheaders",
    "djoser",
    "django_filters",
    "django_extensions",
    "djangoql",
    "colorfield",
    "drf_yasg",
    "phonenumber_field",
    "publishing",
    # "home",
    "search",
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
    "wagtail",
    "modelcluster",
    "taggit",
    "debug_toolbar",
    "import_export",
    "guardian",
    "simple_history",
    "django_celery_beat",
    "djmoney",
]

######################################################################
# Middleware
######################################################################
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "simple_history.middleware.HistoryRequestMiddleware",
    "backend.middleware.ReadonlyExceptionHandlerMiddleware",
]
######################################################################
# Sessions
######################################################################
SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"

######################################################################
# Templates
######################################################################
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            path.normpath(path.join(BASE_DIR, "templates")),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "dashboards.context_processors.variables",
            ],
        },
    },
]

######################################################################
# Database
######################################################################
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "USER": environ.get("DATABASE_USER", "postgres"),
        "PASSWORD": environ.get("DATABASE_PASSWORD", "change-password"),
        "NAME": environ.get("DATABASE_NAME", "db"),
        "HOST": environ.get("DATABASE_HOST", "db"),
        "PORT": "5432",
        "TEST": {
            "NAME": "test",
        },
    }
}
# Django Database Configuration
# DATABASES = {
#     'default': {
#         'ENGINE': 'django_firebase_app.firebase',
#         'CREDENTIALS': cred,
#         'NAME': 'default',
#     }
# }

######################################################################
# Authentication
######################################################################
AUTH_USER_MODEL = "backend.User"

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]
# LOGIN_URL = "admin:login"

# LOGIN_REDIRECT_URL = reverse_lazy("admin:index")
######################################################################
# Internationalization
######################################################################
LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

######################################################################
# Staticfiles
######################################################################
# STATICFILES_FINDERS = [
#     "django.contrib.staticfiles.finders.FileSystemFinder",
#     "django.contrib.staticfiles.finders.AppDirectoriesFinder",
# ]
# STATICFILES_DIRS = [BASE_DIR / "backend" / "static"]

# STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'
# STATICFILES_DIRS = [
#     os.path.join(PROJECT_DIR, "static"),
# ]

STATIC_URL = "/static/"
MEDIA_URL = "/media/"

STATIC_ROOT = os.path.join(BASE_DIR, "static")
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# Default URL on which Django application runs for specific environment
BASE_URL = os.environ.get(
    "http://beetrootapi.greatssystems.co.zw",
    default="http://beetrootapi.greatssystems.co.zw",
)


# STORAGES = {
#     "default": {
#         "BACKEND": "django.core.files.storage.FileSystemStorage",
#     },
#     "staticfiles": {
#         "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
#     },
# }
######################################################################
# Rest Framework
######################################################################
# REST_FRAMEWORK = {
#     "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
#     "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
#     "PAGE_SIZE": 10,
#     "DEFAULT_PERMISSION_CLASSES": [
#         "rest_framework.permissions.IsAuthenticated",
#     ],
#     "DEFAULT_AUTHENTICATION_CLASSES": [
#         "rest_framework_simplejwt.authentication.JWTAuthentication",
#         "rest_framework.authentication.SessionAuthentication",
#     ],
# }


WAGTAIL_SITE_NAME = "backend"

# Search
# https://docs.wagtail.org/en/stable/topics/search/backends.html
WAGTAILSEARCH_BACKENDS = {
    "default": {
        "BACKEND": "wagtail.search.backends.database",
    }
}

# Base URL to use when referring to full URLs within the Wagtail admin backend -
# e.g. in notification emails. Don't include '/admin' or a trailing slash
WAGTAILADMIN_BASE_URL = BASE_URL

THEME_LAYOUT_DIR = THEME_LAYOUT_DIR
TEMPLATE_CONFIG = TEMPLATE_CONFIG
THEME_VARIABLES = THEME_VARIABLES

# Email Settings
# ------------------------------------------------------------------------------

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = ""
EMAIL_HOST_PASSWORD = ""

# Loginyour mail
# ------------------------------------------------------------------------------
LOGIN_URL = "/login/"
LOGOUT_REDIRECT_URL = "/login/"

# Session
# ------------------------------------------------------------------------------

SESSION_ENGINE = "django.contrib.sessions.backends.db"
# SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = "Lax"

SESSION_COOKIE_AGE = 3600


######################################################################
# Unfold
######################################################################
UNFOLD = {
    "SITE_HEADER": _("Beetroot Admin"),
    "SITE_TITLE": _("Beetroot Admin"),
    "SITE_SYMBOL": "settings",
    "SITE_URL": BASE_URL,
    "ENVIRONMENT": "dashboards.utils.environment_callback",
    "DASHBOARD_CALLBACK": "dashboards.views.dashboard_callback",
    "LOGIN": {
        "image": lambda request: static("images/login-bg.jpg"),
    },
    "STYLES": [
        lambda request: static("css/styles.css"),
    ],
    "SCRIPTS": [
        # lambda request: static("js/chart.min.js"),
    ],
    "COLORS": {
        "primary": {
            "50": "255 245 245",
            "200": "255 176 176",
            "300": "255 115 115",
            "400": "255 61 61",
            "500": "255 0 0",
            "600": "214 0 0",
            "700": "173 0 0",
            "800": "134 0 0",
            "900": "94 0 0",
            "950": "61 0 0",
        },
    },
    "TABS": [
        {
            "models": ["akyc.profile", "business.services"],
            "items": [
                {
                    "title": _("Clients"),
                    "icon": "sports_motorsports",
                    "link": reverse_lazy("admin:akyc_profile_changelist"),
                },
                {
                    "title": _("Premium Account"),
                    "icon": "precision_manufacturing",
                    "link": reverse_lazy("admin:business_service_changelist"),
                },
            ],
        },
        {
            "models": [
                "django_celery_beat.clockedschedule",
                "django_celery_beat.crontabschedule",
                "django_celery_beat.intervalschedule",
                "django_celery_beat.periodictask",
                "django_celery_beat.solarschedule",
            ],
            "items": [
                {
                    "title": _("Clocked"),
                    "icon": "hourglass_bottom",
                    "link": reverse_lazy(
                        "admin:django_celery_beat_clockedschedule_changelist"
                    ),
                },
                {
                    "title": _("Crontabs"),
                    "icon": "update",
                    "link": reverse_lazy(
                        "admin:django_celery_beat_crontabschedule_changelist"
                    ),
                },
                {
                    "title": _("Intervals"),
                    "icon": "arrow_range",
                    "link": reverse_lazy(
                        "admin:django_celery_beat_intervalschedule_changelist"
                    ),
                },
                {
                    "title": _("Periodic tasks"),
                    "icon": "task",
                    "link": reverse_lazy(
                        "admin:django_celery_beat_periodictask_changelist"
                    ),
                },
                {
                    "title": _("Solar events"),
                    "icon": "event",
                    "link": reverse_lazy(
                        "admin:django_celery_beat_solarschedule_changelist"
                    ),
                },
            ],
        },
    ],
    "SIDEBAR": {
        "show_search": True,
        "show_all_applications": True,
        "navigation": [
            {
                "title": _("Navigation"),
                "items": [
                    {
                        "title": _("Analytics"),
                        "icon": "dashboard",
                        "link": reverse_lazy("admin:index"),
                    },
                    {
                        "title": _("Users"),
                        "icon": "sports_motorsports",
                        "link": reverse_lazy("admin:akyc_profile_changelist"),
                    },
                    {
                        "title": _("Stylist"),
                        "icon": "circle",
                        "link": reverse_lazy("admin:business_service_changelist"),
                    },
                    {
                        "title": _("Services"),
                        "icon": "stadium",
                        "link": reverse_lazy("admin:business_service_changelist"),
                        "badge": "dashboards.utils.badge_callback",
                    },
                    {
                        "title": _("Products"),
                        "icon": "grade",
                        "link": reverse_lazy("admin:business_product_changelist"),
                        # "permission": "dashboards.utils.permission_callback",
                        # "permission": lambda request: request.user.is_superuser,
                    },
                ],
            },
            {
                "separator": True,
                "items": [
                    {
                        "title": _("Users"),
                        "icon": "person",
                        "link": reverse_lazy("admin:backend_user_changelist"),
                    },
                    {
                        "title": _("Groups"),
                        "icon": "group",
                        "link": reverse_lazy("admin:auth_group_changelist"),
                    },
                    {
                        "title": _("Tasks"),
                        "icon": "task_alt",
                        "link": reverse_lazy(
                            "admin:django_celery_beat_clockedschedule_changelist"
                        ),
                    },
                ],
            },
        ],
    },
}
######################################################################
# Money
######################################################################
CURRENCIES = ("USD", "EUR")

######################################################################
# App
######################################################################
LOGIN_USERNAME = environ.get("LOGIN_USERNAME")

LOGIN_PASSWORD = environ.get("LOGIN_PASSWORD")

############################################################################
# Debug toolbar
############################################################################
DEBUG_TOOLBAR_CONFIG = {"SHOW_TOOLBAR_CALLBACK": lambda request: DEBUG}

######################################################################
# Plausible
######################################################################
PLAUSIBLE_DOMAIN = environ.get("PLAUSIBLE_DOMAIN")

######################################################################
# Sentry
######################################################################
SENTRY_DSN = environ.get("SENTRY_DSN")

if SENTRY_DSN:
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        enable_tracing=True,
    )
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": os.getenv("DJANGO_LOG_LEVEL", "INFO"),
        },
        "daphne": {
            "handlers": [
                "console",
            ],
            "level": "DEBUG",
        },
    },
}
