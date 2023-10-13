import asyncio
import os
from typing import AsyncGenerator

import pytest
from dotenv import load_dotenv
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from main import app
from src.db.model import SQLModel
from src.schemas.client import ClientSchemaAdd

load_dotenv()

TEST_DATABASE_URL = os.environ.get("TEST_DATABASE_URL")
async_engine = create_async_engine(TEST_DATABASE_URL)
test_session_maker = async_sessionmaker(async_engine, expire_on_commit=False)


@pytest.fixture(autouse=True)
async def test_async_session_maker():
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
        yield test_session_maker
        await conn.run_sync(SQLModel.metadata.drop_all)


@pytest.fixture(scope='session')
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test/api/v1") as ac:
        yield ac


@pytest.fixture()
async def added_client_schema():
    return ClientSchemaAdd(
        phone_number="79179999999",
        operator_code="917",
        tag="Test",
        timezone="UTC+5"
    )
