from flask import request, jsonify
from flask_restful import Resource
from models.account import Account
from models.transaction import Transaction
from models.user import User
from app import db
from config import ACTIVE
from datetime import datetime


class Transfer(Resource):
    def post(self):
        data = request.get_json()
        name = data.get("name")
        pwd = data.get("pwd")
        amount = data.get("amount")
        to_acc_num = data.get("to_acc_num")
        message = data.get("message")
        to_account = Account.query.filter(Account.acc_num == to_acc_num).first()
        if not to_account:
            return {"message": "Entered INVALID account number, check receivers account number"}, 400
        user = User.query.filter(User.name == name).filter(User.password == pwd).first()
        if to_account.user_id == user.id:
            return {"message": "Cannot transfer to your own account"}, 400
        elif to_account.status != ACTIVE:
            return {"message": "Cannot process the transaction, receivers account not ACTIVE"}, 400
        if user:
            from_account = Account.query.filter(Account.user_id == user.id).first()
            if from_account.status != ACTIVE:
                return {"message": "Senders Account not active, call customer care to activate the account"}, 400
            if from_account.balance < amount:
                return {"message": "Not enough funds to make this transfer"}, 400
            else:
                to_account.balance += amount
                from_account.balance -= amount
                transaction = Transaction(from_accnum=from_account.acc_num,
                                          to_accnum=to_account.acc_num,
                                          message=message,
                                          amount=amount,
                                          from_acc_balance=from_account.balance,
                                          to_acc_balance=to_account.balance,
                                          transaction_date=datetime.now()
                                          )
                db.session.add_all([to_account, from_account, transaction])
                db.session.commit()
                return {"message": "Transfer successful, new balance: %s" % from_account.balance}
        else:
            return {"message": "Username/Pwd incorrect"}, 401
