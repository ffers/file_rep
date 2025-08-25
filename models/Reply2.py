from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, Float, Boolean, DateTime, Date, Numeric, BigInteger, SmallInteger, ForeignKey
from sqlalchemy.orm import relationship
from infrastructure.db_core.base import Base as db

class Reply2(db):
    __tablename__ = 'reply2'
    id = Column(Integer, primary_key=True)
    comment_id = Column(Integer, ForeignKey('reply.id', name='reply2_comment_id'), nullable=False)
    text = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)
    comment = relationship('Reply', back_populates='replies')
    project_id = Column(Integer, ForeignKey(
        'project.id', name='fk_reply2_project_id'))