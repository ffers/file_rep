from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Text, Float, Boolean, DateTime, Date, Numeric, BigInteger, SmallInteger, ForeignKey
from infrastructure.db_core.base import Base as db

class BalanceV2(db):
    __tablename__ = 'balance_v_2'
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime(timezone.utc()))
    name = Column(String(50))
    total = Column(Numeric(precision=10, scale=2))
    project_id = Column(Integer, ForeignKey(
        'project.id', name='fk_orders_crm_id'), unique=True)
