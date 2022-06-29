"""
The module contains helper functions and utilities needed for API.
"""

from typing import Any

from jose import jwt
from pydantic.utils import GetterDict

from ..apis.token_backend import JWTTokenBackend
from ..settings import get_settings


class UserGetter(GetterDict):
    """A class for serializing User model."""

    def get(self, key: Any, default: Any = None) -> Any:
        """Provides a dictionary-like interface to serialize User model."""
        if key == "user":
            return self._obj
        return super().get(key, default)


class TokenGetter(GetterDict):
    """A class for serializing Token model."""

    def get(self, key: Any, default: Any = None) -> Any:
        """Provides a dictionary-like interface to serialize Token model."""
        if key == "access-token":
            jwt_backend = JWTTokenBackend(jwt, get_settings().secret_key)
            return jwt_backend.create_api_token(self._obj)
        if key == "token":
            return self._obj
        return super().get(key, default)
