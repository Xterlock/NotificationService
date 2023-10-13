import asyncio

from asgiref.sync import async_to_sync
from celery.result import AsyncResult
from loguru import logger

from src.services.message import MessageServices
from src.worker.celery import create_celery

celery = create_celery()


@celery.task(name="check_task")
def check_task(task_ids: list[str]):
    logger.info("start bg task check_send_message_task")
    message_service = MessageServices()
    loop = asyncio.get_event_loop()
    while task_ids:
        task_id = task_ids.pop(0)
        task_result = AsyncResult(task_id)
        if task_result.result is not None:
            logger.info(f"Task: {task_id}, result: {task_result.result}")
            loop.run_until_complete(message_service.update_message_status(task_result.result, task_id))
            continue
        task_ids.append(task_id)
    logger.info("Exit bg task check_send_message_task")
