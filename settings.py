"""
Django settings for chandeleur project.
"""

import os
import sys


ADMINS = []

MANAGERS = ADMINS

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(os.path.abspath(os.path.expanduser(__file__)))
if not os.path.exists(os.path.join(BASE_DIR, 'logs')):
    os.makedirs(os.path.join(BASE_DIR, 'logs'))
TMP_DIR = os.path.join(BASE_DIR, 'temp')
if not os.path.exists(TMP_DIR):
    os.makedirs(TMP_DIR)
FILE_UPLOAD_TEMP_DIR = TMP_DIR
FILE_UPLOAD_PERMISSIONS = 0o644

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/
TEST_RUNNER = 'django.test.runner.DiscoverRunner'

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '&hjt)0xq_d4xr8v$o7nqkulf&n3g@hkt3&3wlw3vor=7@r$42$'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = '*'


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'chandeleur_app',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
]

ROOT_URLCONF = 'urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.static',
            ],

        },
    },
]

# WSGI_APPLICATION = 'chandeleur.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'fr-FR'

TIME_ZONE = 'Europe/Paris'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'

STATIC_DIR = os.path.join(BASE_DIR, 'static')  # this var is not used by Django
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    STATIC_DIR,
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    # 'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            '()': 'django.utils.log.ServerFormatter',
            'format': '%(asctime)s %(module)s %(levelname)s %(message)s',
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
        },
        'django_log_file': {
            'class': 'logging.FileHandler',
            'formatter': 'verbose',
            'filename': os.path.join(TMP_DIR, 'django.log'),
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
    'root': {
        'handlers': ['django_log_file'],
        'level': 'INFO',
        'propagate': False,
    },
}

# Auth config
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/login/'

# Settings override
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)  # to allow imports
try:
    from settings_override import *  # NOQA
except Exception as e:
    if 'No module named \'settings_override\'' not in str(e):
        import traceback
        traceback.print_exc()

if DEBUG:
    TEMPLATES[0]['OPTIONS']['debug'] = True
    TEMPLATES[0]['OPTIONS']['string_if_invalid'] = 'Invalid template string: "%s"'
    LOGGING['root']['level'] = 'DEBUG'
    LOGGING['root']['handlers'] = ['console']
    import warnings
    warnings.simplefilter('always', DeprecationWarning)
else:
    import logging
    logging.captureWarnings(False)
