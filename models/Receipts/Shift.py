from datetime import datetime
from server_flask.db import db
from DTO import ReceiptDTO
 

class Shift(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow())
    shift_id = db.Column(db.String(255))
    open = db.Column(db.DateTime)
    closed = db.Column(db.DateTime)
    cash_id = db.Column(db.Integer, db.ForeignKey(
        'cash.id', name='fk_shift_cash_id'))
    receipts =  db.relationship('Receipt', backref='shift')
    project_id = db.Column(db.Integer, db.ForeignKey(
        'project.id', name='fk_shift_project_id'))

    def __init__(self, d: ReceiptDTO):
        self.shifd_id = d.shift_id
        self.open = d.open
        self.closed = d.closed

    def update(self, d: ReceiptDTO):
        self.shifd_id = d.shift_id or self.shifd_id
        self.open = d.open or self.open
        self.closed = d.closed or self.closed 
