
from andywrote import app, config_app_heroku

if __name__ == '__main__':
    config_app_heroku(app)
    app.run()
