"""
Django settings for compressorx project.

Generated by 'django-admin startproject' using Django 2.2.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""
import os
from pathlib import Path

import environ


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT_DIR = Path(__file__).resolve(strict=True).parent.parent.parent
APPS_DIR = ROOT_DIR / "apps"

env = environ.Env()
env.read_env(ROOT_DIR / ".env")

# GENERAL
# ------------------------------------------------------------------------------

# SECURITY WARNING: don't run with debug turned on in production!
# https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = env.bool("DEBUG", default=False)


# https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS", default=["api.compressor-x.com"])
CSRF_TRUSTED_ORIGINS = env.list(
    "CSRF_TRUSTED_ORIGINS",
    default=["https://api.compressor-x.com"],
)

# Local time zone. Choices are
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# though not all of them may be available with every OS.
# In Windows, this must be set to your system time zone.
TIME_ZONE = "UTC"
# https://docs.djangoproject.com/en/dev/ref/settings/#language-code
LANGUAGE_CODE = "nl"
# https://docs.djangoproject.com/en/dev/ref/settings/#site-id
SITE_ID = 1
# https://docs.djangoproject.com/en/dev/ref/settings/#use-i18n
USE_I18N = True
# https://docs.djangoproject.com/en/dev/ref/settings/#use-l10n
USE_L10N = True
# https://docs.djangoproject.com/en/dev/ref/settings/#use-tz
USE_TZ = True
# https://docs.djangoproject.com/en/dev/ref/settings/#locale-paths
LOCALE_PATHS = [str(ROOT_DIR / "locale")]

LANGUAGES = [
    ("en", "English"),
    ("fr", "Français"),
    ("nl", "Nederlands"),
]

# DATABASES
# ------------------------------------------------------------------------------

# https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": env.str("DB_NAME", "compressorx"),
        "USER": env.str("DB_USER", "root"),
        "PASSWORD": env.str("DB_PASSWORD", ""),
        "HOST": env.str("DB_HOST", "localhost"),
        "PORT": "3306",
        "OPTIONS": {
            "init_command": "SET sql_mode='STRICT_TRANS_TABLES'; ",
        },
    },
}
# https://docs.djangoproject.com/en/stable/ref/settings/#std:setting-DEFAULT_AUTO_FIELD
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# URLS
# ------------------------------------------------------------------------------

# https://docs.djangoproject.com/en/dev/ref/settings/#root-urlconf
ROOT_URLCONF = "compressorx.urls"
# https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
WSGI_APPLICATION = "compressorx.wsgi.application"


# APPS
# ------------------------------------------------------------------------------
DJANGO_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.admin",
]

THIRD_PARTY_APPS = [
    "corsheaders",  # Adds Cross-Origin Resource Sharing (CORS) headers to responses
    "health_check",  # Health check module
    "health_check.db",  # stock Django health checkers
    "health_check.cache",
    "health_check.storage",
    "health_check.contrib.celery",  # requires celery
    "import_export",  # Import and export data with included admin integration (Excel, CSV, JSON)
    "graphene_django",
    "adminsortable2",
    "martor",
    "mptt",
    "storages",
    "boto3",
    "django_celery_beat",
]
LOCAL_APPS = [
    "apps.action",
    "apps.base",
    "apps.blog",
    "apps.compressed_file",
    "apps.compression",
    "apps.config",
    "apps.config_file",
    "apps.contact",
    "apps.cookies",
    "apps.faq",
    "apps.initial_files",
    "apps.locales",
    "apps.mail",
    "apps.pages",
    "apps.translations",
    "apps.users",
]
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# AUTHENTICATION
# ------------------------------------------------------------------------------

# https://docs.djangoproject.com/en/dev/ref/settings/#authentication-backends
AUTHENTICATION_BACKENDS = [
    "graphql_jwt.backends.JSONWebTokenBackend",
    "django.contrib.auth.backends.ModelBackend",
]
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-user-model
AUTH_USER_MODEL = "users.User"


# PASSWORDS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#password-hashers

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators
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


# MIDDLEWARE
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#middleware
MIDDLEWARE = [
    "apps.base.middleware.AdminModelOverrideMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# STATIC
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#static-root
# aws settings
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = os.getenv("AWS_STORAGE_BUCKET_NAME")
AWS_DEFAULT_ACL = "public-read"
AWS_S3_CUSTOM_DOMAIN = "compressor-x.s3.eu-central-1.amazonaws.com"
AWS_S3_OBJECT_PARAMETERS = {"CacheControl": "max-age=86400"}
# s3 static settings
STATIC_LOCATION = "static"
STATIC_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/{STATIC_LOCATION}/"
STATICFILES_STORAGE = "apps.base.storage_backends.StaticStorage"
# s3 public media settings
PUBLIC_MEDIA_LOCATION = "media"
MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/{PUBLIC_MEDIA_LOCATION}/"
DEFAULT_FILE_STORAGE = "apps.base.storage_backends.MediaStorage"
# https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS
STATICFILES_DIRS = [str(APPS_DIR / "static")]
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]


# MEDIA
# ------------------------------------------------------------------------------

# https://docs.djangoproject.com/en/dev/ref/settings/#media-root
MEDIA_ROOT = str(APPS_DIR / "files")
# https://docs.djangoproject.com/en/dev/ref/settings/#media-url
MEDIA_URL = "/files/"


# TEMPLATES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#templates
TEMPLATES = [
    {
        # https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-TEMPLATES-BACKEND
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        # https://docs.djangoproject.com/en/dev/ref/settings/#dirs
        "DIRS": [str(APPS_DIR / "templates")],
        # https://docs.djangoproject.com/en/dev/ref/settings/#app-dirs
        "APP_DIRS": True,
        "OPTIONS": {
            # https://docs.djangoproject.com/en/dev/ref/settings/#template-context-processors
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
                "apps.base.context_processors.settings.git_env_settings",
            ],
        },
    }
]

# SECURITY
# ------------------------------------------------------------------------------

# Note: this is enriched in production.py
# https://docs.djangoproject.com/en/dev/ref/settings/#session-cookie-httponly
SESSION_COOKIE_HTTPONLY = True
# https://docs.djangoproject.com/en/dev/ref/settings/#csrf-cookie-httponly
CSRF_COOKIE_HTTPONLY = True
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-browser-xss-filter
SECURE_BROWSER_XSS_FILTER = True
# https://docs.djangoproject.com/en/dev/ref/settings/#x-frame-options
X_FRAME_OPTIONS = "DENY"

# ADMIN
# ------------------------------------------------------------------------------
# Django Admin URL.
ADMIN_URL = "admin/"

# CORS_ORIGIN_ALLOW_ALL = True   # If this is used then `CORS_ORIGIN_WHITELIST`
# will not have any effect
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_WHITELIST = env.list(
    "CORS_ORIGIN_WHITELIST",
    default=[
        "https://demo-compress-x.vercel.app",
        "http://demo-compress-x.vercel.app",
        # in order to be able to use local FE with dev servers
        "http://localhost:3000",
        "http://localhost:*",
        "http://127.0.0.1:3000",
    ],
)
CORS_ALLOWED_ORIGINS = env.list(
    "CORS_ORIGIN_WHITELIST",
    default=[
        "https://demo-compress-x.vercel.app",
        "http://demo-compress-x.vercel.app",
        # in order to be able to use local FE with dev servers
        "http://localhost:3000",
        "http://localhost:*",
        "http://127.0.0.1:3000",
    ],
)


# LOGGING
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#logging
# See https://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s"
        }
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        }
    },
    "root": {"level": "INFO", "handlers": ["console"]},
}

# Celery
# ------------------------------------------------------------------------------
if USE_TZ:
    # https://docs.celeryq.dev/en/stable/userguide/configuration.html#std:setting-timezone
    CELERY_TIMEZONE = TIME_ZONE

# https://docs.celeryq.dev/en/stable/userguide/configuration.html#std:setting-broker_url
CELERY_BROKER_URL = env("REDIS", default="redis://localhost:6379")
# https://docs.celeryq.dev/en/stable/userguide/configuration.html#std:setting-result_backend
CELERY_RESULT_BACKEND = CELERY_BROKER_URL
# https://docs.celeryq.dev/en/stable/userguide/configuration.html#std:setting-accept_content
CELERY_ACCEPT_CONTENT = ["json"]
# https://docs.celeryq.dev/en/stable/userguide/configuration.html#std:setting-task_serializer
CELERY_TASK_SERIALIZER = "json"
# https://docs.celeryq.dev/en/stable/userguide/configuration.html#std:setting-result_serializer
CELERY_RESULT_SERIALIZER = "json"
# https://docs.celeryq.dev/en/stable/userguide/configuration.html#task-time-limit
# TODO: set to whatever value is adequate in your circumstances
CELERY_TASK_TIME_LIMIT = 5 * 60
# https://docs.celeryq.dev/en/stable/userguide/configuration.html#task-soft-time-limit
# TODO: set to whatever value is adequate in your circumstances
CELERY_TASK_SOFT_TIME_LIMIT = 60
# CELERY
CACHE_MIDDLEWARE_ALIAS = "default"  # which cache alias to use
CACHE_MIDDLEWARE_KEY_PREFIX = ""

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient"},
        "KEY_PREFIX": "compressor_x_",
    }
}
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [(os.environ.get("CHANNELS_URLS", "redis://localhost:6379/0"))],
        },
    },
}

CELERY_DEFAULT_QUEUE = "default"
CELERY_DEFAULT_EXCHANGE = "normal"
CELERY_DEFAULT_ROUTING_KEY = "default"
CELERY_ACKS_LATE = True

# django-cors-headers - https://github.com/adamchainz/django-cors-headers#setup
# CORS_ORIGIN_ALLOW_ALL = True   # If this is used then `CORS_ORIGIN_WHITELIST`
# will not have any effect
CORS_ORIGIN_ALLOW_ALL = False
CORS_ALLOW_CREDENTIALS = True


# compressorx App
# -------------------------------------------------------------------------------
APP_CONFIG = env.str("CONFIG", "DEV")  # Used to name celery queues

# APP_DOMAIN is the domain name used by the frontend app connected to this backend.
# This is used to build email links.
APP_DOMAIN = env.str("APP_DOMAIN", default="http://localhost:4200/")

ENFORCE_EMAIL_VERIFICATION = env.bool("ENFORCE_EMAIL_VERIFICATION", True)

# Environment Information
ENVIRONMENT_COLOR = env.str("ENVIRONMENT_COLOR", default="#800080")
BUILD_INFO = env.str("BUILD_INFO", default="")


# GraphQL
GRAPHENE = {
    "SCHEMA": "compressorx.schemas.schema.schema",
    "MIDDLEWARE": (
        "graphene_django.debug.DjangoDebugMiddleware",
        "graphql_jwt.middleware.JSONWebTokenMiddleware",
    ),
}


ADMIN_MODEL_OVERRIDE = [
    {
        "app": "config",
        "position": 5,
        "labels": "Settings",
        "models": ["mail.EmailTemplate", "config.Config"],
    },
    {
        "app": "auth",
        "position": 1,
        "labels": "Authenticatie",
        "models": ["users.User", "auth.Group", "auth.Permission"],
    },
    {
        "app": "blog",
        "position": 4,
        "labels": "Content",
        "models": [
            "blog.Blog",
            "contact.Contact",
            "cookies.Cookie",
        ],
    },
    {"delete": True, "app": "sites"},
]


# Deepl
DEEPL_API_KEY = env.str("DEEPL_API_KEY", default="")


ASGI_APPLICATION = "compressorx.asgi.application"
