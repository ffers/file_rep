from sqlalchemy import Column, Integer, String, Text, Float, Boolean, DateTime, Date, Numeric, BigInteger, SmallInteger, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from sqlalchemy.orm import relationship
from infrastructure.db_core.base import Base as db


class Project(db):
    __tablename__ = 'project'
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    name = Column(String(150))
    user_id = Column(Integer, ForeignKey( 
        'users.id', name='fk_project_users_id'), nullable=False)  
    user_roles = relationship(
        "UserRoles",
        back_populates="project",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )