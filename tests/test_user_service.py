import pytest

from restaurantservice.services.user_service import UserService


@pytest.mark.asyncio
def test_new_user_returns_user_entity_on_successfull_creation(
    async_repository_mock, async_session_mock
):
    srv = UserService(async_repository_mock)
    user_entity = srv.new_user()
