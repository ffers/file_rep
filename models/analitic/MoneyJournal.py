from sqlalchemy import Column, Integer, String, Text, Float, Boolean, DateTime, Date, Numeric, BigInteger, SmallInteger, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from infrastructure.db_core.base import Base as db

class MoneyJournal(db):
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.now(timezone.utc))
    event_date = Column(DateTime)
    description = Column(String(50))
    movement = Column(Numeric(precision=8, scale=2))
    total = Column(Numeric(precision=8, scale=2))
    project_id = Column(Integer, ForeignKey(
        'project.id', name='fk_money_journal_project_id'))