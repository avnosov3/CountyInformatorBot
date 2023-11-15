from pathlib import Path

import environ
from celery.schedules import crontab

from cities.apps import CitiesConfig
from countries.apps import CountriesConfig
from currencies.apps import CurrencyConfig
from weather.apps import name as weather_app

env = environ.Env(
    SLEEP_TIME=(float),
    LIST_PER_PAGE=(int),
)


BASE_DIR = Path(__file__).resolve().parent.parent

environ.Env.read_env(BASE_DIR.parent / '.env')

LIST_PER_PAGE = env('LIST_PER_PAGE')

SECRET_KEY = env('SECRET_KEY')

DEBUG = env('DEBUG', default=False)

ALLOWED_HOSTS = env('ALLOWED_HOSTS', default=['*'])

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django_celery_beat',
    'django_object_actions',

    'cities',
    'countries',
    'currencies',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

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

WSGI_APPLICATION = 'core.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': env('ENGINE'),
        'USER': env('DB_USER'),
        'PASSWORD': env('DB_PASSWORD'),
        'NAME': env('DB_NAME'),
        'HOST': env('DB_HOST'),
        'PORT': env('DB_PORT'),
    }
}


CACHE_ENABLE = env('CACHE_ENABLE')

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': env('DEFAULT_CACHE_URL'),
    },
    CurrencyConfig.name: {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': env('CURRENCIES_CACHE_URL'),
        'TIMEOUT': env('CURRENCY_TIMEOUT')
    },
    weather_app: {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': env('WEATHER_CACHE_URL'),
        'TIMEOUT': env('WEATHER_CACHE_TIMEOUT')
    },
    CountriesConfig.name: {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': env('COUNTRIES_CACHE_URL'),
        'TIMEOUT': env('COUNTRIES_CACHE_TIMEOUT')
    },
    CitiesConfig.name: {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': env('CITIES_CACHE_URL'),
        'TIMEOUT': env('CITIES_CACHE_TIMEOUT')
    },
}

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

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'static'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CELERY_BROKER_URL = env('CELERY_BROKER_URL')

CELERY_RETRY_ATTEMPTS = env("CELERY_RETRY_ATTEMPTS")
CELERY_WAITING_TIME_BEFORE_NEW_ATTEMPTS = env("CELERY_WAITING_TIME_BEFORE_NEW_ATTEMPTS")
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE

BEAT_COUNTRY = 'countries.tasks.create_and_update_countries'
BEAT_CURRENCIES = 'currencies.tasks.create_and_update_currencies'
BEAT_WEATHER = 'weather.tasks.delete_weather_from_redis'

CELERY_IMPORTS = [
    'weather.tasks',
]

CELERY_BEAT_SCHEDULE = {
    'create_and_update_countries': {
        'task': BEAT_COUNTRY,
        'schedule':  crontab(
            minute='0',
            hour='3',
            day_of_week='1',
            month_of_year='*/6'
        ),
    },
    'create_and_update_currencies': {
        'task': BEAT_CURRENCIES,
        'schedule':  crontab(
            minute='0',
            hour='0',
        ),
    },
    'delete_weather_from_redis': {
        'task': BEAT_WEATHER,
        'schedule':  crontab(
            minute='0',
            hour='*/3'
        ),
    },
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': 'django.log',
            'formatter': 'verbose',
        },
        'console': {
            'level': 'ERROR',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['file', 'console'],
        'level': 'DEBUG',
    },
}
