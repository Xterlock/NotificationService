from typing import List, Optional

from loguru import logger

from src.models import Client

from src.repositories.message import MessageRepository
from src.schemas.message import MessageSchemaResponse
from src.tasks.celery.message import create_task_send_message


class MessageServices:
    repository = MessageRepository()

    async def send_message(self, client: Client, text: str, mailing_id: int, **kwargs) -> (int, str):
        """Отправить сообщений сейчас"""
        send_task = create_task_send_message.apply_async((client.phone_number, text), **kwargs)
        values = {"client_id": client.id, "mailing_id": mailing_id, "task_id": send_task.id}
        message_id = await self.repository.add_one(values)
        return message_id, send_task.id

    async def update_message_status(self, status: bool, task_id: str):
        logger.info("update message status")
        values = {"status": status}
        await self.repository.edit_one(values, task_id=task_id)

    async def delete_message(self, message_id: int):
        logger.info(f"delete message {message_id}")
        await self.repository.delete_one(id=message_id)

    async def find_messages_by_mailing_id(self, mailing_id: int) -> List[MessageSchemaResponse]:
        messages = await self.repository.find_all(**{"mailing_id": mailing_id})
        return [message.read_to_model() for message in messages]
