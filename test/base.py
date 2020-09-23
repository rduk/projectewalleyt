
from flask_testing import TestCase

from app import db
from manage import app


class BaseTestCase(TestCase):
    """ Base Tests """

    def create_app(self):
        app.config.from_object('config.TestingConfig')
        return app

    def setUp(self):
        db.create_all()
        db.session.commit()
        db.engine.execute("insert into employee values (1, 'test_staff', 'test_secure')")

    def tearDown(self):
        db.session.remove()
        db.drop_all()
