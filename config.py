import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    APP_NAME = 'AKIndices'
    APP_VERSION = '0.2.0'


class DevelopmentConfig(Config):
    DEBUG = True
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'top secret'
    DATABASE_URL = os.environ.get('DATABASE_URL')

