"""
This module contains AbstractService class to set common interface,
which should be implemented by application services.
"""

import abc

from restaurantservice.repositories.abstract_reposiitory import AbstractRepository


class AbstractService(abc.ABC):
    """Base service class for all services in the system."""

    entity_repository: AbstractRepository

    def __init__(self, entity_repository):
        self.entity_repository = entity_repository
