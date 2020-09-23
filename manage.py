import os
import unittest

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from app import create_app, db

app = create_app(os.getenv('BOILERPLATE_ENV') or 'dev')

app.app_context().push()

manager = Manager(app)

migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)


@manager.command
def run():
    app.run(host='0.0.0.0')


@manager.command
def set_employee():
    db.engine.execute("insert into employee values (1, 'staff', 'secure')")


@manager.command
def set_users():
    db.engine.execute("insert into user values (1, 'user1', 'secure', '123456ABC')")
    db.engine.execute("insert into account values(1, 2736565246, 'INACTIVE', 0, 1)")
    db.engine.execute("insert into user values (2, 'user2', 'secure', '333333XYZ')")
    db.engine.execute("insert into account values(2, 8975927435, 'INACTIVE', 0, 2)")
    db.engine.execute("insert into user values (3, 'user3', 'secure', 'ABCDEF123')")
    db.engine.execute("insert into account values(3, 4356234532, 'INACTIVE', 0, 3)")


@manager.command
def test():
    """Runs the unit tests."""
    tests = unittest.TestLoader().discover('test', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


if __name__ == '__main__':
    manager.run()
