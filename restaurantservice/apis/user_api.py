"""
This module implements API controllers to perform user related tasks.
"""

from uuid import UUID

from fastapi import APIRouter, Depends
from pydantic import BaseModel, EmailStr, Field, Required
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_session
from ..repositories.sqlalchemy_repository import SQLAlchemyRepository
from ..services.errors import UserAlreadyExists, UserDoesNotExist
from ..services.user_service import UserService
from .auth import authenticated_admin_user
from .errors import ErrorResponse, build_error_response
from .utils import TokenGetter, UserGetter

router = APIRouter(prefix="/users")


class Token(BaseModel):
    id: UUID
    access_token: str = Field(..., alias="access-token")

    class Config:
        orm_mode = True
        getter_dict = TokenGetter


class EmbedTokenOut(BaseModel):
    token: Token

    class Config:
        orm_mode = True
        getter_dict = TokenGetter


class UserIn(BaseModel):
    """A class to represent in bound user data."""

    username: str = Field(Required, max_length=255)
    password: str = Field(Required, max_length=255)
    first_name: str = Field(Required, max_length=255)
    last_name: str = Field(Required, max_length=255)
    email: EmailStr
    is_admin: bool
    is_employee: bool


class UserOut(UserIn):
    """A class to represent out bound user data."""

    id: UUID
    password: str = None

    class Config:
        orm_mode = True
        fields = {"password": {"exclude": True}}


class EmbedUserOut(BaseModel):
    user: UserOut

    class Config:
        orm_mode = True
        getter_dict = UserGetter


@router.post(
    "/",
    response_model=EmbedUserOut,
    status_code=201,
    responses={400: {"model": ErrorResponse}},
    dependencies=[Depends(authenticated_admin_user)],
)
async def create_user(
    user_payload: UserIn,
    db_session: AsyncSession = Depends(get_session),
):
    """Receive user data and create new user entity."""
    repo = SQLAlchemyRepository(db_session)
    srv = UserService(repo)

    try:
        new_user = await srv.new_user(**user_payload.dict())
    except UserAlreadyExists as err:
        return build_error_response(f"{err.detail}", 400)

    return new_user


@router.get(
    "/{user_id}",
    response_model=EmbedUserOut,
    status_code=200,
    responses={404: {"model": ErrorResponse}},
    dependencies=[Depends(authenticated_admin_user)],
)
async def get_user_info(user_id: UUID, db_session: AsyncSession = Depends(get_session)):
    """
    Return information about user.
    :param user_id: uuid, unique user identifier
    :param db_session: asynchronous database session
    """
    repo = SQLAlchemyRepository(db_session)
    srv = UserService(repo)

    try:
        user = await srv.get_user(user_id)
    except UserDoesNotExist:
        return build_error_response(f"User with id {user_id} does not exist.", code=404)

    return user


@router.post(
    "/{user_id}/token",
    response_model=EmbedTokenOut,
    status_code=201,
    responses={404: {"model": ErrorResponse}},
    dependencies=[Depends(authenticated_admin_user)],
)
async def create_user_token(
    user_id: UUID, db_session: AsyncSession = Depends(get_session)
):
    """
    Create and return a new user token.
    :param user_id: uuid, unique user identifier
    :param db_session: asynchronous database session
    """
    repo = SQLAlchemyRepository(db_session)
    srv = UserService(repo)

    try:
        user = await srv.get_user(user_id)
    except UserDoesNotExist:
        return build_error_response(f"User with id {user_id} does not exist.", code=404)

    token = await srv.create_user_token(user)
    return token
