"""
Django settings for stays project.

Generated by 'django-admin startproject' using Django 4.2.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

import json
import os
from pathlib import Path
import platform
from machina import MACHINA_MAIN_TEMPLATE_DIR

print("Thanks to https://simplemaps.com/data/world-cities")
print("Image by Timur Kozmenko from Pixabay")


if "confs.json" in os.listdir(Path(__file__).absolute().parent):
    vars_path = Path(__file__).absolute().parent / "confs.json"
    with open(vars_path) as file:
        confs = json.loads(file.read())

else:
    confs = {
        "DEBUG": True if os.environ.get("DEBUG") in ("True", "true") else False,
        "ENGINE": os.environ.get("ENGINE"),
        "HOST": os.environ.get("HOST"),
        "NAME": os.environ.get("NAME"),
        "PASSWORD": os.environ.get("PASSWORD"),
        "PORT": int(os.environ.get("PORT")),
        "SECRET_KEY": os.environ.get("SECRET_KEY"),
        "TEMPLATE_DEBUG": os.environ.get(""),
        "USER": os.environ.get("USER"),
    }

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
 
# SECURITY WARNING: keep the secret key used in production secret!
#raise ValueError(settings.SECRET_KEY)
SECRET_KEY = confs.get("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = confs.get("DEBUG") # settings.DYNACONF_DEBUG
TEMPLATE_DEBUG = confs.get("TEMPLATE_DEBUG")

if DEBUG is True:
    from frosch import hook
    hook()

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/


ALLOWED_HOSTS = ["*", "localhost", "0.0.0.0", "127.0.0.1"]


# Application definition

INSTALLED_APPS = [
    # APM
    "django.contrib.sites",
    "djapm.apm.apps.ApmConfig",
    "django.contrib.admin",
    "daphne",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "users",
    "core",
    "cities_light",
    "locations",
    "watchman",
    "django_select2",
    "iommi",
    "allauth_ui",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.openid",
    "allauth.socialaccount.providers.reddit",
    "allauth.socialaccount.providers.pinterest",
    "allauth.socialaccount.providers.apple",
    "allauth.socialaccount.providers.edx",
    #"allauth.socialaccount.providers.23andme",
    "allauth.socialaccount.providers.eventbrite",
    "allauth.socialaccount.providers.mediawiki",
    "allauth.socialaccount.providers.kakao",
    "allauth.socialaccount.providers.exist",
    "allauth.socialaccount.providers.eveonline",
    "allauth.socialaccount.providers.gumroad",
    "allauth.socialaccount.providers.baidu",
    #"allauth.socialaccount.providers.500px",
    "allauth.socialaccount.providers.draugiem",
    "allauth.socialaccount.providers.doximity",
    "allauth.socialaccount.providers.daum",
    "allauth.socialaccount.providers.pocket",
    "allauth.socialaccount.providers.strava",
    "allauth.socialaccount.providers.weixin",
    "allauth.socialaccount.providers.weibo",
    "allauth.socialaccount.providers.steam",
    "allauth.socialaccount.providers.wahoo",
    "allauth.socialaccount.providers.naver",
    "allauth.socialaccount.providers.soundcloud",
    "allauth.socialaccount.providers.trainingpeaks",
    #"widget_tweaks",
    "django_countries",
    "django_htmx",
    "formset",
    "django_tables2",
    "django_filters",
    #"extra_views",

    # Quill text editor
    'django_quill',

    # Pagination
    "django_cool_paginator",
    "el_pagination",

    # Machina dependencies:
    'mptt',
    'haystack',
    'widget_tweaks',

    # Machina apps:
    'machina',
    'machina.apps.forum',
    'machina.apps.forum_conversation',
    'machina.apps.forum_conversation.forum_attachments',
    'machina.apps.forum_conversation.forum_polls',
    'machina.apps.forum_feeds',
    'machina.apps.forum_moderation',
    'machina.apps.forum_search',
    'machina.apps.forum_tracking',
    'machina.apps.forum_member',
    'machina.apps.forum_permission',

    # Django-Ninja
    "ninja_extra",

]

CITIES_LIGHT_TRANSLATION_LANGUAGES = ['fr', 'en']
# CITIES_LIGHT_INCLUDE_COUNTRIES = ['FR']
# CITIES_LIGHT_INCLUDE_CITY_TYPES = ['PPL', 'PPLA', 'PPLA2', 'PPLA3', 'PPLA4', 'PPLC', 'PPLF', 'PPLG', 'PPLL', 'PPLR', 'PPLS', 'STLMT',]


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "djapm.apm.middlewares.ApmMetricsMiddleware",
    "djapm.apm.middlewares.ErrorTraceMiddleware",
    "django_htmx.middleware.HtmxMiddleware",
    # Iommi: these three are optional, but highly recommended!
    'iommi.live_edit.Middleware',
    'iommi.sql_trace.Middleware',
    'iommi.profiling.Middleware',
    # Iommi : this one is required
    'iommi.middleware',
    # Add the account middleware:
    #"allauth.account.middleware.AccountMiddleware",
    # Machina
    'machina.apps.forum_permission.middleware.ForumPermissionMiddleware',
]

ROOT_URLCONF = "stays.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates"), MACHINA_MAIN_TEMPLATE_DIR,],
        # "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                # "django.core.context_processors.request"
                # Machina
                'machina.core.context_processors.metadata',
            ],
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ]
        },
    },
]

WSGI_APPLICATION = "stays.wsgi.application"
ASGI_APPLICATION = "stays.asgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": confs.get("ENGINE"),
        "NAME":confs.get("NAME"),
        "USER": confs.get("USER"),
        "PASSWORD": confs.get("PASSWORD"),
        "HOST": confs.get("HOST"),
        "PORT": confs.get("PORT"),
        # 'OPTIONS': {'sslmode': 'require'}
    },
}


CACHES = {
    # … default cache config and others
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    "select2": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/2",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    'machina_attachments': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': '%USERPROFILE%\AppData\Local\Temp' if platform.system() == 'Windows' else '/tmp',
    },
}

# SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "select2"

# # Tell select2 which cache configuration to use:
# SELECT2_CACHE_BACKEND = "select2"


THROTTLE_ZONES = {
    'default': {
        'VARY':'throttle.zones.RemoteIP',
        'ALGORITHM': 'fixed-bucket',  # Default if not defined.
        'BUCKET_INTERVAL':15 * 60,  # Number of seconds to enforce limit.
        'BUCKET_CAPACITY':50,  # Maximum number of requests allowed within BUCKET_INTERVAL
    },
}

# Where to store request counts.
THROTTLE_BACKEND = 'throttle.backends.cache.CacheBackend'

# Optional if Redis backend is chosen ('throttle.backends.redispy.RedisBackend')
THROTTLE_REDIS_HOST = 'localhost'
THROTTLE_REDIS_PORT = 6379
THROTTLE_REDIS_DB = 0
THROTTLE_REDIS_AUTH = 'pass'

# Normally, throttling is disabled when DEBUG=True. Use this to force it to enabled.
THROTTLE_ENABLED = True


HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.simple_backend.SimpleEngine',
    },
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "/static/"
COUNTRIES_FLAG_URL = "flags/{code}.png"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"),)
GEOIP_PATH = os.path.join(BASE_DIR, "geoip")


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

MEDIA_AUTO_FIELD = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

AUTH_USER_MODEL = "users.Profile"

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
#AUTHENTICATION_BACKENDS = ['users.backends.EmailBackend']
AUTHENTICATION_BACKENDS = [
    'users.backends.EmailBackend',  # custom backend
    #'django.contrib.auth.backends.ModelBackend',  # default backend
    'allauth.account.auth_backends.AuthenticationBackend',
]


LOGIN_URL = "users:login"
LOGIN_REDIRECT_URL = "users:account"
LOGOUT_REDIRECT_URL = "core:home"

SITE_ID = 1

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE = False
ACCOUNT_SESSION_REMEMBER = True
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_UNIQUE_EMAIL = True

COOL_PAGINATOR_ELASTIC = True

# HERE STARTS DYNACONF EXTENSION LOAD (Keep at the very bottom of settings.py)
# Read more at https://www.dynaconf.com/django/
import dynaconf  # noqa
settings = dynaconf.DjangoDynaconf(__name__)  # noqa
# HERE ENDS DYNACONF EXTENSION LOAD (No more code below this line)
