"""
This module collects function and objects that are needed to setup a connection with the database.

Functions:
    get_session () -> AsyncSession
"""

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from restaurantservice.models import BaseModel, Token, User
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


async def create_admin_user():
    """Create admin user for the service."""
    async with async_session() as session:
        admin_user = User(
            id="90d9a781-6b7c-49b6-ad70-df41ac378b3c",
            last_name="Stef",
            first_name="Andriy",
            username="admin",
            password="admin",
            email="admin@email.com",
            is_admin=True,
        )
        session.add(admin_user)
        await session.commit()


async def create_admin_token():
    """Create first token for the admin user."""
    async with async_session() as session:
        admin_token = Token(
            id="92516b88-f3c8-42ac-a0ce-1cb48c14f7f9",
            user_id="90d9a781-6b7c-49b6-ad70-df41ac378b3c",
        )
        session.add(admin_token)
        await session.commit()


# eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiOTBkOWE3ODEtNmI3Yy00OWI2LWFkNzAtZGY0MWFjMzc4YjNjIiwidG9rZW5faWQiOiI5MjUxNmI4OC1mM2M4LTQyYWMtYTBjZS0xY2I0OGMxNGY3ZjkifQ.JMDP6XX-RM80Grkkm1NzWifxHXtSdCsVVHEm_u2JfYM


if __name__ == "__main__":
    import asyncio

    asyncio.get_event_loop().run_until_complete(create_all_tables())
    asyncio.get_event_loop().run_until_complete(create_admin_user())
    asyncio.get_event_loop().run_until_complete(create_admin_token())
