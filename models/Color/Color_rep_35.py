from server_flask.db import db
from datetime import datetime

class Colorrep35(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    color = db.Column(db.Integer, unique=True)
    quantity = db.Column(db.Integer)
    project_id = db.Column(db.Integer, db.ForeignKey(
        'project.id', name='fk_colorrep35_project_id'))