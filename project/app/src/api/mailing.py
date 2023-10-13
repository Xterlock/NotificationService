import datetime
from typing import List, Optional

from celery.result import AsyncResult
from fastapi import APIRouter
from starlette import status
from starlette.background import BackgroundTasks
from starlette.responses import JSONResponse

from src.dependencies import MailingService
from src.schemas.mailing import (
    MailingSchemaAdd,
    MailingSchemaResponse,
    MailingTaskSchemaResponse, UpdateMailingSchema
)

router = APIRouter(prefix="/mailing", tags=["Mailing"])


@router.post("", response_model=MailingTaskSchemaResponse, status_code=status.HTTP_201_CREATED)
async def added_mailing(mailing: MailingSchemaAdd, service: MailingService):
    """Добавления новой рассылки со всеми её атрибутами"""
    result = await service.add_mailing(mailing)
    return result


@router.get("/{mailing_id}", response_model=MailingSchemaResponse)
async def get_mailing(mailing_id: int, service: MailingService):
    mailing = await service.get_mailing(mailing_id)
    return mailing


@router.get("/fetch/date", response_model=List[MailingSchemaResponse])
async def fetch_mailing_by_date(search_date: datetime.date, service: MailingService):
    mailings = await service.find_mailing_by_data(search_date)
    return mailings


@router.patch("/{mailing_id}", response_model=MailingSchemaResponse, status_code=status.HTTP_202_ACCEPTED)
async def update_mailing_attributes(mailing_id: int, schema: UpdateMailingSchema, service: MailingService):
    """Обновления атрибутов рассылки"""
    attributes = schema.get_values_dict()
    mailing = await service.update_attributes(mailing_id, attributes)
    return mailing


@router.get("/task/{task_id}")
async def mailing_task_status(task_id: str):
    task_result = AsyncResult(task_id)
    result = {
        "task_id": task_id,
        "task_status": task_result.status,
        "task_result": task_result.result
    }
    return JSONResponse(result)


@router.delete("/{mailing_id}")
async def delete_mailing(
        mailing_id: int, bg_task: BackgroundTasks, service: MailingService, delete_tasks: bool = False):
    result = await service.delete_mailing(mailing_id, delete_tasks, bg_task)
    return result
