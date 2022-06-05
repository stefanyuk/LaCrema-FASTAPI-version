"""
This module implements SQLAlchemy repository class that is used to access the database.
"""

from fastapi import Depends
from sqlalchemy.exc import IntegrityError

from restaurantservice.database import get_session
from restaurantservice.repositories.errors import DatabaseNotReachableError

from ..models.base_model import BaseModel
from .abstract_reposiitory import AbstractRepository
from .errors import EntityIsNotUnique


class SQLAlchemyRepository(AbstractRepository):
    """A class that encapsulates the logic required to access database."""

    DB_CHECK_QUERY = "SELECT 1"
    _db_session = None

    def __init__(self, db_session=Depends(get_session)):
        self._db_session = db_session

    async def create(self, entity: BaseModel) -> BaseModel:
        self._db_session.add(entity)

        try:
            await self._db_session.commit()
        except IntegrityError as err:
            self._handle_integrity_error(err, entity)

        return entity

    async def ping_db(self):
        """Execute a simple check query to db."""
        try:
            return await self._db_session.execute(self.DB_CHECK_QUERY)
        except Exception:  # pylint: disable=broad-except
            self._handle_db_error()
            print(3)

    @staticmethod
    def _handle_db_error():
        raise DatabaseNotReachableError

    @staticmethod
    def _handle_integrity_error(error, entity):
        for error_arg in error.args:
            if "UNIQUE constraint failed" in error_arg:
                raise EntityIsNotUnique(entity)
