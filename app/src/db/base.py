import datetime

from sqlalchemy.orm import DeclarativeBase, mapped_column
from typing import Annotated


class SQLModel(DeclarativeBase):
    """Базовая модель для SQL таблиц"""
    pass


int_pk = Annotated[int, mapped_column(primary_key=True)]
datetime_now = Annotated[datetime.datetime, mapped_column(default=datetime.datetime.utcnow)]
