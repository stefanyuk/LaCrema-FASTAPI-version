"""
This module implements SQLAlchemy repository class that is used to access the database.
"""


from fastapi import Depends

from restaurantservice.database import get_session
from restaurantservice.repositories.errors import DatabaseNotReachableError

from .abstract_reposiitory import AbstractRepository


class SQLAlchemyRepository(AbstractRepository):
    """A class that encapsulates the logic required to access database."""

    DB_CHECK_QUERY = "SELECT 1"
    _db_session = None

    def __init__(self, db_session=Depends(get_session)):
        self._db_session = db_session

    def create(self):
        pass

    async def ping_db(self):
        """Execute a simple check query to db."""
        try:
            return await self._db_session.execute(self.DB_CHECK_QUERY)
        except Exception:  # pylint: disable=broad-except
            self._handle_db_error()

    @staticmethod
    def _handle_db_error():
        raise DatabaseNotReachableError
