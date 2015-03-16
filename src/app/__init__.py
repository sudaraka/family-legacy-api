""" Main Application """

import os

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

from ..config import config_map

app_dir = os.path.abspath(os.path.dirname(__file__))

db = SQLAlchemy()


def create_app(config_name):
    """ Create application instance """

    app = Flask(__name__)

    # Load configuration based on given name
    app.config.from_object(config_map.get(config_name, 'dev'))

    # Initialize extensions in application context
    db.init_app(app)

    return app
