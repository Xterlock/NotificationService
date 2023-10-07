from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from db.base import int_pk, SQLModel


class Client(SQLModel):
    __tablename__ = "clients"

    id: Mapped[int_pk]
    phone_number: Mapped[str] = mapped_column(String(length=11))
    operator_code: Mapped[str]
    tag: Mapped[str] = mapped_column(Text)
    timezone: Mapped[str]
