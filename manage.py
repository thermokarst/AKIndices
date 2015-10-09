#!/usr/bin/env python
import os
from app import create_app, db
from flask.ext.script import Manager, Shell


app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)


@manager.command
def initdb():
    from sqlalchemy.sql import text
    cmd = """
        CREATE TABLE new_communities (
            id serial NOT NULL,
            name character varying(50) NOT NULL,
            northing double precision NOT NULL,
            easting double precision NOT NULL,
            latitude double precision NOT NULL,
            longitude double precision NOT NULL,
            data jsonb NOT NULL,
            CONSTRAINT new_communities_pkey PRIMARY KEY (id)
        );"""
    _ = db.engine.execute(text(cmd))


if __name__ == '__main__':
    manager.run()
