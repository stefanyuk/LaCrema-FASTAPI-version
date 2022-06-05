"""
This module implements AppHealthService class,
that encapsulates logic for checking application health.
"""

from ..repositories.errors import DatabaseNotReachableError
from ..repositories.sqlalchemy_repository import SQLAlchemyRepository
from .abstract_service import AbstractService
from .errors import AppIsNotHealthyError


class AppHealthService(AbstractService):
    """Service is responsible for application health."""

    entity_repository: SQLAlchemyRepository

    async def is_app_healthy(self):
        """Verify whether application is healthy."""
        try:
            return await self.entity_repository.ping_db()
        except DatabaseNotReachableError:
            self._handle_db_not_reachable_error()
            print(2)

    @staticmethod
    def _handle_db_not_reachable_error():
        raise AppIsNotHealthyError
