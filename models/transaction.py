from datetime import datetime
from app import db


class Transaction(db.Model):
    __tablename__ = 'transaction'
    id = db.Column(db.Integer, primary_key=True)
    from_accnum = db.Column(db.Integer, db.ForeignKey('account.id'), index=True, nullable=False)
    to_accnum = db.Column(db.Integer, db.ForeignKey('account.id'), index=True, nullable=False)
    message = db.Column(db.String(200), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    from_acc_balance = db.Column(db.Float)
    to_acc_balance = db.Column(db.Float)
    transaction_date = db.Column(db.DateTime, default=datetime.now(), nullable=False)
