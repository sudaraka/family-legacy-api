""" Main Application """

import os

from flask import Flask

from ..config import config_map

app_dir = os.path.abspath(os.path.dirname(__file__))


def create_app(config_name):
    """ Create application instance """

    app = Flask(__name__)

    # Load configuration based on given name
    app.config.from_object(config_map.get(config_name, 'dev'))

    return app
