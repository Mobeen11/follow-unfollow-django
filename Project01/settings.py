"""
Django settings for Project01 project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

#SETTINGS_PATH = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '(awkd)((s2yy@rtlmrs_f%@fy2wudb+q@a_e8a6q!*$7+h)4%o'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'follow_unfollow',
    'tinymce',

)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'Project01.urls'

WSGI_APPLICATION = 'Project01.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'df93k0jlp0crks',
        'USER': 'wqgxjmgettnmlt',
        'PASSWORD': 'Kmpy16WyV0UMl2MT-EmZ-vUUC6',
        'HOST': 'ec2-54-227-245-222.compute-1.amazonaws.com',
        'PORT': '5432',
    }
}

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)

#TEMPLATE_DIRS = (
#    os.path.join(BASE_DIR, 'follow_unfollow/template'),
#)

#TEMPLATES = [
#    {
#        'BACKEND': 'django.template.backends.django.DjangoTemplates',
#        'DIRS': [os.path.join(BASE_DIR, 'templates')],
#        'APP_DIRS': True,
#        'OPTIONS': {
#            'context_processors': [
#                'django.template.context_processors.debug',
#                'django.template.context_processors.request',
#                'django.contrib.auth.context_processors.auth',
#                'django.contrib.messages.context_processors.messages',
#            ],
#        },
#    },
#]


# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), "static")
print(STATIC_ROOT)

# error in static files
STATICFILES_DIR = (
    os.path.join(os.path.dirname(BASE_DIR), "static")
    # '/Users/Admin/Desktop/djangoProjects/follow-prog-2/static'
)
#

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR),"media")


import dj_database_url
DATABASES['default'] = dj_database_url.config()

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

ALLOWED_HOSTS = ['*']

DEBUG = True

try:
    from .local_settings import *
except ImportError:
    pass
