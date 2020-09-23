from flask import request
from flask_restful import Resource
from models.account import AccountModel
from models.transaction import TransactionModel
from models.user import UserModel
from config import ACTIVE, DEPOSIT_FROM_ACCNUM
from app import db
from datetime import datetime


class Deposit(Resource):
    def post(self):
        # you could deposit using the user_name/pwd
        data = request.get_json()
        name = data.get("name")
        pwd = data.get("pwd")
        amount = data.get("amount")
        user = UserModel.query.filter(UserModel.name == name).filter(UserModel.password == pwd).first()
        if user:
            account = AccountModel.query.filter(AccountModel.user_id == user.id).first()
            if account:
                if account.status == ACTIVE:
                    account.balance += amount
                    transaction = TransactionModel(from_accnum=DEPOSIT_FROM_ACCNUM,
                                                   to_accnum=account.acc_num,
                                                   message="Money deposited: External Source",
                                                   amount=amount,
                                                   to_acc_balance=account.balance,
                                                   transaction_date=datetime.now()
                                                   )
                    db.session.add_all([account, transaction])
                    db.session.commit()
                    return {"message": "Deposit successful, new balance: %s" % account.balance}
                else:
                    return {"message": "Account Inactive, call customer care to activate the account"}, 403
            else:
                return {"message": "Technical error retrieving account, please call customer care"}, 500
        return {"message": "Username/Pwd incorrect"}, 401
