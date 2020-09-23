from flask import request, jsonify
from flask_restful import Resource
from config import DEPOSIT_FROM_ACCNUM, ACTIVE
from models.account import AccountModel
from models.transaction import TransactionModel
from models.user import UserModel


class Transactions(Resource):
    def get(self):
        all_transactions = []
        data = request.get_json()
        name = data.get("name")
        pwd = data.get("pwd")
        user = UserModel.query.filter(UserModel.name == name).filter(UserModel.password == pwd).first()
        if user:
            account = AccountModel.query.filter(AccountModel.user_id == user.id).first()
            if not account.status == ACTIVE:
                return {"message": "Account not ACTIVE, please call customer care"}, 400
            transactions = (TransactionModel.query.filter((TransactionModel.to_accnum == account.acc_num) |
                                                          (TransactionModel.from_accnum == account.acc_num)).order_by(
                TransactionModel.transaction_date.desc()).all())
            for transaction in transactions:
                to_user = UserModel.query.join(AccountModel).filter(
                    transaction.to_accnum == AccountModel.acc_num).filter(AccountModel.user_id == UserModel.id).first()
                if transaction.from_accnum == DEPOSIT_FROM_ACCNUM:
                    from_details = "Third party source"
                else:
                    from_user = UserModel.query.join(AccountModel).filter(
                        transaction.from_accnum == AccountModel.acc_num).filter(
                        AccountModel.user_id == UserModel.id).first()
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
