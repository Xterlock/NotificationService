import pytest

from src.schemas.client import ClientSchemaUpdate
from src.services.client import ClientServices


@pytest.fixture
async def client_service() -> ClientServices:
    yield ClientServices()


@pytest.fixture
async def attributes() -> ClientSchemaUpdate:
    yield ClientSchemaUpdate(
        phone_number="79179999988",
        operator_code="918",
        tag="TestUpdate",
        timezone="UTC+6"
    )
