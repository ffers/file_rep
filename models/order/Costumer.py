from sqlalchemy import Column, Integer, String, Text, Float, Boolean, DateTime, Date, Numeric, BigInteger, SmallInteger, ForeignKey
from sqlalchemy.orm import relationship
from infrastructure.db_core.base import Base as db

class Costumer(db):
    __tablename__ = 'costumer'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    second_name = Column(String(50))
    full_name = Column(String(50))
    phone = Column(String(50))
    email = Column(String(50))
    orders = relationship("Orders", back_populates="costumer")
    project_id = Column(Integer, ForeignKey(
        'project.id', name='fk_costumer_project_id'))