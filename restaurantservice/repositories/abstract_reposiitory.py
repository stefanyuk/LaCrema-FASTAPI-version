"""
This module contains AbstractRepository class, that creates formal interface
for it's derived classes.
"""

import abc

from restaurantservice.models.base_model import BaseModel


class AbstractRepository(abc.ABC):
    """A class to represent base implementation for it's subclasses."""

    @abc.abstractmethod
    async def create(self, entity: BaseModel) -> BaseModel:
        """Set create entity interface for all subclasses."""
        pass
