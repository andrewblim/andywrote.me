import os
import andywrote
import unittest

from app import app, config_app_heroku

class AndywroteTestCase(unittest.TestCase):

    def setUp(self):
        os.environ['HEROKU_ENVIRONMENT'] = 'testing'
        config_app_heroku(app)

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()