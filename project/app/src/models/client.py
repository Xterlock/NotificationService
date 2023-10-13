from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from src.db.model import SQLModel, int_pk
from src.schemas.client import ClientSchemaResponse


class Client(SQLModel):
    __tablename__ = "clients"

    id: Mapped[int_pk]
    phone_number: Mapped[str] = mapped_column(String(length=11))
    operator_code: Mapped[str]
    tag: Mapped[str] = mapped_column(Text)
    timezone: Mapped[str]

    def read_to_schema(self) -> ClientSchemaResponse:
        return ClientSchemaResponse(
            id=self.id,
            phone_number=self.phone_number,
            operator_code=self.operator_code,
            tag=self.tag,
            timezone=self.timezone
        )
