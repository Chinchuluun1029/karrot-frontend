"""
Django settings for karrot.

Generated by 'django-admin startproject' using Django 1.8.4.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Application definition

INSTALLED_APPS = (
    # core Django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    'django.contrib.messages',
    'django.contrib.postgres',

    # Application
    'foodsaving',
    'foodsaving.userauth',
    'foodsaving.base',
    'foodsaving.subscriptions.SubscriptionsConfig',
    'foodsaving.users.UsersConfig',
    'foodsaving.conversations',
    'foodsaving.history.HistoryConfig',
    'foodsaving.groups.GroupsConfig',
    'foodsaving.stores.StoresConfig',
    'foodsaving.pickups.PickupsConfig',
    'foodsaving.invitations.InvitationsConfig',

    # removed app, it's just here that the migration can run
    'foodsaving.walls',

    # Django packages
    'django_extensions',
    'corsheaders',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_nested',
    'rest_framework_swagger',
    'anymail',
    'influxdb_metrics',
    'timezone_field',
    'raven.contrib.django.raven_compat',
    'django_jinja',
    'channels',
)

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ),
    'EXCEPTION_HANDLER': 'foodsaving.utils.misc.custom_exception_handler'
}

MIDDLEWARE_CLASSES = (
    'influxdb_metrics.middleware.InfluxDBRequestMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.common.CommonMiddleware',
)

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        "BACKEND": "django_jinja.backend.Jinja2",
        "APP_DIRS": True,
        "OPTIONS": {
            "match_extension": ".jinja",
            "extensions": [
                "jinja2.ext.i18n",
            ],
            "autoescape": True,
        }
    },
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

REDIS_HOST = os.environ.get('REDIS_HOST', 'localhost')

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://{}:6379/0".format(REDIS_HOST),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"

WSGI_APPLICATION = 'config.wsgi.application'

EMAIL_BACKEND = "anymail.backends.sparkpost.EmailBackend"

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.BCryptPasswordHasher',
]

# Internationalization
# https://docs.djangoproject.com/en/dev/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'

CORS_ORIGIN_WHITELIST = []
# Allow all request origins. Will still require valid CSRF token and session information for modification but allows
# e.g. including the docs from any location
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True

SESSION_COOKIE_HTTPONLY = True

AUTH_USER_MODEL = 'users.User'

LOGIN_URL = '/api-auth/login/'
LOGOUT_URL = '/api-auth/logout/'

SILENCED_SYSTEM_CHECKS = [
    'urls.W005',  # we don't need to reverse backend URLs
]

DESCRIPTION_MAX_LENGTH = 100000
NAME_MAX_LENGTH = 80

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "asgi_redis.RedisChannelLayer",
        "CONFIG": {
            "hosts": [(REDIS_HOST, 6379)],
        },
        "ROUTING": "foodsaving.subscriptions.routing.channel_routing",
    },
}

CHANNELS_WS_PROTOCOLS = ['karrot.token']

# NB: Keep this as the last line, and keep
# local_settings.py out of version control
try:
    from .local_settings import *
except ImportError:
    raise Exception(
        "config/local_settings.py is missing! Copy the provided example file and adapt it to your own config.")
