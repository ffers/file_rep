from sqlalchemy import Column, Integer, String, Text, Float, Boolean, DateTime, Date, Numeric, BigInteger, SmallInteger, ForeignKey
from sqlalchemy.orm import relationship
from infrastructure.db_core.base import Base as db

class OrderedProduct(db):
    __tablename__ = 'ordered_product'
    id = Column(Integer, primary_key=True)
    quantity = Column(Integer)
    price = Column(Numeric(precision=8, scale=2))
    order_id = Column(Integer, ForeignKey(
        'orders.id', name='fk_ordered_product_order_id'), nullable=False)
    product_id = Column(Integer, ForeignKey(
        'products.id', name='fk_ordered_product_product_id'))
    products = relationship('Products', back_populates='ordered_product', overlaps="orders,products")
    project_id = Column(Integer, ForeignKey(
        'project.id', name='fk_ordered_product_project_id'))
