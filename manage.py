#!/usr/bin/env python
import os
from app import create_app, db
from flask.ext.script import Manager, Shell, Command, Option


# http://stackoverflow.com/a/24606817
class GunicornServer(Command):
    """Run the app within Gunicorn"""

    def get_options(self):
        from gunicorn.config import make_settings

        settings = make_settings()
        options = (
            Option(*klass.cli, action=klass.action)
            for setting, klass in settings.iteritems() if klass.cli
        )
        return options

    def run(self, *args, **kwargs):
        from gunicorn.app.wsgiapp import WSGIApplication

        app = WSGIApplication()
        app.app_uri = 'manage:app'
        return app.run()


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

manager.add_command("gunicorn", GunicornServer())


if __name__ == '__main__':
    manager.run()
