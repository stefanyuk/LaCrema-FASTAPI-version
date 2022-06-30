"""
This module implements API controllers to perform user related tasks.
"""

from uuid import UUID

from fastapi import APIRouter, Depends
from pydantic import BaseModel, EmailStr, Field, Required
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_session
from ..models import User
from ..repositories.sqlalchemy_repository import SQLAlchemyRepository
from ..services.errors import UserAlreadyExists, UserDoesNotExist
from ..services.user_service import UserService
from .auth import authenticated_admin_user, authenticated_user
from .errors import ErrorResponse, build_error_response
from .utils import TokenGetter, UserGetter

router = APIRouter(prefix="/v1/users", tags=["user"])
me_router = APIRouter(prefix="/v1/users/me", tags=["me"])


class TokenId(BaseModel):
    id: UUID


class TokenBase(TokenId):
    """Schema that represents base token data."""

    access_token: str = Field(..., alias="access-token")

    class Config:
        orm_mode = True
        getter_dict = TokenGetter


class EmbedTokenOut(BaseModel):
    token: TokenBase

    class Config:
        orm_mode = True
        getter_dict = TokenGetter


class UserId(BaseModel):
    id: UUID


class UserBase(BaseModel):
    """Schema that represents base user data."""

    username: str = Field(Required, max_length=255)
    first_name: str = Field(Required, max_length=255)
    last_name: str = Field(Required, max_length=255)
    email: EmailStr


class UserExtended(UserBase, UserId):
    """Schema that represents extended user data."""

    is_admin: bool
    is_employee: bool

    class Config:
        orm_mode = True


class ExistingUser(UserBase, UserId):
    """Schema that represents minimal set of user data."""

    class Config:
        orm_mode = True


class UserIn(UserBase):
    """Schema that represents in bound extended user data."""

    password: str = Field(Required, max_length=255)
    is_admin: bool = None
    is_employee: bool = None


class EmbedUserExtendedOut(BaseModel):
    user: UserExtended

    class Config:
        orm_mode = True
        getter_dict = UserGetter


class EmbedExistingUserOut(BaseModel):
    user: ExistingUser

    class Config:
        orm_mode = True
        getter_dict = UserGetter


class UpdateExistingUser(BaseModel):
    """Schema to obtain minimal set of user data for update."""

    username: str = Field(None, max_length=255)
    password: str = Field(None, max_length=255)
    first_name: str = Field(None, max_length=255)
    last_name: str = Field(None, max_length=255)
    email: EmailStr = None


class UpdateExtendedUser(UpdateExistingUser):
    """Schema to obtain extended user data for update."""

    is_admin: bool = None
    is_employee: bool = None


class UserCollectionOut(BaseModel):
    users: list[EmbedUserExtendedOut]


def serialize_user_collection(users_list: list):
    """Serialize collection of users."""
    return UserCollectionOut(
        users=[EmbedUserExtendedOut.from_orm(user) for user in users_list]
    )


@me_router.get("/", response_model=EmbedExistingUserOut, status_code=200)
async def get_current_user_info(user: User = Depends(authenticated_user)):
    """Return information about currently authenticated user."""
    return user


@me_router.patch(
    "/",
    response_model=EmbedExistingUserOut,
    status_code=200,
    responses={404: {"model": ErrorResponse}},
)
async def update_current_user_info(
    user_payload: UpdateExistingUser,
    user: User = Depends(authenticated_user),
    db_session: AsyncSession = Depends(get_session),
):
    """Return information about currently authenticated user."""
    repo = SQLAlchemyRepository(db_session)
    user_srv = UserService(repo)

    try:
        await user_srv.update_user_info(user, **user_payload.dict())
    except UserAlreadyExists as err:
        return build_error_response(f"{err.detail}", 400)

    return user


@router.post(
    "/",
    response_model=EmbedUserExtendedOut,
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
    user_srv = UserService(repo)

    try:
        new_user = await user_srv.new_user(**user_payload.dict())
    except UserAlreadyExists as err:
        return build_error_response(f"{err.detail}", 400)

    return new_user


@router.get(
    "/{user_id}",
    response_model=EmbedUserExtendedOut,
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
    user_srv = UserService(repo)

    try:
        user = await user_srv.get_user(user_id)
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
    user_srv = UserService(repo)

    try:
        user = await user_srv.get_user(user_id)
    except UserDoesNotExist:
        return build_error_response(f"User with id {user_id} does not exist.", code=404)

    token = await user_srv.create_user_token(user)
    return token


@router.patch(
    "/{user_id}",
    response_model=EmbedUserExtendedOut,
    status_code=200,
    responses={404: {"model": ErrorResponse}, 400: {"model": ErrorResponse}},
    dependencies=[Depends(authenticated_admin_user)],
)
async def update_user(
    user_id: UUID,
    user_payload: UpdateExtendedUser,
    db_session: AsyncSession = Depends(get_session),
):
    """Update user information."""
    repo = SQLAlchemyRepository(db_session)
    user_srv = UserService(repo)

    try:
        user = await user_srv.get_user(user_id, for_update=True)
    except UserDoesNotExist:
        return build_error_response(f"User with id {user_id} does not exist.", code=404)

    try:
        await user_srv.update_user_info(user, **user_payload.dict())
    except UserAlreadyExists as err:
        return build_error_response(f"{err.detail}", 400)

    return user


@router.get(
    "/",
    response_model=UserCollectionOut,
    status_code=200,
    dependencies=[Depends(authenticated_admin_user)],
)
async def get_users_list(db_session: AsyncSession = Depends(get_session)):
    """Return list of all users."""
    repo = SQLAlchemyRepository(db_session)
    user_srv = UserService(repo)
    users_list = await user_srv.find_users()
    return serialize_user_collection(users_list)
