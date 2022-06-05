"""
This module implements API controllers to perform user related tasks.
"""

from fastapi import APIRouter, Depends
from pydantic import BaseModel, EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_session
from ..repositories.sqlalchemy_repository import SQLAlchemyRepository
from ..services.errors import UserAlreadyExists
from ..services.user_service import UserService

router = APIRouter(prefix="/users")


class UserIn(BaseModel):
    """A class to represent in bound user data."""

    username: str
    password: str
    first_name: str
    last_name: str
    email: EmailStr
    is_admin: bool
    is_employee: bool


class UserOut(UserIn, BaseModel):
    """A class to represent out bound user data."""

    user_id: str
    password: str = None

    class Config:
        """A class to represent Pydantic configuration"""

        fields = {"password": {"exclude": True}}
        orm_mode = True


@router.post("/")
async def create_user(user: UserIn, db_session: AsyncSession = Depends(get_session)):
    """Receive user data and create new user entity."""
    repo = SQLAlchemyRepository(db_session)
    srv = UserService(repo)

    try:
        new_user = await srv.new_user(**user.dict())
    except UserAlreadyExists as err:
        raise Exception("User already exists")

    return UserOut.from_orm(new_user)
