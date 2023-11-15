import logging

from celery import shared_task
from django.core.cache import caches

from core.settings import CELERY_RETRY_ATTEMPTS, CELERY_WAITING_TIME_BEFORE_NEW_ATTEMPTS
from currencies.apps import CurrencyConfig
from currencies.client import currency_client

logger = logging.getLogger(__name__)


@shared_task(bind=True, default_retry_delay=CELERY_RETRY_ATTEMPTS)
def create_and_update_currencies(self):
    try:
        currency_cache = caches[CurrencyConfig.name]
        currency_cache.set_many(currency_client.get_currencies())
    except Exception as error:
        logger.exception(error)
        raise self.retry(exc=error, countdown=CELERY_WAITING_TIME_BEFORE_NEW_ATTEMPTS)
