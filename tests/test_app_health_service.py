# pylint: disable=missing-module-docstring, missing-function-docstring

import pytest

from restaurantservice.repositories.errors import DatabaseNotReachableError
from restaurantservice.services import app_health_service
from restaurantservice.services.errors import AppIsNotHealthyError


@pytest.mark.asyncio
async def test_app_health_service_returns_true_when_app_is_healthy(
    async_repository_mock,
):
    async_repository_mock.ping_db.return_value = True
    srv = app_health_service.AppHealthService(async_repository_mock)

    assert await srv.is_app_healthy()


@pytest.mark.asyncio
async def test_app_health_service_raises_error_when_app_is_not_healthy(
    async_repository_mock,
):
    async_repository_mock.ping_db.side_effect = DatabaseNotReachableError
    srv = app_health_service.AppHealthService(async_repository_mock)
    with pytest.raises(AppIsNotHealthyError):
        assert await srv.is_app_healthy()
