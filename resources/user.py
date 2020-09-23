from flask import request
from flask_restful import Resource
from models.account import AccountModel
from models.user import UserModel
from app import db
from config import INACTIVE
import random


class User(Resource):
    def get(self):
        data = request.get_json()
        name = data.get("name")
        pwd = data.get("pwd")
        user = UserModel.query.filter(UserModel.name == name).filter(UserModel.password == pwd).first()
        if user:
            account = AccountModel.query.filter(AccountModel.user_id == user.id).first()
            if account:
                return {"account_number": account.acc_num, "account_status": account.status}
            else:
                return {"message": "Technical error, cannot retrieve acc information. Please call customer care"}, 500
        return {"message": "Username/Pwd incorrect"}, 401

    def post(self):
        data = request.get_json()
        name = data.get("name")
        pwd = data.get("pwd")
        id_num = data.get("id_num")
        if not UserModel.query.filter(UserModel.name == name).first():
            while True:
                # in real world this will surely be replaced with a better efficient/scalable service to generate
                # unique account number
                acc_num = random.randint(1000000001, 9999999999)
                if not AccountModel.query.filter(AccountModel.acc_num == acc_num).first():
                    break
            user = UserModel(name=name, password=pwd, id_num=id_num)
            db.session.add(user)
            db.session.commit()
            account = AccountModel(acc_num=acc_num, status=INACTIVE, balance=0, user_id=user.id)
            db.session.add(account)
            db.session.commit()
            return {"message": "User created", "account_number": account.acc_num, "account_status": account.status}, 201
        else:
            return {"message": "username already registered"}, 409
