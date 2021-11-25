"""
Django settings for adjsite project.

Generated by 'django-admin startproject' using Django 3.2.
"""
import os
import environ
from pathlib import Path


env = environ.Env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
# BASE_DIR = Path(__file__).resolve().parent.parent

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT_DIR = environ.Path(__file__) - 3

# reading .env file
# environ.Env.read_env(os.path.join(BASE_DIR, '.env'))
environ.Env.read_env(os.path.join(ROOT_DIR, 'adjsite.env'))
APPS_DIR = ROOT_DIR.path('survay')


# Эта часть добавлена из CookieCutter Django и гарантирует отсутствие ошибок при запуске локального сервера/миграциях
# READ_DOT_ENV_FILE = env.bool('DJANGO_READ_DOT_ENV_FILE', default=False)
#
# if READ_DOT_ENV_FILE:
#     env_file = str(ROOT_DIR.path('.env'))
#     print('Loading : {}'.format(env_file))
#     env.read_env(env_file)
#     print('The .env file has been loaded. See basesettings.py for more information')


# SECRET_KEY = env("SECRET_KEY")

DEBUG = env.bool('DJANGO_DEBUG', False)
# DEBUG = True
# ALLOWED_HOSTS = []


# Application definition

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    'django_tables2',
    'django_filters',
    'bootstrap3',
]

LOCAL_APPS = [
    'survay.apps.SurvayConfig',
    'adjauth',
]

DEVEL_APPS = []

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS + DEVEL_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'adjsite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'adjsite.wsgi.application'


# Database
DATABASES = {
    'default': env.db()
    # 'default': {
    #     'ENGINE': 'django.db.backends.postgresql_psycopg2',
    #     'NAME': env("DATABASE_NAME"),
    #     'USER': env("DATABASE_USER"),
    #     'PASSWORD': env("DATABASE_PASSWORD"),
    #     'HOST': env("DATABASE_HOST"),
    #     'PORT': env("DATABASE_PORT"),
    # }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 5,
        }
    },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    # },
]


# Internationalization

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Геолокатор

API_URL = env("API_URL")
    

API_KEY_GEO = env("API_KEY_GEO")
   

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/
# The absolute path to the directory where collectstatic will collect static files for deployment.

STATIC_ROOT = os.path.join(ROOT_DIR, 'staticfiles')

STATIC_URL = 'survay/static/'

# STATICFILES_DIRS = [BASE_DIR / "static", ]

# STATIC_ROOT = str(ROOT_DIR('staticfiles'))

STATICFILES_DIRS = (
    str(APPS_DIR.path('static')),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)
WHITENOISE_USE_FINDERS = True

INTERNAL_IPS = []

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_REDIRECT_URL = "main_page"

LOGOUT_REDIRECT_URL = "index_page"

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

EMAIL_HOST = 'localhost'

EMAIL_PORT = 1025

EMAIL_HOST_USER = 'kgb1-akuzmicheva@mail.ru'

EMAIL_HOST_PASSWORD = ''
