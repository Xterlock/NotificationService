from celery import current_app as current_celery_app
from celery.result import AsyncResult

from src.worker.config import get_worker_settings

config = get_worker_settings()


def create_celery():
    celery_app = current_celery_app
    celery_app.config_from_object(config, namespace="CELERY")
    return celery_app



