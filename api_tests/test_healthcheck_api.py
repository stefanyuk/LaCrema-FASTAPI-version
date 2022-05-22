from unittest import mock

import pytest

from restaurantservice.services import app_health_service
from restaurantservice.services.errors import AppIsNotHealthyError


@pytest.mark.asyncio
async def test_healthcheck_api_returns_200_when_app_is_healthy(api_client):
    response = await api_client.get("/health")
    assert response.status_code == 200


@pytest.mark.asyncio
@mock.patch.object(app_health_service.AppHealthService, "is_app_healthy", autospec=True)
async def test_healthcheck_api_returns_503_when_app_is_not_healthy(
    mocked_service, api_client
):
    """
    Test if API returns HTTP status code 503 in case if application is not healthy.
    :param mocked_service: Mock object that is used to simulate unhealthy behaviour of the app
    """
    mocked_service.side_effect = AppIsNotHealthyError
    response = await api_client.get("/health")
    assert response.status_code == 503
