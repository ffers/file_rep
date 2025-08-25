from sqlalchemy import Column, Integer, String, Text, Float, Boolean, DateTime, Date, Numeric, BigInteger, SmallInteger, ForeignKey
from sqlalchemy.orm import relationship
from infrastructure.db_core.base import Base as db


class DeliveryStatus(db):
    id = Column(Integer, primary_key=True)
    code = Column(Integer)
    name = Column(String(50))
    description = Column(String(300))
    delivery_order = relationship("DeliveryOrder", back_populates="delivery_status")