"""
The module contains a Token class that defines attributes for the token table.
"""

import uuid

import sqlalchemy as sqla
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from .base_model import BaseModel


class Token(BaseModel):
    """The schema used to generate the token table in the database."""

    __tablename__ = "token"

    id = sqla.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = sqla.Column(
        sqla.ForeignKey("user.id", ondelete="CASCADE"), nullable=False
    )
    user = relationship("User", back_populates="tokens", lazy="joined", innerjoin=True)
