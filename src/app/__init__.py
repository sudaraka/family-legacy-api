""" Main Application """

import os

from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy

app_dir = os.path.abspath(os.path.dirname(__file__))

from ..config import config_map

db = SQLAlchemy()


def create_app(config_name):
    """ Create application instance """

    app = Flask(__name__)

    # Load configuration based on given name
    app.config.from_object(config_map.get(config_name, 'dev'))

    # Initialize extensions in application context
    db.init_app(app)

    # Register blueprints
    from .api_v1 import api as api_blueprint_1
    app.register_blueprint(api_blueprint_1, url_prefix='/v1')

    @app.route('/')
    def app_home():
        """ Homepage for API application """

        return render_template('index.html')

    return app
