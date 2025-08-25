from server_flask.db import db
from sqlalchemy import UniqueConstraint, Index
from sqlalchemy.orm import relationship

class UserRoles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer, db.ForeignKey('role.id', ondelete='CASCADE'))
    project_id = db.Column(db.Integer, db.ForeignKey(
        'project.id', name='fk_user_roles_project_id'))

    user    = relationship("Users",    back_populates="user_roles")
    role    = relationship("Role",    back_populates="user_roles")
    project = relationship("Project", back_populates="user_roles")

    __table_args__ = (
        db.UniqueConstraint("user_id", "project_id", name="uq_user_project"),  # рівно одна роль у проекті
        db.Index("ix_user_roles_user_project", "user_id", "project_id"),
    )
    


    
