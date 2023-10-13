from fastapi import FastAPI

from settings import base_setting
from src.api.routers import api_router
from src.worker.celery import create_celery

app = FastAPI(title=base_setting.app.title)
app.celery_app = create_celery()

celery = app.celery_app

app.include_router(api_router)


# @app.on_event("startup")
# def startup_event():
#     start_schedulers(
#         host=base_setting.cache.host,
#         port=base_setting.cache.port,
#         db=base_setting.cache.db
#     )
