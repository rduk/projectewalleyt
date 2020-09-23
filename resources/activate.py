from flask import request
from flask_restful import Resource
from models.account import AccountModel
from models.employee import EmployeeModel
from app import db
from config import ACTIVE, INACTIVE, DORMANT


class Activate(Resource):
    def post(self):
        data = request.get_json()
        name = data.get("name")
        pwd = data.get("pwd")
        acc_num = data.get("acc_num")
        employee = EmployeeModel.query.filter(EmployeeModel.name == name).filter(
            EmployeeModel.password == pwd).first()
        if employee:
            acc = AccountModel.query.filter(AccountModel.acc_num == acc_num).first()
            if acc:
                if acc.status == INACTIVE:
                    acc.status = ACTIVE
                    db.session.add(acc)
                    db.session.commit()
                    return {"message": "Account Activated"}, 201
                elif acc.status == ACTIVE:
                    return {"message": "Account already ACTIVATED"}
                elif acc.status == DORMANT:
                    return {"message": "Cannot ACTIVATE a DORMANT acc online, Please call customer care"}
            else:
                return {"message": "Internal server error"}, 500
        else:
            return {"message": "Username/Pwd incorrect"}, 401
