""" Main Application """

import os
import logging

from celery import Celery
from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy

app_dir = os.path.abspath(os.path.dirname(__file__))

from ..config import config_map

db = SQLAlchemy()
celery = Celery(__name__)


def create_app(config_name):
    """ Create application instance """

    app = Flask(__name__)

    # Load configuration based on given name
    app.config.from_object(config_map.get(config_name, 'prod'))

    # Make Celery instance use inherit the Flask configuration
    celery.conf.update(app.config)

    # Initialize extensions in application context
    db.init_app(app)

    # Setup logging
    if not app.config.get('DEBUG', False) \
            and not app.config.get('TESTING', False):

        mail_log = logging.handlers.SMTPHandler(
            app.config.get('MAIL_SERVER', 'localhost'),
            'no-reply@ourfamilylegacy.org',
            app.config.get('ERROR_MAIL_RECEIVERS',
                           ['admin@ourfamilylegacy.org']),
            'Error occurred in API application'
        )
        mail_log.setLevel(app.config.get('ERROR_EMAIL_LEVEL', logging.ERROR))

        mail_log.setFormatter(logging.Formatter('''
        Message type:       %(levelname)s
        Location:           %(pathname)s:%(lineno)d
        Module:             %(module)s
        Function:           %(funcName)s
        Time:               %(asctime)s

        Message:

        %(message)s
        '''))

        app.logger.addHandler(mail_log)

    file_log = logging.handlers.RotatingFileHandler(
        'log/flapi.log',
        maxBytes=1024*1024,
        backupCount=5
    )
    file_log.setLevel(app.config.get('LOG_LEVEL', logging.WARNING))
    file_log.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s '
        '[in %(pathname)s:%(lineno)d]'
    ))
    app.logger.addHandler(file_log)

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
