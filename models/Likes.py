from sqlalchemy import Column, Integer, String, Text, Float, Boolean, DateTime, Date, Numeric, BigInteger, SmallInteger, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from infrastructure.db_core.base import Base as db

class Likes(db):
    __tablename__ = 'likes'
    id = Column(Integer, primary_key=True)
    date_created = Column(DateTime(timezone=True), default=func.now())
    author_id = Column(Integer, ForeignKey(
        'users.id', name='fk_likes_users_id', ondelete="CASCADE"), nullable=False)
    posts_id = Column(Integer, ForeignKey(
        'posts.id', name='fk_likes_posts_id', ondelete="CASCADE"), nullable=True)
    orders_id = Column(Integer, ForeignKey(
        'orders.id', name='fk_likes_orders_id', ondelete="CASCADE"), nullable=True)
    products_id = Column(Integer, ForeignKey(
        'products.id', name='fk_likes_products_id', ondelete="CASCADE"), nullable=True)
    comment_id = Column(Integer, ForeignKey(
        'comment.id', name='fk_likes_comment_id', ondelete="CASCADE"), nullable=True)
    project_id = Column(Integer, ForeignKey(
        'project.id', name='fk_likes_project_id'))