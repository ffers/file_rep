from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, Float, Boolean, DateTime, Date, Numeric, BigInteger, SmallInteger, ForeignKey
from infrastructure.db_core.base import Base as db

class Balance(db):
    __tablename__ = 'balance'
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    balance = Column(Numeric(precision=10, scale=2))
    wait = Column(Numeric(precision=10, scale=2))
    stock = Column(Numeric(precision=10, scale=2))
    inwork = Column(Numeric(precision=10, scale=2))
    salary = Column(Numeric(precision=10, scale=2))
    rozetka_pay = Column(Numeric(precision=10, scale=2))
    nova_pay = Column(Numeric(precision=10, scale=2))
    project_id = Column(Integer, ForeignKey(
        'project.id', name='fk_orders_crm_id'), unique=True)
