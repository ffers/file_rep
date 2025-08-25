from sqlalchemy import Column, Integer, String, Text, Float, Boolean, DateTime, Date, Numeric, BigInteger, SmallInteger, ForeignKey
from sqlalchemy.orm import relationship
from infrastructure.db_core.base import Base as db


class DeliveryMethod(db):
    __tablename__ = 'delivery_method'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    description = Column(String(50))
    orders = relationship("Orders", back_populates="delivery_method")


#  id |         name         | description
# ----+----------------------+-------------
#   1 | Нова Пошта           |
#   3 | Укрпошта             |
#   5 | Самовивіз            |
#   4 | Meest                |
#   2 | Точка видачі Rozetka |