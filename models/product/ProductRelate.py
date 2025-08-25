from sqlalchemy import Column, Integer, String, Text, Float, Boolean, DateTime, Date, Numeric, BigInteger, SmallInteger, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from infrastructure.db_core.base import Base as db


class ProductRelate(db):
    __tablename__ = 'product_relate'
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    article = Column(String(50)) # сейчас не используеться
    name = Column(String(150))
    quantity = Column(Integer)
    product_id = Column(Integer, ForeignKey(
        'products.id', name='fk_product_relate_products_id'), nullable=False)
    products = relationship('Products', back_populates='product_relate')
    product_source_id = Column(Integer, ForeignKey(
        'product_source.id', name='fk_product_relate_product_source_id'))
    product_source = relationship("ProductSource", back_populates="product_relate")
    project_id = Column(Integer, ForeignKey(
        'project.id', name='fk_product_relate_project_id'))
