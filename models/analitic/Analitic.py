from sqlalchemy import Column, Integer, String, Text, Float, Boolean, DateTime, Date, Numeric, BigInteger, SmallInteger, ForeignKey
from sqlalchemy.orm import relationship




from datetime import datetime, timezone
from infrastructure.db_core.base import Base as db

class Analitic(db):
    __tablename__ = 'analitic'
    id = Column(Integer, primary_key=True)
    timestamp = Column(
            DateTime, 
            default=datetime.now(timezone.utc)
            )
    period = Column(String(50))
    torg = Column(Numeric(precision=10, scale=2))
    body = Column(Numeric(precision=10, scale=2))
    worker = Column(Numeric(precision=10, scale=2))
    prom = Column(Numeric(precision=10, scale=2))
    orders = Column(Integer)
    rozet = Column(Numeric(precision=10, scale=2))
    google_shop = Column(Numeric(precision=10, scale=2))
    insta = Column(Numeric(precision=10, scale=2))
    profit = Column(Numeric(precision=10, scale=2))
    balance = Column(Numeric(precision=10, scale=2))
    wait = Column(Numeric(precision=10, scale=2))
    stock = Column(Numeric(precision=10, scale=2))
    income = Column(Numeric(precision=10, scale=2))
    inwork = Column(Numeric(precision=10, scale=2))
    salary = Column(Numeric(precision=10, scale=2))
    project_id = Column(Integer, ForeignKey(
        'project.id', name='fk_analitic_project_id'))
