import datetime

from sqlalchemy import Text
from sqlalchemy.orm import Mapped, mapped_column

from db.base import SQLModel, int_pk


class Mailing(SQLModel):
    __tablename__ = "mailings"

    id: Mapped[int_pk]
    date_start: Mapped[datetime.datetime]
    date_end: Mapped[datetime.datetime]
    date_stop: Mapped[datetime.datetime]
    text: Mapped[str] = mapped_column(Text)
    filter: Mapped[str]
