"""
This module implements SQLAlchemy repository class that is used to access the database.
"""

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.exc import IntegrityError, NoResultFound

from ..database import get_session
from ..models.base_model import BaseModel
from .abstract_reposiitory import AbstractRepository
from .errors import DatabaseNotReachableError, EntityDoesNotExist, EntityIsNotUnique


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

    async def get_by_id(self, entity_model: BaseModel, entity_id: int):
        stmt = select(entity_model).where(entity_model.id == entity_id)
        query = await self._db_session.execute(stmt)
        return self._extract_one_entity(query)

    def _extract_one_entity(self, query_result: Result):
        try:
            entity = query_result.scalar_one()
        except NoResultFound as err:
            self._handle_no_result_found_error(err)

        return entity

    async def ping_db(self):
        """Execute a simple check query to db."""
        try:
            return await self._db_session.execute(self.DB_CHECK_QUERY)
        except Exception:  # pylint: disable=broad-except
            self._handle_db_error()

    @staticmethod
    def _handle_db_error():
        raise DatabaseNotReachableError

    def _handle_integrity_error(self, error, entity):
        for error_arg in error.args:
            if "duplicate key value violates unique constraint" in error_arg:
                error_detail = self._find_error_detail(error_arg)
                raise EntityIsNotUnique(entity, error_detail)

    def _handle_no_result_found_error(self, error):
        error_args = error.args[0]
        error_detail = self._find_error_detail(error_args)
        raise EntityDoesNotExist(detail=error_detail)

    @staticmethod
    def _find_error_detail(error_argument):
        return error_argument[error_argument.find("Key") :]
