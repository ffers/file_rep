from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, Float, Boolean, DateTime, Date, Numeric, BigInteger, SmallInteger, ForeignKey
from sqlalchemy.orm import relationship
from infrastructure.db_core.base import Base as db

class Reply(db):
    __tablename__ = 'reply'
    id = Column(Integer, primary_key=True)
    comment_id = Column(Integer, ForeignKey('comment.id', name='reply_comment_id'), nullable=False)
    text = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)
    comment = relationship('Comment', back_populates='replies')
    replies = relationship('Reply2', back_populates='comment')
    project_id = Column(Integer, ForeignKey(
        'project.id', name='fk_reply_project_id'))
