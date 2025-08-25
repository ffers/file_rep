from sqlalchemy import Column, Integer, String, Text, Float, Boolean, DateTime, Date, Numeric, BigInteger, SmallInteger, ForeignKey
from sqlalchemy.orm import relationship
from infrastructure.db_core.base import Base as db


class OrderItems(db):
    __tablename__ = 'order_items'
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    orders_id = Column(Integer, ForeignKey(
        'orders.id', name='fk_order_items_order_id', ondelete="CASCADE"), nullable=False)
    project_id = Column(Integer, ForeignKey(
        'project.id', name='fk_order_items_project_id'))
