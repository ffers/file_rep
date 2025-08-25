from sqlalchemy import Column, Integer, String, Text, Float, Boolean, DateTime, Date, Numeric, BigInteger, SmallInteger, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from infrastructure.db_core.base import Base as db

class DeliveryOrder(db):
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.now)
    city = Column(String(50), nullable=False)
    city_description = Column(String(50))
    region = Column(String(50))
    area = Column(String(50))
    city_ref = Column(String(50))
    warehouse = Column(String(50))