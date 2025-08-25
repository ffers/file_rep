from sqlalchemy import Column, Integer, String, Text, Float, Boolean, DateTime, Date, Numeric, BigInteger, SmallInteger, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from infrastructure.db_core.base import Base as db


class Products(db):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    article = Column(String(150), unique=True)
    product_name = Column(String(150))
    name_official = Column(String(150))
    description = Column(String(300))
    photo_1 = Column(String(300))
    photo_2 = Column(String(300))
    photo_3 = Column(String(300))
    photo_4 = Column(String(300))
    photo_5 = Column(String(300))
    photo_6 = Column(String(300))
    photo_7 = Column(String(300))
    price = Column(Numeric(precision=8, scale=2))
    opt_1 = Column(Numeric(precision=8, scale=2))
    opt_2 = Column(Numeric(precision=8, scale=2))
    opt_3 = Column(Numeric(precision=8, scale=2))
    opt_4 = Column(Numeric(precision=8, scale=2))
    opt_5 = Column(Numeric(precision=8, scale=2))
    opt_6 = Column(Numeric(precision=8, scale=2))
    opt_7 = Column(Numeric(precision=8, scale=2))
    opt_8 = Column(Numeric(precision=8, scale=2))
    opt_9 = Column(Numeric(precision=8, scale=2))
    opt_10 = Column(Numeric(precision=8, scale=2))
    opt_11 = Column(Numeric(precision=8, scale=2))
    opt_12 = Column(Numeric(precision=8, scale=2))
    quantity = Column(Integer)
    body_product_price = Column(Numeric(precision=8, scale=2))
    orders = relationship('Orders', secondary='ordered_product', overlaps='ordered_product,orders,products')
    ordered_product = relationship('OrderedProduct', back_populates='products')
    product_analitic = relationship('ProductAnalitic', back_populates='products')
    arrival = relationship('Arrival', back_populates='products')
    product_relate = relationship('ProductRelate', back_populates='products')
    project_id = Column(Integer, ForeignKey(
        'project.id', name='fk_products_project_id'))
    