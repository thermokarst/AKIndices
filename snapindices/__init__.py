# -*- coding: utf-8 -*-

from flask import Flask
import logging
from logging.handlers import RotatingFileHandler

application = Flask(__name__)
application.config.from_pyfile('../config.py')

format = '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'

if not application.debug:
    file_handler = RotatingFileHandler(application.config['LOG'],
                                       maxBytes=application.config['MAXLOG'],
                                       backupCount=application.config['BACKUPCOUNT'])
    application.logger.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter(format))
    application.logger.addHandler(file_handler)

from snapindices import views
