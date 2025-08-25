from sqlalchemy import Column, Integer, String, Text, Float, Boolean, DateTime, Date, Numeric, BigInteger, SmallInteger, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from infrastructure.db_core.base import Base as db


class Drop(db):
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    project_id = Column(Integer, ForeignKey(
        'project.id', name='fk_drop_project_id'))
    user_id = Column(Integer, ForeignKey(
        'users.id', name='fk_drop_user_id'), nullable=False)
    # role = relationship('Role', secondary='drop_role', backref='drop')
