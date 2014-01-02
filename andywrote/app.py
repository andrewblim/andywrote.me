
from flask import Flask
from config import ProductionConfig, TestingConfig, DevelopmentConfig
import os

# Set up Flask app

app = Flask(__name__)

# Configure app based on HEROKU_ENVIRONMENT

def config_app_heroku(app):
    heroku_environment = os.getenv('HEROKU_ENVIRONMENT', None)
    if heroku_environment == 'production':
        app.config.from_object(ProductionConfig)
    elif heroku_environment == 'testing':
        app.config.from_object(TestingConfig)
    elif heroku_environment == 'development':
        app.config.from_object(DevelopmentConfig)
    else:
        raise Exception('Unrecognized or unset HEROKU_ENVIRONMENT variable')
