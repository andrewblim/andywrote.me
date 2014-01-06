
from andywrote import app, config_app_heroku

# won't work except through `python serve.py` if the config_app_heroku call is 
# inside the if __name__ == '__main__' clause (so for example gunicorn won't 
# work)

config_app_heroku(app)

if __name__ == '__main__':
    app.run()
