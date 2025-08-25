



from server_flask.db import db
from datetime import datetime

class BalanceJournal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    event_date = db.Column(db.DateTime)
    desription = db.Column(db.String(50))
    total = db.Column(db.Numeric(precision=8, scale=2))
    income = db.Column(db.Numeric(precision=8, scale=2))
    project_id = db.Column(db.Integer, db.ForeignKey(
        'project.id', name='fk_balance_journal_project_id'))
    project = db.relationship('Project', backref='balance_journal')
    balance_id = db.Column(db.Integer, db.ForeignKey(
        'balance.id', name='fk_balance_journal_balance_id'))
    balance = db.relationship('Balance', backref='balance_journal')
    project_id = db.Column(db.Integer, db.ForeignKey(
        'project.id', name='fk_balance_journal_project_id'))