import os

from celery import Celery
from celery.signals import worker_ready

from core.settings import BEAT_COUNTRY, BEAT_CURRENCIES, BEAT_WEATHER

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

app = Celery("core")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()


@worker_ready.connect
def on_startup(sender, **kwargs):
    with sender.app.connection() as conn:
        sender.app.send_task(BEAT_COUNTRY, connection=conn)
        sender.app.send_task(BEAT_CURRENCIES, connection=conn)
        sender.app.send_task(BEAT_WEATHER, connection=conn)
