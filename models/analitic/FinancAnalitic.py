from sqlalchemy import Column, Integer, String, Text, Float, Boolean, DateTime, Date, Numeric, BigInteger, SmallInteger, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from infrastructure.db_core.base import Base as db

class FinancAnalitic(db):
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    balance = Column(Float)
    order_quantity = Column(Float)
    rest_start_month = Column(Float)
    expect_start_month = Column(Float)
    expect_payment = Column(Float)
    body = Column(Float)
    product_balance = Column(Float)
    salary = Column(Float)
    debet = Column(Float)
    credit = Column(Float)
    working_money = Column(Float)
    project_id = Column(Integer, ForeignKey(
        'project.id', name='fk_financ_analitic_project_id'))