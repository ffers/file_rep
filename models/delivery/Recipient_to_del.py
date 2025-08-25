from sqlalchemy import Column, Integer, String, Text, Float, Boolean, DateTime, Date, Numeric, BigInteger, SmallInteger, ForeignKey
from sqlalchemy.orm import relationship
from infrastructure.db_core.base import Base as db

class Recipient(db):
    id = Column(Integer, primary_key=True)
    recipient_title = Column(String(50))
    recipient_first_name = Column(String(50))
    recipient_last_name = Column(String(50))
    recipient_second_name = Column(String(50))
    recipient_phone = Column(String(50))
    project_id = Column(Integer, ForeignKey(
        'project.id', name='fk_recipient_project_id'))

    