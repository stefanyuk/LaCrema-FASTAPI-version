# pylint: disable=missing-module-docstring, missing-function-docstring

import pytest

from restaurantservice.repositories.errors import DatabaseNotReachableError
from restaurantservice.repositories.sqlalchemy_repository import SQLAlchemyRepository


@pytest.mark.asyncio
async def test_ping_db_returns_true_when_db_is_reachable(async_session_mock):
    async_session_mock.execute.return_value = True
    repo = SQLAlchemyRepository(async_session_mock)

    assert await repo.ping_db()


@pytest.mark.asyncio
async def test_ping_db_raises_db_not_reachable_error_when_db_is_not_reachable(
    async_session_mock,
):
    async_session_mock.execute.side_effect = Exception
    repo = SQLAlchemyRepository(async_session_mock)

    with pytest.raises(DatabaseNotReachableError):
        await repo.ping_db()
