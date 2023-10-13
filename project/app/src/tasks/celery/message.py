import asyncio

from loguru import logger

from src.worker.celery import create_celery

celery = create_celery()


async def delete_task(task_id: str):
    logger.info(f"delete task: {task_id}")
    loop = asyncio.get_running_loop()
    await loop.run_in_executor(None, celery.control.revoke, task_id)


@celery.task(name="create_task_send_message")
def create_task_send_message(phone_number: str, text: str):
    return True
