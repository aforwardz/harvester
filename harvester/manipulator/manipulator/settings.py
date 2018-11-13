"""
Django settings for manipulator project.

Generated by 'django-admin startproject' using Django 2.0.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'y4q0b%c6u*^06p%e!+pgy94d6qjl__v3@eypyc)x9blih98%10'

# SECURITY WARNING: don't run with debug turned on in production!
import socket
hostname = socket.gethostname()

if hostname == 'aforwardz':
    DEBUG = False

    ALLOWED_HOSTS = [
        'aforwardz.com'
    ]

    from harvester import private_settings
    DEFAULT_DB_NAME = private_settings.DEFAULT_DB_NAME
    DEFAULT_DB_USER = private_settings.DEFAULT_DB_USER
    DEFAULT_DB_PASSWORD = private_settings.DEFAULT_DB_PASSWORD

    EMAIL_HOST_USER = private_settings.EMAIL_HOST_USER
    EMAIL_HOST_PASSWORD = private_settings.EMAIL_HOST_PASSWORD

else:
    DEBUG = True

    ALLOWED_HOSTS = [
        '127.0.0.1',
        '127.0.0.1:8080'
    ]

    DEFAULT_DB_NAME = 'harvester'
    DEFAULT_DB_USER = 'harvester'
    DEFAULT_DB_PASSWORD = '666666'

    EMAIL_HOST_USER = ''
    EMAIL_HOST_PASSWORD = ''

    USER_SESSION_EXPIRE = 30 * 60

    CORS_ORIGIN_ALLOW_ALL = False
    CORS_ALLOW_CREDENTIALS = True
    CORS_ORIGIN_WHITELIST = (
        'localhost',
        '127.0.0.1:8080'
    )

    SESSION_COOKIE_HTTPONLY = False


# Application definition

INSTALLED_APPS = [
    'jet',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'seed',
    'peeler'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'manipulator.urls'

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

WSGI_APPLICATION = 'manipulator.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': DEFAULT_DB_NAME,
        'USER': DEFAULT_DB_USER,
        'PASSWORD': DEFAULT_DB_PASSWORD,
        'HOST': '127.0.0.1',
        'PORT': '5432',
    },
}


# Redis
REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379
REDIS_DB = 2

# Media
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# Web HTML
WEB_ROOT = os.path.join(BASE_DIR, 'seller')
WEB_URL = '/seller/'

# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        # 'rest_framework.authentication.TokenAuthentication',
        # 'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_FILTER_BACKENDS': ('rest_framework.filters.DjangoFilterBackend',),
    'DEFAULT_PAGINATION_CLASS':
        'rest_framework.pagination.LimitOffsetPagination',
    'DATETIME_FORMAT': '%Y-%m-%d %H:%M:%S',
    'GENERIC_SEARCH_PARAM': 'generic_search',
}


# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(BASE_DIR, 'static'),
)
STATIC_ROOT = os.path.join(BASE_DIR, 'static_deployment')


if not DEBUG:
    ADMINS = (
        ('yucongwei', 'yucongwei@aforwardz.com'),
    )
    SERVER_EMAIL = 'god@aforwardz.com'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.mxhichina.com'
EMAIL_PORT = 25
EMAIL_HOST_USER = EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = EMAIL_HOST_PASSWORD
DEFAULT_FROM_EMAIL = 'Harvester <{}>'.format(EMAIL_HOST_USER)

# Log
LOG_DIR = os.path.join(BASE_DIR, 'logs')
if not os.path.exists(LOG_DIR):
    os.mkdir(LOG_DIR)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %('
                      'thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(asctime)s %(message)s'
        },
        'detail': {
            'format': '[%(levelname)s] %(asctime)s %(filename)s:%(lineno)-4s: %(message)s'
        },
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'logs/django.log',
            'formatter': 'simple',
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            # 'filters': ['special']
        },
        'peeler': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'logs/peeling_record.log',
            'formatter': 'detail'
        }

    },
    'loggers': {
        'django': {
            'handlers': ['null'],
            'propagate': True,
            'level': 'INFO',
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
        'peeler': {
            'handlers': ['peeler', 'console'],
            'level': 'INFO',
            'propagate': False
        }
    }
}


JET_INDEX_DASHBOARD = 'jet.dashboard.dashboard.DefaultIndexDashboard'
JET_APP_INDEX_DASHBOARD = 'jet.dashboard.dashboard.DefaultAppIndexDashboard'


DICTIONARY_ROOT = os.path.join(BASE_DIR, 'dictionary')
DICTIONARY = os.path.join(DICTIONARY_ROOT, 'dictionary.json')
RE_DICTIONARY = os.path.join(DICTIONARY_ROOT, 're_dictionary.json')
STOPWORDS = os.path.join(DICTIONARY_ROOT, 'stopwords.txt')

TENSORBOARD_ROOT = '/tmp/'

TFRECORD_ROOT = os.path.join(BASE_DIR, 'tfrecord')
CLASSIFY_TFRECORD = os.path.join(TFRECORD_ROOT, 'classify')
EMBEDDING_TFRECORD = os.path.join(TFRECORD_ROOT, 'embedding')

SESSION_ROOT = os.path.join(BASE_DIR, 'models')
CLASSIFY_SESSION = os.path.join(SESSION_ROOT, 'classify')

EMBEDDING_SESSION = os.path.join(SESSION_ROOT, 'embedding')

