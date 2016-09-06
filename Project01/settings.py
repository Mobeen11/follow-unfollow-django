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
DEBUG = False

TEMPLATE_DEBUG = False

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
    'facebook_image',
    'tinymce',

    'social.apps.django_app.default',
)

# MIDDLEWARE_CLASSES = (
#     'django.contrib.sessions.middleware.SessionMiddleware',
#     'django.middleware.common.CommonMiddleware',
#     'django.middleware.csrf.CsrfViewMiddleware',
#     'django.contrib.auth.middleware.AuthenticationMiddleware',
#     'django.contrib.messages.middleware.MessageMiddleware',
#     'django.middleware.clickjacking.XFrameOptionsMiddleware',
# )
MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'Project01.urls'

WSGI_APPLICATION = 'Project01.wsgi.application'

AUTHENTICATION_BACKENDS = (

    'social.backends.facebook.FacebookOAuth2',


    'social.backends.instagram.InstagramOAuth2',


    'social.backends.twitter.TwitterOAuth',


    'social.backends.username.UsernameAuth',

    'django.contrib.auth.backends.ModelBackend',
)

TEMPLATES_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.auth.context_processors.messages",

    # py social auth
    'socail.apps.django_app.context_processors.backends',
    'socail.apps.django_app.context_processors.login_redirect',
)

#pipeline settings
SOCIAL_AUTH_PIPELINE = (
    'social.pipeline.social_auth.social_details',
    'social.pipeline.social_auth.social_uid',
    'social.pipeline.social_auth.auth_allowed',
    'social.pipeline.social_auth.social_user',
    'social.pipeline.user.get_username',
    'social.pipeline.user.create_user',
    'social.pipeline.social_auth.associate_user',
    'social.pipeline.social_auth.load_extra_data',

    # 'social.pipeline.user.user_details',
    #
    # 'social.pipeline.mail.mail_validation',
    # # Associates the current social details with another user account with
    # # a similar email address. Disabled by default.
    # 'social.pipeline.social_auth.associate_by_email',
    # # Create the record that associated the social account with this user.
    # 'social.pipeline.social_auth.associate_user',
    # # Populate the extra_data field in the social record with the values
    # # specified by settings (and the default ones like access_token, etc).
    # 'social.pipeline.social_auth.load_extra_data',

    'facebook_image.pipeline.save_profile',
)


#pipeline disconnect settings
SOCIAL_AUTH_DISCONNECT_PIPELINE = (
    # Verifies that the social association can be disconnected from the current
    # user (ensure that the user login mechanism is not compromised by this
    # disconnection).
    'social.pipeline.disconnect.allowed_to_disconnect',

    # Collects the social associations to disconnect.
    'social.pipeline.disconnect.get_entries',

    # Revoke any access_token when possible.
    'social.pipeline.disconnect.revoke_tokens',

    # Removes the social associations.
    'social.pipeline.disconnect.disconnect',
)


#facebook
SOCIAL_AUTH_FACEBOOK_KEY = '185642748516816'
SOCIAL_AUTH_FACEBOOK_SECRET = '39aa209f4c058aec0493027bfcfef904'
# SOCIAL_AUTH_FACEBOOK_SCOPE = ['email', 'public_profile']    #what we want to grab from the user
SOCIAL_AUTH_FACEBOOK_SCOPE = [
    'email',
    'user_friends',
    'publish_actions',
    'user_posts',
    'manage_pages',
    'publish_pages',
]
SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PRAMS = {'locale':'ru_RU'}

#instagram
SOCIAL_AUTH_INSTAGRAM_KEY = 'f1e482c282914b02b36565e7923f1ba9'
SOCIAL_AUTH_INSTAGRAM_SECRET = '46456179a3544ad0bbdb4d0d9d1249df'
SOCIAL_AUTH_INSTAGRAM_AUTH_EXTRA_ARGUMENTS = {'scope':'likes comments relationships'}

#twitter
SOCIAL_AUTH_TWITTER_KEY = 'HISKYRsVumzfw29OsuO6uemJY'
SOCIAL_AUTH_TWITTER_SECRET = '2sUI8VMPSaYpma1wQeQn6GSKP9o08uQAbtYQH5JAhIufWPT4Xv'


STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)
# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.postgresql_psycopg2',
    #     'NAME': 'df93k0jlp0crks',
    #     'USER': 'wqgxjmgettnmlt',
    #     'PASSWORD': 'Kmpy16WyV0UMl2MT-EmZ-vUUC6',
    #     'HOST': 'ec2-54-227-245-222.compute-1.amazonaws.com',
    #     'PORT': '5432',
    # }

    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'd7auv1isafvk6r',
        'USER': 'cenufnduhpgdwu',
        'PASSWORD': 'Yf9WbiSNM5GokvveBgbtuG5hs6',
        'HOST': 'ec2-50-19-227-171.compute-1.amazonaws.com',
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
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) #+ '/..'

STATIC_URL = '/static/'

ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'
STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), "static")
# STATIC_ROOT = "E:/Git Parent/follow/follow-prog-2/static"


# error in static files
STATICFILES_DIR = (
    os.path.join(BASE_DIR, "static"),
    # '/Users/Admin/Desktop/djangoProjects/follow-prog-2/static'

)
# STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), "static")

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR),"media")

# MEDIA_ROOT = 'follow/follow-prog-2/media'

SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/test/'
LOGIN_ERROR_URL = '/login-error/'

# import dj_database_url
# DATABASES['default'] = dj_database_url.config()

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

ALLOWED_HOSTS = ['*']

#
#
# try:
#     from .local_settings import *
# except ImportError:
#     pass
