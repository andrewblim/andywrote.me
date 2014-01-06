import os
import andywrote
import unittest

from andywrote import app, config_app_heroku

class AndywroteTestCase(unittest.TestCase):

    def setUp(self):
        os.environ['HEROKU_ENVIRONMENT'] = 'testing'
        config_app_heroku(app)
        self.app = app.test_client()

    def tearDown(self):
        pass

    def test_trivial(self):
        rv = self.app.get('/blog/')
        assert 'No posts.' in rv.data

if __name__ == '__main__':
    unittest.main()