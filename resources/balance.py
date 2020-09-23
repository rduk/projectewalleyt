from flask import request, jsonify
from flask_restful import Resource
from models.account import Account
from models.user import User
from config import ACTIVE


class Balance(Resource):
    def get(self):
        data = request.get_json()
        name = data.get("name")
        pwd = data.get("pwd")
        user = User.query.filter(User.name == name).filter(User.password == pwd).first()
        if user:
            account = Account.query.filter(Account.user_id == user.id).first()
            if account:
                if account.status == ACTIVE:
                    return jsonify({"balance": account.balance})
                else:
                    return {"message": "Account not ACTIVE, please call customer care"}, 400
            else:
                return {"message": "Technical error, cannot retrieve balance. Please call customer care"}, 500
        return {"message": "Username/Pwd incorrect"}, 401

