"""
This module implements health check API controller to handle application health status related task.
"""

from fastapi import APIRouter, Depends, Response, status

from ..database import AsyncSession, get_session
from ..repositories.sqlalchemy_repository import SQLAlchemyRepository
from ..services.app_health_service import AppHealthService
from ..services.errors import AppIsNotHealthyError

router = APIRouter()


@router.get("/health")
async def check_health(db_session: AsyncSession = Depends(get_session)):
    """Return API health status."""
    repo = SQLAlchemyRepository(db_session)
    app_health_srv = AppHealthService(repo)

    try:
        await app_health_srv.is_app_healthy()
    except AppIsNotHealthyError:
        return Response(status_code=status.HTTP_503_SERVICE_UNAVAILABLE)

    return Response(status_code=status.HTTP_200_OK)
