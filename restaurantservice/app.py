"""
This module initializes FastApi application.
"""

from fastapi import FastAPI


def _register_api_handlers(app: FastAPI) -> FastAPI:
    return app


def create_app() -> FastAPI:
    """Create and return FastAPI application."""
    app = FastAPI()
    app = _register_api_handlers(app)
    return app


app = create_app()
