"""
The module contains helper functions and utilities needed for API.
"""

from typing import Any

from passlib.context import CryptContext
from pydantic.utils import GetterDict

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


class UserGetter(GetterDict):
    """A class for serializing User model."""

    def get(self, key: Any, default: Any = None) -> Any:
        """Provides a dictionary-like interface to serialize User model."""
        if key == "user":
            return self._obj
        return super().get(key, default)
