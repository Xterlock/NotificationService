from fastapi import FastAPI

from settings import base_setting

app = FastAPI(
    title=base_setting.app.title
)
