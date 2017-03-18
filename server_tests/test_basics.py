import unittest
from flask import current_app
from app import create_app, db
'''
The setUp() and tearDown() methods run before and after each test
Any methods that have a name that begins with "test_" are executed as tests.

How to run the tests
    Method 1: Add a custom command into manage.py script.
    Method 2: Add a custom command into manage.py script.

'''
class BasicsTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_app_exists(self):
        self.assertFalse(current_app is None)

    def test_app_is_testing(self):
        self.assertTrue(current_app.config['TESTING'])


if __name__ == "__main__":
    # main use unittest.TestLoader to run the test cases in current module
    unittest.main()