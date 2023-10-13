import datetime

from sqlalchemy import ForeignKey, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column

from src.db.model import SQLModel, int_pk
from src.schemas.message import MessageSchemaResponse


class Message(SQLModel):
    __tablename__ = "messages"

    id: Mapped[int_pk]
    task_id: Mapped[str] = mapped_column(unique=True)
    date_created: Mapped[datetime.datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        default=datetime.datetime.now
    )
    status: Mapped[bool] = mapped_column(nullable=True)

    client_id: Mapped[int] = mapped_column(ForeignKey("clients.id"))
    mailing_id: Mapped[int] = mapped_column(ForeignKey("mailings.id"))

    def read_to_model(self) -> MessageSchemaResponse:
        return MessageSchemaResponse(
            id=self.id,
            task_id=self.task_id,
            date_created=self.date_created,
            status=self.status,
            client_id=self.client_id,
            mailing_id=self.mailing_id
        )
