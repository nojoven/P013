"""
Django settings for stays project.

Generated by 'django-admin startproject' using Django 4.2.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

# Add these at the top of your settings.py
import json
import os
from pathlib import Path
from os import getenv
from dotenv import load_dotenv
import sentry_sdk

from icecream import install as icinstall, ic
icinstall()

ic("Thanks to https://simplemaps.com/data/world-cities")
ic("Image by Timur Kozmenko from Pixabay")



# if "confs.json" in os.listdir(Path(__file__).absolute().parent):
#     vars_path = Path(__file__).absolute().parent / "confs.json"
#     with open(vars_path) as file:
#         confs = json.loads(file.read())

# else:
load_dotenv()




# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
# raise ValueError(settings.SECRET_KEY)
SECRET_KEY = getenv("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = getenv("DEBUG")
TEMPLATE_DEBUG = getenv("TEMPLATE_DEBUG")

# if DEBUG is True:
#     # Comment the one you don't need

#     import stackprinter
#     stackprinter.set_excepthook(style='darkbg2')


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
    # "rest_framework",
    "users",
    "core",
    "cities_light",
    "locations",
    # "silk",
    # "allauth_ui",
    # "allauth",
    # "allauth.account",
    # "allauth.socialaccount",
    # "allauth.socialaccount.providers.reddit",
    "django_countries",
    "django_htmx",

    # Pagination
    "django_cool_paginator",
    
    # Django-Ninja
    "ninja_extra",
    # Django Q2
    "django_q",
    # Font-Awesome
    "fontawesomefree",

    # Thumbnails
    # 'sorl.thumbnail',

    # tinymce
    # "tinymce",

    # friendship
    "friendship",
    "pagination",
    # sweetify
    # 'sweetify',
]


# Sweet Alert choices: 'sweetalert', 'sweetalert2' - default is 'sweetalert2'
# SWEETIFY_SWEETALERT_LIBRARY = 'sweetalert2'


CITIES_LIGHT_TRANSLATION_LANGUAGES = ['fr', 'en']


MIDDLEWARE = [
    # 'silk.middleware.SilkyMiddleware',
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.middleware.common.CommonMiddleware",
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django_htmx.middleware.HtmxMiddleware",
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
                'django_auto_logout.context_processors.auto_logout_client',
            ],
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ]
        },
    },
]

# WSGI_APPLICATION = "stays.wsgi.application"
ASGI_APPLICATION = "stays.asgi.application"
SILKY_PYTHON_PROFILER = True

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases


# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': getenv('PGDATABASE'),
#         'USER': getenv('PGUSER'),
#         'PASSWORD': getenv('PGPASSWORD'),
#         'HOST': getenv('PGHOST'),
#         'PORT': getenv('PGPORT'),
#         'OPTIONS': {
#             'sslmode': 'require',
#         },
#         'DISABLE_SERVER_SIDE_CURSORS': True,
#     }
# }
DATABASES = {
    'default': {
        'ENGINE': getenv('ENGINE'),
        'NAME': getenv('NAME'),
        'USER': getenv('USER'),
        'PASSWORD': getenv('PASSWORD'),
        'HOST': getenv('HOST'),
        'PORT': getenv('DBPORT'),
        # 'OPTIONS': {
        #     'sslmode': 'require',
        # },
        'DISABLE_SERVER_SIDE_CURSORS': True,
    }
}

CACHES = {
    # … default cache config and others
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": getenv("REDIS_URL"),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
    # ,
    # "select2": {
    #     "BACKEND": "django_redis.cache.RedisCache",
    #     "LOCATION": "redis://127.0.0.1:6379/2",
    #     "OPTIONS": {
    #         "CLIENT_CLASS": "django_redis.client.DefaultClient",
    #     }
    # }
}

# SESSION_ENGINE = "django.contrib.sessions.backends.cache"
# SESSION_CACHE_ALIAS = "select2"

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

DEFENDER_REDIS_NAME = 'default'
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

COUNTRIES_FIRST = ['FR', 'US', 'GB']
COUNTRIES_FIRST_SORT = True

NINJAS_API_KEY = getenv("NINJAS_API_KEY")

# settings.py
X_FRAME_OPTIONS = 'SAMEORIGIN'

# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_BACKEND = getenv("EMAIL_BACKEND")
# Hostname of your email provider
EMAIL_HOST = getenv("EMAIL_HOST")
# port of your email provider
EMAIL_PORT = getenv("EMAIL_PORT")
EMAIL_USE_TLS = getenv("EMAIL_USE_TLS")
# your email account
EMAIL_HOST_USER = getenv("EMAIL_HOST_USER")
# your email password
EMAIL_HOST_PASSWORD = getenv("EMAIL_HOST_PASSWORD")

# Mailgun Authorized email
DEFAULT_EMAIL_DESTINATION = getenv("DEFAULT_EMAIL_DESTINATION")

ADMIN_EMAIL = getenv("ADMIN_EMAIL")

MAILGUN_API_KEY = getenv("MAILGUN_API_KEY")
MAILGUN_DOMAIN_NAME = getenv("MAILGUN_DOMAIN_NAME")

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

SENTRY_DSN_PROTOCOL = getenv("SENTRY_DSN_PROTOCOL")
SENTRY_DSN_START = getenv("SENTRY_DSN_START")
SENTRY_DSN_END = getenv("SENTRY_DSN_END")

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
}
