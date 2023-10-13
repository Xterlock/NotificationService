from typing import Union

from pydantic import BaseModel


class IdResponse(BaseModel):
    id: Union[str, int]


class ResponseStatus(BaseModel):
    status: str
