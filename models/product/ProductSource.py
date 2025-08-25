from sqlalchemy import Column, Integer, String, Text, Float, Boolean, DateTime, Date, Numeric, BigInteger, SmallInteger, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from infrastructure.db_core.base import Base as db

class ProductSource(db):
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    article = Column(String(50), unique=True)
    name = Column(String(150))
    quantity = Column(Integer)
    price = Column(Numeric(precision=8, scale=2))
    money = Column(Numeric(precision=10, scale=2))
    product_relate = relationship("ProductRelate", back_populates="product_source")
    source_difference = relationship('SourceDifference', back_populates='product_source')
    project_id = Column(Integer, ForeignKey(
        'project.id', name='fk_product_source_project_id'))



