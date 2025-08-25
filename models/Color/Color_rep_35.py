from sqlalchemy import Column, Integer, String, Text, Float, Boolean, DateTime, Date, Numeric, BigInteger, SmallInteger, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from infrastructure.db_core.base import Base as db

class Colorrep35(db):
    __tablename__ = 'colorrep_35'
    id = Column(Integer, primary_key=True)
    color = Column(Integer, unique=True)
    quantity = Column(Integer)
    project_id = Column(Integer, ForeignKey(
        'project.id', name='fk_colorrep35_project_id'))
