import datetime

from sqlalchemy.orm import DeclarativeBase, mapped_column
from typing import Annotated

int_pk = Annotated[int, mapped_column(primary_key=True)]


class SQLModel(DeclarativeBase):
    """Базовая модель для SQL таблиц"""
    pass
