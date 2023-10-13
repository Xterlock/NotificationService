import re
from typing import Optional

from pydantic import BaseModel, field_validator, Field


class ClientSchemaAdd(BaseModel):
    """
    Схема добавления пользователя
    """
    phone_number: str = Field(max_length=11)
    tag: str

    @field_validator('phone_number')
    @classmethod
    def validate_phone_number(cls, field: str) -> str:
        """
        Проверка телефонного номера на формат 7XXXXXXXXXX (X - цифра от 0 до 9)
        :param field: номер телефона
        """
        pattern = "^7\d{10}$"
        match = re.match(pattern, field)
        if match:
            return field
        raise ValueError("Phone Number Invalid")


class ClientSchemaUpdate(BaseModel):
    phone_number: Optional[str] = Field(max_length=11)
    operator_code: Optional[str]
    tag: Optional[str]
    timezone: Optional[str]

    @field_validator('phone_number')
    @classmethod
    def validate_phone_number(cls, field: str) -> str:
        """
        Проверка телефонного номера на формат 7XXXXXXXXXX (X - цифра от 0 до 9)
        :param field: номер телефона
        """
        if not field:
            return field
        pattern = "^7\d{10}$"
        match = re.match(pattern, field)
        if match:
            return field
        raise ValueError("Phone Number Invalid")

    def get_values_dict(self) -> dict:
        # TODO Подумать как сделать лучше
        values = {}
        if self.phone_number:
            values["phone_number"] = self.phone_number
        if self.operator_code:
            values["operator_code"] = self.operator_code
        if self.tag:
            values["tag"] = self.tag
        if self.timezone:
            values["timezone"] = self.timezone
        return values


class ClientSchemaResponse(BaseModel):
    id: int
    phone_number: str
    operator_code: str
    tag: str
    timezone: str
