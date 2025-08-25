from sqlalchemy import Column, Integer, String, Text, Float, Boolean, DateTime, Date, Numeric, BigInteger, SmallInteger, ForeignKey
from sqlalchemy.orm import relationship
from infrastructure.db_core.base import Base as db


class Store(db):
    __tablename__ = 'store'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    api = Column(String(50))
    token = Column(String(255))
    # store_crm_token = Column(String(255))
    # marketplace_token = Column(String(255))
    token_market = Column(String(255))
    orders = relationship("Orders", back_populates="store")
    project_id = Column(Integer, ForeignKey(
        'project.id', name='fk_store_project_id'))