from sqlalchemy import Column, Integer, String, Text, Float, Boolean, DateTime, Date, Numeric, BigInteger, SmallInteger, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from DTO import ReceiptDTO
from infrastructure.db_core.base import Base as db
 

class Shift(db):
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow())
    shift_id = Column(String(255))
    open = Column(DateTime)
    closed = Column(DateTime)
    cash_id = Column(Integer, ForeignKey(
        'cash.id', name='fk_shift_cash_id'))
    receipts =  relationship('Receipt', backref='shift')
    project_id = Column(Integer, ForeignKey(
        'project.id', name='fk_shift_project_id'))

    def __init__(self, d: ReceiptDTO):
        self.shifd_id = d.shift_id
        self.open = d.open
        self.closed = d.closed

    def update(self, d: ReceiptDTO):
        self.shifd_id = d.shift_id or self.shifd_id
        self.open = d.open or self.open
        self.closed = d.closed or self.closed 