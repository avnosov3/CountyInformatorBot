import logging

from celery import shared_task

from core.settings import CELERY_RETRY_ATTEMPTS, CELERY_WAITING_TIME_BEFORE_NEW_ATTEMPTS
from countries.client import country_client
from countries.repository import country_repository

logger = logging.getLogger(__name__)


@shared_task(bind=True, default_retry_delay=CELERY_RETRY_ATTEMPTS)
def create_and_update_countries(self):
    try:
        countries_in = country_client.get_countries()
        country_repository.create_countries(countries_in)
        country_repository.update_countries(countries_in)
    except Exception as error:
        logger.exception(error)
        raise self.retry(exc=error, countdown=CELERY_WAITING_TIME_BEFORE_NEW_ATTEMPTS)
