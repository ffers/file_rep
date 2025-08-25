from sqlalchemy import Column, Integer, String, Text, Float, Boolean, DateTime, Date, Numeric, BigInteger, SmallInteger, ForeignKey, UniqueConstraint, Index
from sqlalchemy.orm import relationship
from infrastructure.db_core.base import Base as db

class UserRoles(db):
    __tablename__ = 'user_roles'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    role_id = Column(Integer, ForeignKey('role.id', ondelete='CASCADE'))
    project_id = Column(Integer, ForeignKey(
        'project.id', name='fk_user_roles_project_id'))

    user    = relationship("Users",    back_populates="user_roles")
    role    = relationship("Role",    back_populates="user_roles")
    project = relationship("Project", back_populates="user_roles")

    __table_args__ = (
        UniqueConstraint("user_id", "project_id", name="uq_user_project"),  # рівно одна роль у проекті
        Index("ix_user_roles_user_project", "user_id", "project_id"),
    )
    


    
