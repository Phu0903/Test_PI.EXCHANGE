import unittest
from send_email import *


class TestFirst(unittest.TestCase):
    TEMP_PATH = 'path/to/email_template.json'
    CUSTOMERS_PATH = 'path/to/customers.csv'

    def test_Application(self):
        app = Application()
        args = (self.TEMP_PATH, self.CUSTOMERS_PATH)
        self.assertEqual(app.getData(*args), True)


if __name__ == '__main__':
    unittest.main(verbosity=2)
