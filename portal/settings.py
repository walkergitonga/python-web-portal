"""
Django settings for portal project.

Generated by 'django-admin startproject' using Django 1.8.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

from django.utils.translation import ugettext_lazy as _
from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS as TCP

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SITE_ID = 1

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'dx4pv9i)lulsom%b@=1$13x6z$844^8*toe4x9ivs#7$v3ccc2'

DJANGO_APP = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)

THIRD_PARTY_APPS = ()

LOCAL_APSS = (
    'apps.baseapp',
    'apps.profiles',
)

# Application definition
INSTALLED_APPS = DJANGO_APP + THIRD_PARTY_APPS + LOCAL_APSS

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.locale.LocaleMiddleware',
)

ROOT_URLCONF = 'portal.urls'

#Backend of login
AUTHENTICATION_BACKENDS = (
    'apps.baseapp.backends.EmailOrUsernameModelBackend',
    'django.contrib.auth.backends.ModelBackend',
)

#For login required
LOGIN_URL = "/"

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

'''Static files (CSS, JavaScript, Images)'''

STATIC_URL = '/static/'

#Root absolute for static files
STATICFILES_DIRS = (
    os.path.join(BASE_DIR,'static'),
)

#Static root for deployment with collectstatic
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

#Media files
MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

'''Internationalization'''

#Working Lenguage 
LANGUAGE_CODE = 'es'

#Lenguage support 
LANGUAGES = (
    ('en', _('English')),
    ('es', _('Spanish')),
)

#Path of the folder locale
LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

#Defined processor of contexto
TEMPLATE_CONTEXT_PROCESSORS = TCP + (
    "django.core.context_processors.i18n",
    "django.core.context_processors.request",
)

USE_I18N = True
USE_L10N = True

'''Time Zone'''

TIME_ZONE = 'America/Buenos_Aires'
USE_TZ = True

WSGI_APPLICATION = 'portal.wsgi.application'

# Import local settings
try:
    from settings_local import *
except Exception:
    pass



