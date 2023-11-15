import logging

from celery import shared_task
from django.core.cache import caches

from core.settings import CELERY_RETRY_ATTEMPTS, CELERY_WAITING_TIME_BEFORE_NEW_ATTEMPTS
from weather.apps import name as weather_app

logger = logging.getLogger(__name__)


@shared_task(bind=True, default_retry_delay=CELERY_RETRY_ATTEMPTS)
def delete_weather_from_redis(self):
    try:
        weather_cache = caches[weather_app]
        weather_cache.clear()
    except Exception as error:
        logger.exception(error)
        raise self.retry(exc=error, countdown=CELERY_WAITING_TIME_BEFORE_NEW_ATTEMPTS)
