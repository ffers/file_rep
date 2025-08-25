from sqlalchemy import Column, Integer, String, Text, Float, Boolean, DateTime, Date, Numeric, BigInteger, SmallInteger, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from DTO import ReceiptDTO
from infrastructure.db_core.base import Base as db


class Receipt(db):
    __tablename__ = 'receipt'
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow())
    shift_id = Column(Integer, ForeignKey(
        'shift.id', name='fk_receipt_shift_id'))
    receipt_id = Column(String(255))
    project_id = Column(Integer, ForeignKey(
        'project.id', name='fk_receipt_project_id'))
    
    def __init__(self, d: ReceiptDTO):
        """
        Кастомний конструктор для створення екземпляра UserToken з UserTokenDTO.
        """
        self.shift_id = d.shift_id
        self.receipt_id = d.receipt_id

    def update(self, d: ReceiptDTO):
        self.shift_id = d.shift_id or self.shift_id
        self.receipt_id = d.receipt_id or self.receipt_id
    
