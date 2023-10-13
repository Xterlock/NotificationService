from src.models import Client
from src.utils.irepository import SQLAlchemyRepository


class ClientRepository(SQLAlchemyRepository):
    model = Client
