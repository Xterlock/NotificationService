import datetime
from typing import Optional

from pydantic import BaseModel


class MessageSchemaAdd(BaseModel):
    status: bool
    client_id: int
    mailing_id: int


class MessageSchemaResponse(BaseModel):
    id: int
    task_id: str
    date_created: datetime.datetime
    status: Optional[bool]
    client_id: int
    mailing_id: int


class DeleteMessageSchema(BaseModel):
    status: str
    amount_deleted_task: int = 0
