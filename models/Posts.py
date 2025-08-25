from sqlalchemy import Column, Integer, String, Text, Float, Boolean, DateTime, Date, Numeric, BigInteger, SmallInteger, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from infrastructure.db_core.base import Base as db

class Posts(db):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    text = Column(Text)
    name_post = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)
    author_id = Column(Integer, ForeignKey(
        'users.id', name='fk_posts_users_id', ondelete="CASCADE"), nullable=True)
    comments = relationship('Comment', backref='posts', passive_deletes=True)
    likes = relationship('Likes', backref='posts', passive_deletes=True)
    project_id = Column(Integer, ForeignKey(
        'project.id', name='fk_posts_project_id'))
