import datetime

from sqlalchemy.dialects.mysql import TEXT, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column

from src.db.model import SQLModel, int_pk
from src.schemas.mailing import MailingSchemaResponse


class Mailing(SQLModel):
    __tablename__ = "mailings"

    id: Mapped[int_pk]
    date_start: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(timezone=True))
    date_end: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(timezone=True))
    text: Mapped[str] = mapped_column(TEXT)
    tag_filter: Mapped[str] = mapped_column(nullable=True)
    operator_code_filter: Mapped[str] = mapped_column(nullable=True)

    def read_to_schema(self) -> MailingSchemaResponse:
        return MailingSchemaResponse(
            id=self.id,
            date_start=self.date_start,
            date_end=self.date_end,
            text=self.text,
            tag_filter=self.tag_filter,
            operator_code_filter=self.operator_code_filter
        )
