import os
import andywrote
import unittest

from andywrote import app, config_app_heroku, create_user, delete_all_records

class AndywroteTestCase(unittest.TestCase):

    def setUp(self):
        os.environ['HEROKU_ENVIRONMENT'] = 'testing'
        self.email = 'testing@andywrote.me'
        self.name = 'Mr. Test'
        self.display_name = ''  # should set to name if ''
        self.password = 'testing'
        config_app_heroku(app)
        delete_all_records()
        with app.app_context():
            create_user(
                **dict(email=self.email,
                       name=self.name,
                       display_name=self.display_name,
                       password=self.password))
        self.app = app.test_client()

    def tearDown(self):
        delete_all_records()

    def test_about_visitor(self):
        rv = self.app.get('/')
        assert '<h1>andywrote.me</h1>' in rv.data
        assert 'In TESTING mode' in rv.data

    def login(self, email, password, remember):
        return self.app.post('/login', 
            data=dict(email=email,
                      password=password), 
            follow_redirects=True)
    
    def logout(self):
        return self.app.get('/logout', follow_redirects=True)

    def test_login_logout(self):
        # rv = self.login(self.email, self.password, False)
        # assert self.email in rv.data
        # assert 'Write a blog post' in rv.data
        # rv = self.logout()
        # assert self.email not in rv.data
        # assert 'Write a blog post' not in rv.data
        rv = self.login('baduser@andywrote.me', 'badpass', False)
        print rv.data
        assert 'Specified user does not exist' in rv.data
        rv = self.login(self.email, 'badpass', False)
        assert 'Password not provided' in rv.data

if __name__ == '__main__':
    unittest.main()