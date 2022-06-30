"""
The module contains a User class that defines attributes for the user table.
"""

import uuid
from datetime import datetime

import sqlalchemy as sqla
from passlib.context import CryptContext
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from .base_model import BaseModel

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(BaseModel):
    """The schema used to generate the user table in the database."""

    __tablename__ = "user"

    id = sqla.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = sqla.Column(sqla.String(255), nullable=False, unique=True)
    password_hash = sqla.Column(sqla.String(255), nullable=False)
    first_name = sqla.Column(sqla.String(255), nullable=False)
    last_name = sqla.Column(sqla.String(255), nullable=False)
    email = sqla.Column(sqla.String(255), nullable=False, unique=True)
    last_login = sqla.Column(sqla.Date, nullable=True)
    registered_on = sqla.Column(sqla.Date, nullable=False, default=datetime.utcnow)
    is_admin = sqla.Column(sqla.Boolean, default=False)
    is_employee = sqla.Column(sqla.Boolean, default=False)
    employee = sqla.orm.relationship(
        "EmployeeInfo",
        backref="user",
        uselist=False,
        cascade="all, delete",
        passive_deletes=True,
    )
    tokens = sqla.orm.relationship(
        "Token",
        back_populates="user",
        cascade="all, delete",
        passive_deletes=True,
        lazy="joined",
    )

    @property
    def password(self):
        raise AttributeError("password is not a readable attribute")

    @password.setter
    def password(self, password):
        self.password_hash = pwd_context.hash(password)

    # def verify_password(self, password):
    #     """Verify whether provided password matches the hash saved in db."""
    #     return verify_password(password, self.password_hash)
