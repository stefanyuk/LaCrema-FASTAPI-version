"""
The module contains an EmployeeInfo class that defines attributes for the employee_info table.
"""

import uuid

import sqlalchemy as sqla
from sqlalchemy.dialects.postgresql import UUID

from .base_model import BaseModel


class EmployeeInfo(BaseModel):
    """The schema used to generate the employee_info table in the database."""

    __tablename__ = "employee_info"

    id = sqla.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    hire_date = sqla.Column(sqla.Date)
    salary = sqla.Column(sqla.Numeric(10, 3), nullable=False)
    role = sqla.Column(sqla.String(255), nullable=False)
    user_id = sqla.Column(
        sqla.ForeignKey("user.id", ondelete="CASCADE"), nullable=False
    )
    available_holidays = sqla.Column(sqla.Integer)
