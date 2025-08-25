from sqlalchemy import Column, Integer, String, Text, Float, Boolean, DateTime, Date, Numeric, BigInteger, SmallInteger, ForeignKey
from sqlalchemy.orm import relationship
from infrastructure.db_core.base import Base as db

class ConfirmedAddressTg(db):
    __tablename__ = 'confirmed_address_tg'
    id = Column(Integer, primary_key=True)
    message_id = Column(Integer)
    chat_id = Column(BigInteger)
    tg_ord_id = Column(Integer, ForeignKey(
        'telegram_ordered.id', name='fk_telegram_ordered_conf_addr_tg_id'), nullable=False)
