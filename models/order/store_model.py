from server_flask.db import db


class Store(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    api = db.Column(db.String(50))
    token = db.Column(db.String(255))
    # store_crm_token = db.Column(db.String(255))
    # marketplace_token = db.Column(db.String(255))
    token_market = db.Column(db.String(255))
    orders = db.relationship("Orders", back_populates="store")
    project_id = db.Column(db.Integer, db.ForeignKey(
        'project.id', name='fk_store_project_id'))