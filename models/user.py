from app import db


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), index=True, unique=True, nullable=False)
    password = db.Column(db.String(80), index=True, nullable=False)
    # any identification document # like NRIC #, license #, passport # etc
    id_num = db.Column(db.String, index=True, unique=True, nullable=False)

