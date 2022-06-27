"""
This module collects function and objects that are needed to setup a connection with the database.

Functions:
    get_session () -> AsyncSession
"""

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from restaurantservice.models.base_model import BaseModel
from restaurantservice.settings import get_settings

engine = create_async_engine(get_settings().db_connection_string, echo=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_session() -> AsyncSession:
    """Return asynchronous session object."""
    async with async_session() as session:
        yield session


async def create_all_tables():
    """Delete and recreate all tables."""
    meta = BaseModel.metadata
    async with engine.begin() as conn:
        await conn.run_sync(meta.reflect)
        await conn.run_sync(meta.drop_all)
        await conn.run_sync(meta.create_all)
