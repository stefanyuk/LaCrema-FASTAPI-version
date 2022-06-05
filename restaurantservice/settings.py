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
    db_connection_string: str = "sqlite+aiosqlite:///test.db"

    class Config:
        """Class representing Pydantic configuration."""

        env_prefix = "la_crema_"


@lru_cache()
def get_settings() -> AppSettings:
    """Return application settings."""
    return AppSettings()
