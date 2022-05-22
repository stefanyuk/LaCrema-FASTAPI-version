"""
This module initializes FastApi application.
"""

from fastapi import FastAPI

from restaurantservice.apis import healthcheck


def _register_api_handlers(app: FastAPI) -> FastAPI:
    app.include_router(healthcheck.router)
    return app


def create_app() -> FastAPI:
    """Create and return FastAPI application."""
    app = FastAPI()
    app = _register_api_handlers(app)
    return app


app = create_app()
