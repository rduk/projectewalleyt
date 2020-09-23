import unittest

import json
from models.account import Account
from models.user import User
from test.base import BaseTestCase
from config import INACTIVE, ACTIVE


def register_user(self):
    return self.client.post(
        '/register',
        data=json.dumps(dict(
            name='test_user',
            pwd='test_pwd',
            id_num='AAAA123456'
        )),
        content_type='application/json'
    )


def check_balance(self):
    return self.client.get(
        '/balance',
        data=json.dumps(dict(
            name='test_user',
            pwd='test_pwd'
        )),
        content_type='application/json'
    )


def activate_account(self, acc_num):
    return self.client.post(
        '/activate',
        data=json.dumps(dict(
            name='test_staff',
            pwd='test_secure',
            acc_num=acc_num
        )),
        content_type='application/json'
    )


def deposit(self, acc_num):
    return self.client.post(
        '/deposit',
        data=json.dumps(dict(
            name='test_user',
            pwd='test_pwd',
            amount=1000
        )),
        content_type='application/json'
    )


class TestRegister(BaseTestCase):
    def test_end_to_end_flow(self):
        """ Test for user registration """
        with self.client:
            # 1 Register User
            response = register_user(self)
            data = json.loads(response.data)
            self.assertTrue(data['message'] == 'User created')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 201)

            # Assert user created with correct user name
            user = User.query.filter(User.name == 'test_user').first()
            self.assertTrue(user.name, 'test_user')
            self.assertTrue(user.id_num, 'AAAA123456')

            # Assert account created with INACTIVE status
            acc = Account.query.filter(Account.user_id == user.id).first()
            self.assertEqual(acc.status, INACTIVE)

            # # Assert you cannot get a balance fro an inactive account
            response = check_balance(self)
            data = json.loads(response.data)
            self.assertTrue(data['message'] == "Account not ACTIVE, please call customer care")
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 400)

            # Assert a staff can activate an account
            response = activate_account(self, acc.acc_num)
            data = json.loads(response.data)
            self.assertTrue(data['message'] == "Account Activated")
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 201)
            acc = Account.query.filter(Account.user_id == user.id).first()
            self.assertEqual(acc.status, ACTIVE)

            # Test deposit feature
            response = deposit(self, acc.acc_num)
            data = json.loads(response.data)
            self.assertTrue(data['message'] == "Deposit successful, new balance: 1000")
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 200)

            # Assert balance is 1000
            response = check_balance(self)
            data = json.loads(response.data)
            self.assertTrue(data['balance'] == 1000)
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 200)

            """
            We could add many more test likewise. Few scenarios which could be covered:
            -> Deposit some more money and assert new balance
            -> Create one more user and after Activating transfer money to this user from test_user
            -> Assert transactions based on above actions
            etc
            """


if __name__ == '__main__':
    unittest.main()
