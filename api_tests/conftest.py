"""
This module collects pytest fixtures needed for api testing.
"""

import pytest_asyncio
from httpx import AsyncClient

from restaurantservice.app import app


@pytest_asyncio.fixture()
async def api_client():
    """Return asynchronous client instance."""
    async with AsyncClient(app=app, base_url="http://test") as async_client:
        yield async_client
