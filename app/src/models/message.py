from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from db.base import SQLModel, datetime_now, int_pk


class Message(SQLModel):
    __tablename__ = "messages"

    id: Mapped[int_pk]
    date_created: Mapped[datetime_now]
    status: Mapped[bool]

    client_id: Mapped[int] = mapped_column(ForeignKey("clients.id"))
    mailing_id: Mapped[int] = mapped_column(ForeignKey("mailings.id"))
