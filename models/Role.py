from sqlalchemy import Column, Integer, String, Text, Float, Boolean, DateTime, Date, Numeric, BigInteger, SmallInteger, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import relationship
from infrastructure.db_core.base import Base as db


class Role(db):
    id = Column(Integer, primary_key=True)
    name = Column(String(80), unique=True, nullable=False)
    user_roles = relationship(
        "UserRoles",
        back_populates="role",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

 