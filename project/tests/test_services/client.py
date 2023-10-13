from src.schemas.client import ClientSchemaAdd, ClientSchemaUpdate
from src.services.client import ClientServices


async def added_client_positive_test(client_service: ClientServices, schema: ClientSchemaAdd):
    """Добавление нового клиента позитивный тест"""
    user_id = await client_service.added_client(schema)
    assert isinstance(user_id, int)


async def update_client_attributes_positive_test(client_service: ClientServices, attributes: ClientSchemaUpdate):
    user_id = await client_service.update_client_attributes(1, attributes)
    assert user_id == 1
