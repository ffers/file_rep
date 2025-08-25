from datetime import datetime
from server_flask.db import db
from sqlalchemy.orm import relationship


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    name = db.Column(db.String(150))
    user_id = db.Column(db.Integer, db.ForeignKey( 
        'users.id', name='fk_project_users_id'), nullable=False)  
    user_roles = relationship(
        "UserRoles",
        back_populates="project",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )