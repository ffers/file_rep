from sqlalchemy import Column, Integer, String, Text, Float, Boolean, DateTime, Date, Numeric, BigInteger, SmallInteger, ForeignKey
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from datetime import datetime
from infrastructure.db_core.base import Base as db

class Manager(db):
    __tablename__ = 'manager'
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    project_id = Column(Integer, ForeignKey(
        'project.id', name='fk_project_id'))
    user_id = Column(Integer, ForeignKey(
        'users.id', name='fk_manager_users_id'), nullable=False)
    # role = relationship('Role', secondary='manager_role', backref='manager')
    project_id = Column(Integer, ForeignKey(
        'project.id', name='fk_manager_project_id'))
