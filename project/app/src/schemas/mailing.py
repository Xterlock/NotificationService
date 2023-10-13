import datetime
from typing import Optional

from pydantic import BaseModel


class MailingSchemaBase(BaseModel):
    date_start: datetime.datetime
    date_end: datetime.datetime
    text: str
    tag_filter: Optional[str] = None
    operator_code_filter: Optional[str] = None


class MailingTaskSchemaResponse(BaseModel):
    id: int
    created_message_ids: list[int] = []


class MailingSchemaAdd(MailingSchemaBase):
    pass


class MailingSchemaResponse(MailingSchemaBase):
    id: int


class UpdateMailingSchema(BaseModel):
    date_start: Optional[datetime.datetime] = None
    date_end: Optional[datetime.datetime] = None
    text: Optional[str] = None
    tag_filter: Optional[str] = None
    operator_code_filter: Optional[str] = None

    def get_values_dict(self) -> dict:
        values = {}
        if self.date_start:
            values["date_start"] = self.date_start
        if self.date_end:
            values["date_end"] = self.date_end
        if self.text:
            values["text"] = self.text
        if self.tag_filter:
            values["tag_filter"] = self.tag_filter
        if self.operator_code_filter:
            values["operator_code_filter"] = self.operator_code_filter
        return values
