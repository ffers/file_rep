from sqlalchemy import Column, Integer, String, Text, Float, Boolean, DateTime, Date, Numeric, BigInteger, SmallInteger, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from DTO import ReceiptDTO
from infrastructure.db_core.base import Base as db
 

class Cash(db):
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow())
    cash_id = Column(String(255))
    fiscal_number = Column(String(255))
    name = Column(String(255))
    shifts =  relationship('Shift', backref='cash')
    project_id = Column(Integer, ForeignKey(
        'project.id', name='fk_cash_project_id'))

    def __init__(self, d: ReceiptDTO):
        self.cash_id = d.cash_id
        self.fiscal_number = d.fiscal_number
        self.name = d.name

    def update(self, d: ReceiptDTO):
        self.cash_id = d.cash_id or self.cash_id
        self.fiscal_number = d.fiscal_number or self.fiscal_number
        self.name = d.name or self.name