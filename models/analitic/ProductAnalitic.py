from sqlalchemy import Column, Integer, String, Text, Float, Boolean, DateTime, Date, Numeric, BigInteger, SmallInteger, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from infrastructure.db_core.base import Base as db

class ProductAnalitic(db):
    __tablename__ = 'product_analitic'
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    quantity_sale = Column(Integer)
    money_in_product = Column(Numeric(precision=8, scale=2))
    quantity_stok = Column(Integer)
    money_in_sale = Column(Numeric(precision=8, scale=2))
    product_id = Column(Integer, ForeignKey(
        'products.id', name='fk_product_analitic_products_id'), unique=True)
    products = relationship('Products', back_populates='product_analitic')
    project_id = Column(Integer, ForeignKey(
        'project.id', name='fk_product_analitic_project_id'))
