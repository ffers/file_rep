from sqlalchemy import Column, Integer, String, Text, Float, Boolean, DateTime, Date, Numeric, BigInteger, SmallInteger, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from infrastructure.db_core.base import Base as db

class JournalChange(db):
    __tablename__ = 'journal_change'
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    event_date = Column(DateTime)
    status = Column(String(50))
    quantity = Column(Integer)
    body = Column(Numeric(precision=8, scale=2))
    income = Column(Numeric(precision=8, scale=2))
    quantity_stock = Column(Integer)
    product_id = Column(Integer, ForeignKey(
        'product_source.id', name='fk_journal_change_product_source_id'))
    product = relationship('ProductSource', backref='journal_change')
    project_id = Column(Integer, ForeignKey(
        'project.id', name='fk_journal_change_project_id'))