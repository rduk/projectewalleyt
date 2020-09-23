from flask import request, jsonify
from flask_restful import Resource
from config import DEPOSIT_FROM_ACCNUM, ACTIVE
from models.account import Account
from models.transaction import Transaction
from models.user import User


class Transactions(Resource):
    def get(self):
        all_transactions = []
        data = request.get_json()
        name = data.get("name")
        pwd = data.get("pwd")
        user = User.query.filter(User.name == name).filter(User.password == pwd).first()
        if user:
            account = Account.query.filter(Account.user_id == user.id).first()
            if not account.status == ACTIVE:
                return {"message": "Account not ACTIVE, please call customer care"}, 400
            transactions = (Transaction.query.filter((Transaction.to_accnum == account.acc_num) |
                                                     (Transaction.from_accnum == account.acc_num)).order_by(
                Transaction.transaction_date.desc()).all())
            for transaction in transactions:
                to_user = User.query.join(Account).filter(transaction.to_accnum == Account.acc_num).filter(
                    Account.user_id == User.id).first()
                if transaction.from_accnum == DEPOSIT_FROM_ACCNUM:
                    from_details = "Third party source"
                else:
                    from_user = User.query.join(Account).filter(transaction.from_accnum == Account.acc_num).filter(
                        Account.user_id == User.id).first()
                    from_details = ''.join([str(transaction.from_accnum), '<', from_user.name, '>'])
                if account.acc_num == transaction.from_accnum:
                    interim_balance = transaction.from_acc_balance
                    transaction_amount = ''.join(['-', str(transaction.amount)])
                else:
                    interim_balance = transaction.to_acc_balance
                    transaction_amount = ''.join(['+', str(transaction.amount)])
                all_transactions.append({"from": from_details,
                                         "to": ''.join([str(transaction.to_accnum), '<', to_user.name, '>']),
                                         "amount": transaction_amount,
                                         "msg": transaction.message,
                                         "date": transaction.transaction_date.strftime("%d/%m/%Y %H:%M:%S"),
                                         "interim_balance": interim_balance})
            return {"transactions": all_transactions, "balance": account.balance}
        else:
            return {"message": "Username/Pwd incorrect"}, 401
