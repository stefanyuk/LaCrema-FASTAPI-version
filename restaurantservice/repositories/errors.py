"""
This module contains the set of custom errors for application repositories.
"""

from ..models.base_model import BaseModel


class RepositoryBaseError(Exception):
    """Base error class for all repository-related errors."""


class DatabaseNotReachableError(RepositoryBaseError):
    """Raised in case when database is not reachable."""


class EntityIsNotUnique(RepositoryBaseError):
    """Raised when try to create entity that is not unique."""

    entity: BaseModel

    def __init__(self, entity, detail, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.entity = entity
        self.detail = detail


class EntityDoesNotExist(RepositoryBaseError):
    """Raised when try to retrieve entity that does not exist."""

    def __init__(self, detail, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.detail = detail
