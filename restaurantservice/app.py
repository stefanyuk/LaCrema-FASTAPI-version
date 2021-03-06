"""
This module initializes FastApi application.
"""
import uvicorn
from fastapi import FastAPI

from restaurantservice.apis import healthcheck, user_api
from restaurantservice.database import create_all_tables


def _register_api_handlers(app: FastAPI) -> FastAPI:
    app.include_router(healthcheck.router)
    app.include_router(user_api.router)
    return app


def create_app() -> FastAPI:
    """Create and return FastAPI application."""
    app = FastAPI()
    app = _register_api_handlers(app)
    return app


app = create_app()


@app.on_event("startup")
async def startup():
    await create_all_tables()


if __name__ == "__main__":
    uvicorn.run(app, port=8080)
