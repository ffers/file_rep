from sqlalchemy import Column, Integer, String, Text, Float, Boolean, DateTime, Date, Numeric, BigInteger, SmallInteger, ForeignKey
from sqlalchemy.orm import relationship
from infrastructure.db_core.base import Base as db

class DeliveryOrder(db):
    id = Column(Integer, primary_key=True)
    ref_ttn = Column(String(50), nullable=False)
    number_ttn = Column(String(50))
    ref_registr = Column(String(50))
    number_registr = Column(String(50))

    status_id = Column(Integer, ForeignKey(
        'delivery_status.id', name='fk_delivery_order_status_id'))
    order_id = Column(Integer, ForeignKey(
        'orders.id', name='fk_delivery_order_order_id'), nullable=False, unique=True)

    delivery_status = relationship("DeliveryStatus", back_populates="delivery_order")
    orders = relationship("Orders", back_populates="delivery_order", passive_deletes=True)
    project_id = Column(Integer, ForeignKey(
        'project.id', name='fk_delivery_order_project_id'))