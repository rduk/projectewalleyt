from flask import Flask, jsonify
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from config import config_by_name

# todo marshal
# todo refactor


class Hello(Resource):
    def get(self):
        return jsonify({"msg": "welcome"})


db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])
    app.config['JSON_SORT_KEYS'] = False
    db.init_app(app)
    api = Api(app)
    from resources.user import User
    from resources.transactions import Transactions
    from resources.balance import Balance
    from resources.activate import Activate
    from resources.deposit import Deposit
    from resources.transfer import Transfer
    api.add_resource(User, "/user")
    api.add_resource(Activate, "/activate")
    api.add_resource(Deposit, "/deposit")
    api.add_resource(Balance, "/balance")
    api.add_resource(Transfer, "/transfer")
    api.add_resource(Transactions, "/transactions")
    api.add_resource(Hello, "/")
    return app
