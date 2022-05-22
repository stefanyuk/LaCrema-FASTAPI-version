"""
This module contains the set of custom errors for application services.
"""


class ServiceBaseError(Exception):
    """Base error class for all service-related errors."""


class AppIsNotHealthyError(ServiceBaseError):
    """Raised in case when application is not healthy."""
