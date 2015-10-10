import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    APP_NAME = 'AKIndices'
    APP_VERSION = '0.2.0'
    TITLE = 'AKIndices'
    COPYRIGHT_YEAR = 2015
    CSRF_ENABLED = True
    DEBUG = False

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    TITLE = 'AKIndices (test)'
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'top secret'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgres://matthew@localhost/akindices'


config = {
    'development': DevelopmentConfig,

    'default': DevelopmentConfig
}
