"""
This module contains the set of custom errors for application repositories.
"""


class RepositoryBaseError(Exception):
    """Base error class for all repository-related errors."""


class DatabaseNotReachableError(RepositoryBaseError):
    """Raised in case when database is not reachable."""
