#!/usr/bin/env python
import os
from app import create_app, db
from flask.ext.script import Manager, Shell


app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)


@manager.command
def initdb():
    db.create_all(app=app)


if __name__ == '__main__':
    manager.run()

