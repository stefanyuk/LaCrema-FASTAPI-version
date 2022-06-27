"""
This module collects class and function needed to setup application settings.

Functions:
    get_settings () -> AppSettings
"""


from functools import lru_cache

from pydantic import BaseSettings, Field


class AppSettings(BaseSettings):
    """Class representing configuration for FastApi application."""

    host = Field("127.0.0.1")
    port = Field("8080")
    db_connection_string: str = "postgresql+asyncpg://stefa:1234@localhost:5432/stefa"

    class Config:
        """Class representing Pydantic configuration."""


@lru_cache()
def get_settings() -> AppSettings:
    """Return application settings."""
    return AppSettings()
