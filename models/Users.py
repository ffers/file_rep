from flask_login import UserMixin
from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from infrastructure.db_core.base import Base as db





class Users(db, UserMixin):
    __tablename__ = 'users' 
    
    id = Column(Integer, primary_key=True)
    email = Column(String(150), unique=True)
    username = Column(String(150), unique=True, nullable=False)
    password = Column(String(255))
    timestamp = Column(DateTime, default=datetime.utcnow)
    posts = relationship('Posts', backref='users', passive_deletes=True)
    orders = relationship('Orders', backref='users', passive_deletes=True)
    comments = relationship('Comment', backref='users', passive_deletes=True)
    likes = relationship('Likes', backref='users', passive_deletes=True)
    roles = relationship(
        "Role",
        secondary="user_roles",
        viewonly=True,
        overlaps="user_roles,role,users",
    )
    user_roles = relationship(
        "UserRoles",
        back_populates="user",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    #dsd project = db.relationship('Project', secondary='user_project', backref='user')
