from datetime import datetime

import sqlalchemy as sqla
from sqlalchemy.orm import relationship

from ..apis.utils import get_password_hash, verify_password
from .base_model import BaseModel


class User(BaseModel):
    """A class to represent attributes of user table in database."""

    __tablename__ = "user"

    user_id = sqla.Column(sqla.Integer, primary_key=True)
    username = sqla.Column(sqla.String(255), nullable=False, unique=True)
    password_hash = sqla.Column(sqla.String(255), nullable=False)
    first_name = sqla.Column(sqla.String(255), nullable=False)
    last_name = sqla.Column(sqla.String(255), nullable=False)
    email = sqla.Column(sqla.String(255), nullable=False, unique=True)
    last_login_date = sqla.Column(sqla.Date)
    registered_on = sqla.Column(sqla.Date, nullable=False, default=datetime.utcnow())
    is_admin = sqla.Column(sqla.Boolean, nullable=False)
    is_employee = sqla.Column(sqla.Boolean, nullable=False)
    employee = relationship(
        "EmployeeInfo",
        backref="user",
        uselist=False,
        cascade="all, delete",
        passive_deletes=True,
    )

    @property
    def password_2(self):
        raise AttributeError("password is not a readable attribute")

    @password_2.setter
    def password_2(self, password):
        self.password_hash = get_password_hash(password)

    def verify_password_2(self, password):
        """Verify whether provided password matches the hash saved in db."""
        return verify_password(password, self.password_hash)
