
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

    DEBUG = False
    TESTING = False

    # DATABASE_URL not DATABASE_URI is how Heroku environments do it by default
    DATABASE_URI            = os.getenv('DATABASE_URL')
    SQLALCHEMY_DATABASE_URI = DATABASE_URI
    USERNAME                = os.getenv('FLASK_USERNAME')
    SECRET_KEY              = os.getenv('FLASK_SECRET_KEY')
    SECURITY_PASSWORD_SALT  = os.getenv('FLASK_SECURITY_PASSWORD_SALT')

class TestingConfig(Config):
    
    DEBUG = False
    TESTING = True

    DATABASE_URI            = "postgresql://andywrote@localhost/andywrote-testing"
    SQLALCHEMY_DATABASE_URI = DATABASE_URI
    USERNAME                = 'andywrote'
    SECRET_KEY              = 'testing_key'
    SECURITY_PASSWORD_SALT  = 'testing_salt'

class DevelopmentConfig(Config):
    
    DEBUG = True
    TESTING = False

    DATABASE_URI            = "postgresql://andywrote@localhost/andywrote-development"
    SQLALCHEMY_DATABASE_URI = DATABASE_URI
    USERNAME                = 'andywrote'
    SECRET_KEY              = 'development_key'
    SECURITY_PASSWORD_SALT  = 'development_salt'
