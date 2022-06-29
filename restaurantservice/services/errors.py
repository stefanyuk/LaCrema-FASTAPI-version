"""
This module contains the set of custom errors for application services.
"""


class ServiceBaseError(Exception):
    """Base error class for all service-related errors."""


class AppIsNotHealthyError(ServiceBaseError):
    """Raised in case when application is not healthy."""


class UserAlreadyExists(ServiceBaseError):
    """Raised in case when user with the provided attributes already exists."""

    def __init__(self, user_model, detail, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_model = user_model
        self.detail = detail


class UserDoesNotExist(ServiceBaseError):
    """Raised in case when user with the provided id does not exist."""

    def __init__(self, user_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_id = user_id


class TokenDoesNotExist(ServiceBaseError):
    """Raised in case when token with the provided id does not exist."""

    def __init__(self, token_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.token_id = token_id


class InvalidToken(ServiceBaseError):
    """Raised in case when token is not valid."""
