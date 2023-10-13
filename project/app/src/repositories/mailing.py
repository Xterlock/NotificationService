from src.models.mailing import Mailing
from src.utils.irepository import SQLAlchemyRepository


class MailingRepository(SQLAlchemyRepository):
    model = Mailing
