from httpx import AsyncClient

from src.schemas.client import ClientSchemaAdd


async def test_added_client(async_client: AsyncClient, added_client_schema: ClientSchemaAdd):
    """
    Добавления нового клиента в справочник со всеми его атрибутами
    """
    result = await async_client.post("/client", json=added_client_schema.model_dump())
    data = result.json()
    assert isinstance(data, dict)
    assert isinstance(data["id"], int)
