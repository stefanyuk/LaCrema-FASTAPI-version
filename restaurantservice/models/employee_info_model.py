import sqlalchemy as sqla

from .base_model import BaseModel


class EmployeeInfo(BaseModel):
    """A class to represent attributes of employee_info table in database."""

    __tablename__ = "employee_info"

    employee_info_id = sqla.Column(sqla.String, primary_key=True)
    hire_date = sqla.Column(sqla.Date)
    salary = sqla.Column(sqla.Numeric(10, 3), nullable=False)
    user_id = sqla.Column(
        sqla.ForeignKey("user.user_id", ondelete="CASCADE"), nullable=False
    )
    available_holidays = sqla.Column(sqla.Integer)
