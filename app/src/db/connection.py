from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from settings import base_setting

base_db_url = base_setting.db.get_url()

async_engine = create_async_engine(base_db_url)
async_session_maker = async_sessionmaker(async_engine, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Создание асинхронной сессии
    """
    async with async_session_maker() as session:
        yield session
