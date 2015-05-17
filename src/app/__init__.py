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
    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='')

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    @app.route('/')
    def app_home():  # pylint: disable=I0011,W0612
        """ Homepage for API application """

        return render_template('index.html')

    return app
