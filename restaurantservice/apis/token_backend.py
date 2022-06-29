"""
This module implements JWTTokenBackend class, that encapsulates
logic needed for work with the JWT token.
"""

# pylint: disable=line-too-long, raise-missing-from

import abc
import uuid

from jose.exceptions import JWTError

from ..models import Token, User
from ..services.errors import InvalidToken, TokenDoesNotExist, UserDoesNotExist
from ..services.user_service import UserService


class APITokenBackend(abc.ABC):
    """Base backend service implementation for API token operations."""

    @abc.abstractmethod
    def create_api_token(self, user_token: Token) -> str:
        """Set create token interface for all subclasses."""
        pass

    @abc.abstractmethod
    async def get_user_from_token(self, token: str, user_service: UserService) -> User:
        """Set get user from token interface for all subclasses."""
        pass


class JWTTokenBackend(APITokenBackend):
    """Backend service is responsible for API token operations."""

    _algorithm = "HS256"

    def __init__(self, jwt_backend, shared_secret):
        self.jwt = jwt_backend
        self._shared_secret = shared_secret

    def create_api_token(self, user_token: Token) -> str:
        """Create new API token based on the provided data."""
        return self.jwt.encode(
            {"user_id": str(user_token.user_id), "token_id": str(user_token.id)},
            self._shared_secret,
            algorithm=self._algorithm,
        )

    async def get_user_from_token(self, token: str, user_service: UserService) -> User:
        """Return user instance based on the provided token."""
        token_info = self._decode_api_token(token)

        try:
            user = await user_service.get_user(token_info["user_id"], for_update=True)
            await user_service.get_user_token(user, token_info["token_id"])
        except (TokenDoesNotExist, UserDoesNotExist):
            raise InvalidToken

        return user

    def _decode_api_token(self, token: str) -> dict:
        """Decode API token and return it's payload.

        :raises InvalidToken: in case when provided token is not valid
        """
        try:
            payload = self.jwt.decode(token, self._shared_secret, self._algorithm)
            self._verify_payload_claims(payload)
            payload = self._convert_payload_values_to_uuid(payload)
        except (JWTError, ValueError, KeyError):
            raise InvalidToken

        return payload

    @staticmethod
    def _convert_payload_values_to_uuid(payload: dict) -> dict:
        """
        Convert provided payload claims values to UUID format.
        :param payload: payload retrieved from jwt token
        :raises ValueError: in case when any of the claims values is not a valid UUID object
        """
        payload["user_id"] = uuid.UUID(payload["user_id"])
        payload["token_id"] = uuid.UUID(payload["token_id"])
        return payload

    @staticmethod
    def _verify_payload_claims(payload: dict) -> None:
        """Verify whether payload contains required claims."""
        user_id = payload.get("user_id")
        token_id = payload.get("token_id")

        if not (user_id and token_id):
            raise KeyError("Invalid payload claims.")
