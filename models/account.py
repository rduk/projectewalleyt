from app import db


class Account(db.Model):
    __tablename__ = 'account'
    id = db.Column(db.Integer, primary_key=True)
    acc_num = db.Column(db.Integer, index=True, unique=True, nullable=False)
    status = db.Column(db.String(20), nullable=False)   # Inactive, Active, Dormant
    balance = db.Column(db.Integer, default=0, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

