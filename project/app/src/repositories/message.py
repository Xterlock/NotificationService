from src.models.message import Message
from src.utils.irepository import SQLAlchemyRepository


class MessageRepository(SQLAlchemyRepository):
    model = Message
