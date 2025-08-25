from sqlalchemy import Column, Integer, String, Text, Float, Boolean, DateTime, Date, Numeric, BigInteger, SmallInteger, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from infrastructure.db_core.base import Base as db

class Client(db):
    __tablename__ = 'client'
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    name = Column(String(150))
    lastname = Column(String(150))
    city = Column(String(150))
    warehouse = Column(Integer)
    phone = Column(Integer, unique=True)
    email = Column(String(150), unique=True)
    project_id = Column(Integer, ForeignKey(
        'project.id', name='fk_client2_project_id'))