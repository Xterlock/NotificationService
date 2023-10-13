from fastapi import APIRouter
from .client import router as client_router
from .mailing import router as mailing_router

api_router = APIRouter(prefix="/api/v1")

ROUTERS: list[APIRouter] = [
    client_router,
    mailing_router
]

[api_router.include_router(router) for router in ROUTERS]
