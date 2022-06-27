"""
This module contains common error handlers.
"""

from fastapi.responses import JSONResponse
from pydantic import BaseModel  # pylint: disable=no-name-in-module


class ErrorDetails(BaseModel):
    """Base error class.

    Provides an ability to specify error details inside the message
    field as well as the error code in the code field.
    """

    message: str
    code: int


class ErrorResponse(BaseModel):
    """API error response."""

    error: ErrorDetails


def build_error_response(message, code):
    """
    Build and return API error response object.

    :param message: str, error message
    :param code: int, HTTP error code
    """

    return JSONResponse(
        status_code=code, content={"error": {"message": message, "code": code}}
    )
