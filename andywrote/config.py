
import os

class Config(object):

    DEBUG = False
    TESTING = False
    DATABASE_URI = None

    SECURITY_LOGIN_USER_TEMPLATE = "security/login_user.html"
    SECURITY_TRACKABLE     = True
    SECURITY_PASSWORD_HASH = 'sha512_crypt'

    # all these flags are set to False, their defaults in Flask-Security, 
    # but might be useful if you ever want to make this a multi-user site

    SECURITY_CONFIRMABLE  = False
    SECURITY_REGISTERABLE = False
    SECURITY_RECOVERABLE  = False
    SECURITY_CHANGEABLE   = False


# Obviously don't deploy anything into production using anything other than
# the ProductionConfig. 

class ProductionConfig(Config):

    DEBUG = False # just to be explicit

    SQLALCHEMY_DATABASE_URI = os.getenv('FLASK_SQLALCHEMY_DATABASE_URI')
    USERNAME                = os.getenv('FLASK_USERNAME')
    SECRET_KEY              = os.getenv('FLASK_SECRET_KEY')
    SECURITY_PASSWORD_SALT  = os.getenv('FLASK_SECURITY_PASSWORD_SALT')


class DevelopmentConfig(Config):

    DEBUG = True

    SQLALCHEMY_DATABASE_URI = "postgresql://andywrote@localhost/andywrote"
    USERNAME                = 'andywrote'
    SECRET_KEY              = 'development_key'
    SECURITY_PASSWORD_SALT  = 'developmentsalt'
