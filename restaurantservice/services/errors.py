"""
This module contains the set of custom errors for application services.
"""


class ServiceBaseError(Exception):
    """Base error class for all service-related errors."""


class AppIsNotHealthyError(ServiceBaseError):
    """Raised in case when application is not healthy."""


class UserAlreadyExists(ServiceBaseError):
    """Raised in case when user with the provided attributes already exists."""

    def __init__(self, user_model, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_model = user_model
