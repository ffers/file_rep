from sqlalchemy import Column, Integer, String, Text, Float, Boolean, DateTime, Date, Numeric, BigInteger, SmallInteger, ForeignKey
from sqlalchemy.orm import relationship
from infrastructure.db_core.base import Base as db


class Colorrep45(db):
    __tablename__ = 'colorrep45'
    id = Column(Integer, primary_key=True)
    color = Column(Integer, unique=True)
    quantity = Column(Integer)
    project_id = Column(Integer, ForeignKey(
        'project.id', name='fk_colorrep45_project_id'))