from flask import request, jsonify
from flask_restful import Resource, abort
from models.account import Account
from models.user import User
from app import db
from config import INACTIVE
import random


class Register(Resource):
    def post(self):
        data = request.get_json()
        name = data.get("name")
        pwd = data.get("pwd")
        id_num = data.get("id_num")
        if not User.query.filter(User.name == name).first():
            while True:
                # in real world this will surely be replaced with a better efficient/scalable service to generate
                # unique account number
                acc_num = random.randint(1000000001, 9999999999)
                if not Account.query.filter(Account.acc_num == acc_num).first():
                    break
            user = User(name=name, password=pwd, id_num=id_num)
            db.session.add(user)
            db.session.commit()
            account = Account(acc_num=acc_num, status=INACTIVE, balance=0, user_id=user.id)
            db.session.add(account)
            db.session.commit()
            return {"message": "User created"}, 201
        else:
            return {"message": "username already registered"}, 409
