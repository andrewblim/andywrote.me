
from andywrote import app, create_user, config_app_heroku

if __name__ == '__main__':
    config_app_heroku(app)
    with app.app_context():
        create_user()