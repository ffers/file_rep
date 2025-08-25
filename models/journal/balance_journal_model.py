from sqlalchemy import Column, Integer, String, Text, Float, Boolean, DateTime, Date, Numeric, BigInteger, SmallInteger, ForeignKey
from sqlalchemy.orm import relationship




from datetime import datetime
from infrastructure.db_core.base import Base as db

class BalanceJournal(db):
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    event_date = Column(DateTime)
    desription = Column(String(50))
    total = Column(Numeric(precision=8, scale=2))
    income = Column(Numeric(precision=8, scale=2))
    project_id = Column(Integer, ForeignKey(
        'project.id', name='fk_balance_journal_project_id'))
    project = relationship('Project', backref='balance_journal')
    balance_id = Column(Integer, ForeignKey(
        'balance.id', name='fk_balance_journal_balance_id'))
    balance = relationship('Balance', backref='balance_journal')
    project_id = Column(Integer, ForeignKey(
        'project.id', name='fk_balance_journal_project_id'))