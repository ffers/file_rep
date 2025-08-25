from sqlalchemy import Column, Integer, String, Text, Float, Boolean, DateTime, Date, Numeric, BigInteger, SmallInteger, ForeignKey
from sqlalchemy.orm import relationship
from infrastructure.db_core.base import Base as db


class TelegramOrdered(db):
    __tablename__ = 'telegram_ordered'
    id = Column(Integer, primary_key=True)
    text = Column(String(4096))
    confirmed_address_tg = relationship('ConfirmedAddressTg', backref='telegram_ordered', cascade='all, delete-orphan')
    np_address_tg = relationship('NpAddressTg', backref='telegram_ordered', cascade='all, delete-orphan')
    rozetka_address_tg = relationship('RozetkaAddressTg', backref='telegram_ordered', cascade='all, delete-orphan')
    ukr_address_tg = relationship('UkrAddressTg', backref='telegram_ordered', cascade='all, delete-orphan')
    order_id = Column(Integer, ForeignKey(
        'orders.id', name='fk_ordered_telegram_order_id'), nullable=False)
    project_id = Column(Integer, ForeignKey(
        'project.id', name='fk_analitic_project_id'))