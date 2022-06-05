"""
This module implements UserService class, that encapsulates logic for managing User entity.
"""

from ..models.user_model import User
from ..repositories.errors import EntityIsNotUnique
from ..repositories.sqlalchemy_repository import SQLAlchemyRepository
from .abstract_service import AbstractService
from .errors import UserAlreadyExists


class UserService(AbstractService):
    """Service is responsible for managing User entity."""

    entity_repository: SQLAlchemyRepository

    async def new_user(
        self,
        username: str,
        email: str,
        first_name: str,
        last_name: str,
        password: str,
        is_admin: bool,
        is_employee: bool,
    ):
        """Create new user entity."""
        user_instance = self._create_user_instance(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password,
            is_admin=is_admin,
            is_employee=is_employee,
        )

        try:
            await self.entity_repository.create(user_instance)
        except EntityIsNotUnique as err:
            self._handle_entity_is_no_unique_error(err)

        return user_instance

    def test_func(self):
        pass

    @staticmethod
    def _create_user_instance(**kwargs) -> User:
        return User(**kwargs)

    @staticmethod
    def _handle_entity_is_no_unique_error(error):
        raise UserAlreadyExists(error.entity, 2)
