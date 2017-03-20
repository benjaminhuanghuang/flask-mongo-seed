Python Uint Test
================

Coding
--------------
import unittest

class BasicsTestCase(unittest.TestCase):
    def setUp(self):
        pass
    
    def tearDown(self):
        pass

    def test_app_exists(self):
        pass
        
The setUp() and tearDown() methods run before and after each test
Any methods that have a name that begins with "test_" are executed as tests.

How to
--------------
    * Method 1: 
        Add a custom command into manage.py script.
        $ python manage.py test
        
    * Method 2: 
        # main use unittest.TestLoader to run the test cases in current module
        if __name__ == "__main__":
            unittest.main()

    * Method 3:
        Run test 
        $ python unittest.py widgettests.WidgetTestSuite