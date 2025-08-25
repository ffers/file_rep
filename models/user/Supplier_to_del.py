from sqlalchemy import Column, Integer, String, Text, Float, Boolean, DateTime, Date, Numeric, BigInteger, SmallInteger, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from infrastructure.db_core.base import Base as db


class Supplier(db):
    __tablename__ = 'supplier'
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    project_id = Column(Integer, ForeignKey(
        'project.id', name='fk_project_id'))
    user_id = Column(Integer, ForeignKey(
        'users.id', name='fk_supplier_users_id'), nullable=False)
    user_roles_id =  Column(Integer, ForeignKey(
        'user_roles.id', name='fk_supplier_user_roles_id'), nullable=False)
    # role = relationship('Role', secondary='supplier_role', backref='supplier')

 
