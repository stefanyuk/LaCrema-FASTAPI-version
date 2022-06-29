"""
This module implements UserService class, that encapsulates logic for managing User entity.
"""

import datetime
from uuid import UUID

from ..models import Token, User
from ..repositories.errors import EntityDoesNotExist, EntityIsNotUnique
from ..repositories.sqlalchemy_repository import SQLAlchemyRepository
from .abstract_service import AbstractService
from .errors import TokenDoesNotExist, UserAlreadyExists, UserDoesNotExist


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
        is_admin: bool = False,
        is_employee: bool = False,
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
            self._handle_entity_is_not_unique_error(err)

        return user_instance

    async def get_user(self, user_id: UUID, for_update: bool = False):
        """
        Get and return user entity based on the provided id.
        :param user_id: uuid, unique user identifier
        :param for_update: bool, indicates whether user will be updated
        :raises UserDoesNotExist: when user with the provided id does not exist
        """
        try:
            return await self.entity_repository.get_by_id(
                User, user_id, for_update=for_update
            )
        except EntityDoesNotExist:
            self._handle_entity_does_not_exist(user_id)

    async def get_user_token(self, user: User, token_id: UUID):
        """
        Return token instance that belongs to the provided user.
        :param user: instance of the user, token of which should be retrieved
        :param token_id: uuid, unique token identifier
        """
        for token in user.tokens:
            if token.id == token_id:
                return token

        self._handle_token_does_not_exist(token_id)

    async def create_user_token(self, user: User):
        """
        Create new token for the provided user.
        :param user: user for which token should be created
        """
        token_instance = self._create_token_instance(user_id=user.id)
        await self.entity_repository.create(token_instance)
        return token_instance

    async def update_user_last_login_time(
        self, user: User, new_last_login_time: datetime
    ):
        """
        Update last_login attribute value for the specified user.

        :param user: instance of the user that should be updated
        :param new_last_login_time: datetime, time for last login update
        """
        user.last_login = new_last_login_time
        await self.entity_repository.update(user)
        return user

    @staticmethod
    def _create_user_instance(**kwargs) -> User:
        return User(**kwargs)

    @staticmethod
    def _create_token_instance(user_id: UUID) -> User:
        return Token(user_id=user_id)

    @staticmethod
    def _handle_entity_is_not_unique_error(error):
        raise UserAlreadyExists(error.entity, error.detail)

    @staticmethod
    def _handle_entity_does_not_exist(user_id: UUID):
        raise UserDoesNotExist(user_id)

    @staticmethod
    def _handle_token_does_not_exist(token_id: UUID):
        raise TokenDoesNotExist(token_id)
