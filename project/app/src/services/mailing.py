import asyncio
import datetime
from typing import List

from celery.result import AsyncResult
from fastapi import HTTPException, BackgroundTasks

from loguru import logger
from starlette import status

from src.models import Client
from src.models.mailing import Mailing
from src.repositories.client import ClientRepository
from src.schemas.message import MessageSchemaResponse, DeleteMessageSchema
from src.services.message import MessageServices

from src.repositories.mailing import MailingRepository
from src.schemas.mailing import (
    MailingSchemaAdd,
    MailingTaskSchemaResponse,
    MailingSchemaResponse,
)
from src.tasks.celery.check_message import check_task
from src.tasks.celery.message import delete_task
from src.worker.celery import create_celery

celery_app = create_celery()


class MailingServices:
    repository = MailingRepository()
    client_repository = ClientRepository()
    message_service = MessageServices()

    async def get_mailing(self, mailing_id: int) -> MailingSchemaResponse:
        mailing_model = await self.repository.find_all(id=mailing_id)
        if not mailing_model:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="not found")
        return mailing_model.read_to_schema()

    async def find_mailing_by_data(self, search_date: datetime.date) -> List[MailingSchemaResponse] | List:
        criteria = Mailing.date_start >= search_date
        mailing_models = await self.repository.find_all(criteria)
        return [model.read_to_schema() for model in mailing_models] if mailing_models else []

    async def add_mailing(self, schema: MailingSchemaAdd) -> MailingTaskSchemaResponse:
        """Добавления новой рассылки со всеми её атрибутами"""
        try:
            mailing_id = await self.repository.add_one(schema.model_dump())
        except Exception as ex:
            logger.error(f"Ошибка при добавление новой рассылки: {ex}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
        try:
            message_ids = await self.__send_mailing(schema, mailing_id)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_200_OK,
                detail={"message_ids": [], "detail": "Не полилось найти не одного пользователя по параметрам"}
            )
        return MailingTaskSchemaResponse(id=mailing_id, created_message_ids=message_ids)

    async def update_attributes(self, mailing_id: int, attributes: dict):
        mailing_model = await self.repository.edit_one(attributes, id=mailing_id)
        return mailing_model.read_to_schema()

    async def delete_mailing(self, mailing_id: int, del_task: bool, bg_task: BackgroundTasks):

        if not del_task:
            return DeleteMessageSchema(status="success")
        messages = await self.message_service.find_messages_by_mailing_id(mailing_id)
        if messages:
            bg_task.add_task(self.__delete_task, mailing_id, messages)
        return DeleteMessageSchema(status="success", amount_deleted_task=len(messages))

    async def __send_mailing(self, schema: MailingSchemaAdd, mailing_id: int) -> list[int]:
        criteria = (Client.tag == schema.tag_filter) | (Client.operator_code == schema.operator_code_filter)
        clients = await self.client_repository.find_all(criteria)
        if not clients:
            raise ValueError
        date_now = datetime.datetime.now(tz=schema.date_end.tzinfo)
        scheduler = {}
        if not schema.date_end > date_now > schema.date_start:
            logger.info("Send later")
            start_time_diff = date_now - schema.date_start
            end_time_diff = date_now - schema.date_end
            scheduler["expires"] = int(end_time_diff.total_seconds())
            scheduler["countdown"] = int(start_time_diff.total_seconds())
        message_ids, task_ids = [], []
        for client in clients:
            message_id, task_id = await self.message_service.send_message(client, schema.text, mailing_id, **scheduler)
            message_ids.append(message_id), task_ids.append(task_id)

        check_task.apply_async((task_ids,), **scheduler)
        return message_ids

    async def __delete_task(self, mailing_id: int, messages: List[MessageSchemaResponse]):
        logger.info("delete celery tasks")
        loop = asyncio.get_running_loop()
        background_tasks = set()
        for message in messages:
            result = await loop.run_in_executor(None, AsyncResult, message.task_id)
            if result.state in ["STARTED", "SUCCESS"]:
                # if result.state not in ["STARTED", "SUCCESS"]:
                await delete_task(message.task_id)
                await self.message_service.delete_message(message.id)
                # background_tasks.add(del_task_cache_task)
                # background_tasks.add(del_message_task)
        # await asyncio.gather(*background_tasks)
        await self.repository.delete_one(id=mailing_id)
