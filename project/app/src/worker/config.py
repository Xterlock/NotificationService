from settings import base_setting

BROKER_URL = base_setting.cache.get_url_redis()


class WorkerConfig:
    """Celery Configuration"""
    broker_url = BROKER_URL
    result_backend = BROKER_URL
    include: list = ['src.tasks.celery']


def get_worker_settings():
    return WorkerConfig()
