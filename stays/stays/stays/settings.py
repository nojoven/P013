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

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/


ALLOWED_HOSTS = ["*", "localhost", "0.0.0.0", "127.0.0.1"]


# Application definition

INSTALLED_APPS = [
    # APM
    "django.contrib.sites",
    "djapm.apm.apps.ApmConfig",
    "django.contrib.admin",
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
    "widget_tweaks",
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
    # Iommi: these three are optional, but highly recommended!
    'iommi.live_edit.Middleware',
    'iommi.sql_trace.Middleware',
    'iommi.profiling.Middleware',
    # Iommi : this one is required
    'iommi.middleware',
    # Add the account middleware:
    #"allauth.account.middleware.AccountMiddleware",

]

ROOT_URLCONF = "stays.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                # "django.core.context_processors.request"
            ],
        },
    },
]

WSGI_APPLICATION = "stays.wsgi.application"


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
    # "test": {
    #     "ENGINE": confs.get("ENGINE"),
    #     "NAME": confs.get("NAME"),
    #     "USER": confs.get("USER"),
    #     "PASSWORD": confs.get("PASSWORD"),
    #     "HOST": confs.get("HOST"),
    #     "PORT": confs.get("PORT"),
    #     'OPTIONS': {'sslmode': 'require'}
    # }
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
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_DIRS =  (os.path.join(BASE_DIR, "static"),)


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

# HERE STARTS DYNACONF EXTENSION LOAD (Keep at the very bottom of settings.py)
# Read more at https://www.dynaconf.com/django/
import dynaconf  # noqa
settings = dynaconf.DjangoDynaconf(__name__)  # noqa
# HERE ENDS DYNACONF EXTENSION LOAD (No more code below this line)
