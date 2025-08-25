
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, Float, Boolean, DateTime, Date, Numeric, BigInteger, SmallInteger, ForeignKey
from sqlalchemy.orm import relationship
from infrastructure.db_core.base import Base as db

class Comment(db):
    id = Column(Integer, primary_key=True)
    text = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)
    author_id = Column(Integer, ForeignKey(
        'users.id', name='fk_comment_users_id', ondelete="CASCADE"), nullable=True)
    post_id = Column(Integer, ForeignKey(
        'posts.id', name='fk_comment_posts_id',  ondelete="CASCADE"), nullable=True)
    orders_id = Column(Integer, ForeignKey(
        'orders.id', name='fk_comment_orders_id', ondelete="CASCADE"), nullable=True)
    replies = relationship('Reply', back_populates='comment')
    likes = relationship('Likes', backref='comment', passive_deletes=True)
    project_id = Column(Integer, ForeignKey(
        'project.id', name='fk_comment_project_id'))
