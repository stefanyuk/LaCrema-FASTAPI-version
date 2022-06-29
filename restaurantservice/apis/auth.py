"""
This module contains function needed for securing application with the help of JWT API token.
"""


from datetime import datetime

from fastapi import Depends
from fastapi.exceptions import HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt

from ..database import AsyncSession, get_session
from ..models import User
from ..repositories.sqlalchemy_repository import SQLAlchemyRepository
from ..services.errors import InvalidToken
from ..services.user_service import UserService
from ..settings import AppSettings, get_settings
from .token_backend import JWTTokenBackend


async def authenticated_user(
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
    db_session: AsyncSession = Depends(get_session),
    settings: AppSettings = Depends(get_settings),
):
    """Protect API endpoints with JWT token authentication."""
    repo = SQLAlchemyRepository(db_session)
    srv = UserService(repo)
    jwt_backend = JWTTokenBackend(jwt, settings.secret_key)

    try:
        user = await jwt_backend.get_user_from_token(credentials.credentials, srv)
    except InvalidToken:
        raise HTTPException(  # pylint: disable=raise-missing-from
            status_code=403, detail="Token is not valid."
        )

    await srv.update_user_last_login_time(user, new_last_login_time=datetime.utcnow())

    return user


async def authenticated_admin_user(user: User = Depends(authenticated_user)):
    """Protect API endpoints which should be used only by admins."""
    if not user.is_admin:
        raise HTTPException(  # pylint: disable=raise-missing-from
            status_code=403, detail="You don't have permission to access this resource."
        )

    return user
