Python Uint Test
================

Coding
--------------
from flask_script import Manager

app = create_app('default')
manager = Manager(app)

@manager.command
def adduser(email, username, admin=False):
    """Register a new user."""

@manager.command
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

if __name__ == '__main__':
    manager.run()

How to
--------------
$ python 