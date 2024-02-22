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
# import platform
# from machina import MACHINA_MAIN_TEMPLATE_DIR

from icecream import install as icinstall, ic
icinstall()

ic("Thanks to https://simplemaps.com/data/world-cities")
ic("Image by Timur Kozmenko from Pixabay")

import sentry_sdk


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
# raise ValueError(settings.SECRET_KEY)
SECRET_KEY = confs.get("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = confs.get("DEBUG") # settings.DYNACONF_DEBUG
TEMPLATE_DEBUG = confs.get("TEMPLATE_DEBUG")

if DEBUG is True:
    # Comment the one you don't need

    import stackprinter
    stackprinter.set_excepthook(style='darkbg2')

    # from frosch import hook
    # hook()

    # os.environ['BETTER_EXCEPTIONS'] = "1"


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

ALLOWED_HOSTS = ["*", "localhost", "0.0.0.0", "127.0.0.1"]


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django.db.backends': {
            # 'level': 'DEBUG',
            'level': 'INFO',
        },
    },
}


# Application definition

INSTALLED_APPS = [
    # APM
    "django.contrib.sites",
    "django.contrib.admin",
    "daphne",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "defender",
    "rest_framework",
    "users",
    "core",
    "cities_light",
    "locations",
    "watchman",
    "django_select2",
    # "iommi",
    # "allauth_ui",
    # "allauth",
    # "allauth.account",
    # "allauth.socialaccount",
    # "allauth.socialaccount.providers.github",
    # "allauth.socialaccount.providers.reddit",
    "django_countries",
    "django_htmx",
    # "formset",
    # "django_filters",
    # "extra_views",

    # Quill text editor
    # 'django_quill',

    # Pagination
    "django_cool_paginator",
    # "el_pagination",

    # Machina dependencies:
    # 'mptt',
    # 'haystack',
    # 'widget_tweaks',

    # Machina apps:
    # 'machina',
    # 'machina.apps.forum',
    # 'machina.apps.forum_conversation',
    # 'machina.apps.forum_conversation.forum_attachments',
    # 'machina.apps.forum_conversation.forum_polls',
    # 'machina.apps.forum_feeds',
    # 'machina.apps.forum_moderation',
    # 'machina.apps.forum_search',
    # 'machina.apps.forum_tracking',
    # 'machina.apps.forum_member',
    # 'machina.apps.forum_permission',

    # Django-Ninja
    "ninja_extra",
    # Django Q2
    "django_q",
    # Font-Awesome
    "fontawesomefree",

    # Thumbnails
    'sorl.thumbnail',

    # Audiofield
    # "audiofield",

    # Easy Maps
    # "easy_maps",

    # tinymce
    "tinymce",

    # friendship
    "friendship",
    "pagination",
    # sweetify
    'sweetify',
]


# Sweet Alert choices: 'sweetalert', 'sweetalert2' - default is 'sweetalert2'
SWEETIFY_SWEETALERT_LIBRARY = 'sweetalert2'


CITIES_LIGHT_TRANSLATION_LANGUAGES = ['fr', 'en']
# CITIES_LIGHT_INCLUDE_COUNTRIES = ['FR']
# CITIES_LIGHT_INCLUDE_CITY_TYPES = ['PPL', 'PPLA', 'PPLA2', 'PPLA3', 'PPLA4', 'PPLC', 'PPLF', 'PPLG', 'PPLL', 'PPLR', 'PPLS', 'STLMT',]


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    'django.middleware.cache.UpdateCacheMiddleware',
    "django.middleware.common.CommonMiddleware",
    'django.middleware.cache.FetchFromCacheMiddleware',
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django_htmx.middleware.HtmxMiddleware",
    # Iommi: these three are optional, but highly recommended!
    'iommi.live_edit.Middleware',
    'iommi.sql_trace.Middleware',
    'iommi.profiling.Middleware',
    # Iommi : this one is required
    'iommi.middleware',
    # better_exceptions
    # "better_exceptions.integrations.django.BetterExceptionsMiddleware",
    # Add the account middleware:
    # "allauth.account.middleware.AccountMiddleware",
    # Machina
    # 'machina.apps.forum_permission.middleware.ForumPermissionMiddleware',
    # Current user
    # 'django_currentuser.middleware.ThreadLocalUserMiddleware',
    # Defender
    'defender.middleware.FailedLoginMiddleware',
    # Auto Logout
    "django_auto_logout.middleware.auto_logout",
    # http error handler
    "stays.utils.errors_helpers.ErrorHandlerMiddleware",
    'pagination.middleware.PaginationMiddleware',
]

ROOT_URLCONF = "stays.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(BASE_DIR, "templates"),
            #  MACHINA_MAIN_TEMPLATE_DIR,
            ],
        # "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                #"django.core.context_processors.request"
                # Machina
                # 'machina.core.context_processors.metadata',
                # auto logout
                'django_auto_logout.context_processors.auto_logout_client',
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
        "NAME": confs.get("NAME"),
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
    # 'machina_attachments': {
    #     'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
    #     'LOCATION': confs.get("MACHINA_ATTACHMENT_CACHE_LOCATION") if platform.system() == 'Windows' else '/tmp',
    # },
}

# SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "select2"

# # Tell select2 which cache configuration to use:
# SELECT2_CACHE_BACKEND = "select2"


THROTTLE_ZONES = {
    'default': {
        'VARY': 'throttle.zones.RemoteIP',
        'ALGORITHM': 'fixed-bucket',  # Default if not defined.
        'BUCKET_INTERVAL': 5 * 60,  # Number of seconds to enforce limit.
        'BUCKET_CAPACITY': 20  # Maximum number of requests allowed within BUCKET_INTERVAL
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


# HAYSTACK_CONNECTIONS = {
#     'default': {
#         'ENGINE': 'haystack.backends.simple_backend.SimpleEngine',
#     },
# }


# python manage.py cleanup_django_defender to unlock
DEFENDER_LOGIN_FAILURE_LIMIT = 20

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

# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# AUTHENTICATION_BACKENDS = ['users.backends.EmailBackend']
AUTHENTICATION_BACKENDS = [
    'users.backends.EmailBackend',  # custom backend
    # 'django.contrib.auth.backends.ModelBackend',  # default backend
    # 'allauth.account.auth_backends.AuthenticationBackend',
]

FRIENDSHIP_CONTEXT_OBJECT_NAME = 'profile'
FRIENDSHIP_CONTEXT_OBJECT_LIST_NAME = 'profiles'
FRIENDSHIP_MANAGER_FRIENDSHIP_REQUEST_SELECT_RELATED_STRATEGY = 'select_related'  # ('select_related', 'prefetch_related', 'none')

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

AUTO_LOGOUT = {
    'IDLE_TIME': 6000,
    'SESSION_TIME': 36000,
    'REDIRECT_TO_LOGIN_IMMEDIATELY': True,
    'MESSAGE': 'The session has expired. Please login again to continue.'
    }


# EASY_MAPS_GOOGLE_KEY = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ___0123456789'
# EASY_MAPS_CENTER = (-41.3, 32)
# EASY_MAPS_LANGUAGE = 'fr'

TINYMCE_JS_URL = f"https://cdn.tiny.cloud/1/{confs.get('TINY_MCE_API_KEY')}/tinymce/6/tinymce.min.js"
TINYMCE_COMPRESSOR = confs.get("TINYMCE_COMPRESSOR", False)

PORCUPINE_ACCESSKEY = confs.get("PORCUPINE_ACCESSKEY")
OPENAI_API_KEY = confs.get("OPENAI_API_KEY")


COUNTRIES_FIRST = ['FR', 'US', 'GB']
COUNTRIES_FIRST_SORT = True

MAPBOX_TOKEN = confs.get("MAPBOX_TOKEN")
NINJAS_API_KEY = confs.get("NINJAS_API_KEY")


UNDETECTABLE_AI_API_KEY = confs.get("UNDETECTABLE_AI_API_KEY")


# settings.py
X_FRAME_OPTIONS = 'SAMEORIGIN'

EMAIL_BACKEND = confs.get("EMAIL_BACKEND")
# Hostname of your email provider
EMAIL_HOST = confs.get("EMAIL_HOST")
# port of your email provider
EMAIL_PORT = confs.get("EMAIL_PORT")
EMAIL_USE_TLS = confs.get("EMAIL_USE_TLS")
# your email account
EMAIL_HOST_USER = confs.get("EMAIL_HOST_USER")
# your email password
EMAIL_HOST_PASSWORD = confs.get("EMAIL_HOST_PASSWORD")

# Mailgun Authorized email
DEFAULT_EMAIL_DESTINATION = confs.get("DEFAULT_EMAIL_DESTINATION")
ADMIN_EMAIL = confs.get("ADMIN_EMAIL")

MAILGUN_API_KEY = confs.get("MAILGUN_API_KEY")
MAILGUN_DOMAIN_NAME = confs.get("MAILGUN_DOMAIN_NAME")

HANDLER400 = 'stays.urls.handler400'
HANDLER401 = 'stays.urls.handler401'
HANDLER403 = 'stays.urls.handler403'
HANDLER404 = 'stays.urls.handler404'
HANDLER410 = 'stays.urls.handler410'
HANDLER418 = 'stays.urls.handler418'
HANDLER429 = 'stays.urls.handler429'
HANDLER500 = 'stays.urls.handler500'
HANDLER503 = 'stays.urls.handler503'
HANDLER504 = 'stays.urls.handler504'

SENTRY_DSN_PROTOCOL = confs.get("SENTRY_DSN_PROTOCOL", "")
SENTRY_DSN_START = confs.get("SENTRY_DSN_START", "")
SENTRY_DSN_END = confs.get("SENTRY_DSN_END", "")
dsn = f"{SENTRY_DSN_PROTOCOL}://{SENTRY_DSN_START}/{SENTRY_DSN_END}"
if dsn and len(dsn) > 20:
    sentry_sdk.init(
        dsn=dsn,
        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        traces_sample_rate=1.0,
        # Set profiles_sample_rate to 1.0 to profile 100%
        # of sampled transactions.
        # We recommend adjusting this value in production.
        profiles_sample_rate=1.0,
    )


Q_CLUSTER = {
    'name': 'stays',  # Name of your project
    'workers': 3 if DEBUG is True else 4,  # Number of workers to use
    'orm': 'default',  # The ORM to use
    'recycle': 80,  # Number of tasks a worker will perform before being recycled
    'timeout': 90,  # Timeout before a task is considered as blocked
    # 'compress': True,  # If True, tasks will be compressed before being queued
    'save_limit': 10,  # Maximum number of successful tasks to keep in the database
    'queue_limit': 50,  # Maximum number of tasks to queue
    'cpu_affinity': 1,  # Number of CPU cores to use per worker
    'label': 'Django_Q2',  # Label for the cluster
    'retry': 110,
    'redis': {  # Redis configuration
        'host': '127.0.0.1',  # Redis host address
        'port': 6379,  # Redis host port
        'db': 3,  # Redis database to use
    }
    # ,
    # 'ALT_CLUSTERS': {  # Alternative clusters for different categories of tasks
    #     'long': {  # Configuration for long-running tasks
    #         'timeout': 3000,  # Timeout before a task is considered as blocked
    #         'retry': 3600,  # Time to wait before retrying a blocked task
    #         'max_attempts': 2,  # Maximum number of attempts for a task
    #     },
    #     'short': {  # Configuration for short-running tasks
    #         'timeout': 10,  # Timeout before a task is considered as blocked
    #         'max_attempts': 1,  # Maximum number of attempts for a task
    #     },
    # }
}

# HERE STARTS DYNACONF EXTENSION LOAD (Keep at the very bottom of settings.py)
# Read more at https://www.dynaconf.com/django/
# import dynaconf  # noqa
# settings = dynaconf.DjangoDynaconf(__name__)  # noqa
# HERE ENDS DYNACONF EXTENSION LOAD (No more code below this line)
