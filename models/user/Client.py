from server_flask.db import db

class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    second_name = db.Column(db.String(50))
    full_name = db.Column(db.String(50))
    phone = db.Column(db.String(50))
    project_id = db.Column(db.Integer, db.ForeignKey(
        'project.id', name='fk_client_project_id'))

    