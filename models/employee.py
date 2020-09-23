from app import db


class EmployeeModel(db.Model):
    __tablename__ = 'employee'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), index=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
