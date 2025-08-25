from server_flask.db import db
from sqlalchemy.orm import relationship


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    user_roles = relationship(
        "UserRoles",
        back_populates="role",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

 