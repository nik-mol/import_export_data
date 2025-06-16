import os

import django
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
django.setup()

celery_app = Celery(
    name="backend",
    broker_connection_retry_on_startup=True,
)


celery_app.config_from_object("django.conf:settings", namespace="CELERY")
celery_app.autodiscover_tasks()
