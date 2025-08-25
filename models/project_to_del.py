from sqlalchemy import Column, Integer, String, Text, Float, Boolean, DateTime, Date, Numeric, BigInteger, SmallInteger, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from infrastructure.db_core.base import Base as db


class Project(db):
    __tablename__ = 'project'
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    timestamp = Column(DateTime, default=datetime.now(datetime.timezone.utc))
    user_id = Column(Integer, ForeignKey(
        'users.id', name='fk_project_user_id'), nullable=False)
