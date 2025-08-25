from sqlalchemy import Column, Integer, String, Text, Float, Boolean, DateTime, Date, Numeric, BigInteger, SmallInteger, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from infrastructure.db_core.base import Base as db


class Arrival(db):
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    datetime_new = Column(DateTime)
    quantity = Column(Integer)
    body_price = Column(Numeric(precision=8, scale=2))
    total_price = Column(Numeric(precision=8, scale=2))
    product_id = Column(Integer, ForeignKey(
        'products.id', name='fk_arrival_products_id'))
    products = relationship('Products', back_populates='arrival')
    project_id = Column(Integer, ForeignKey(
        'project.id', name='fk_arrival_project_id'))
