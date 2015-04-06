""" WSGI module for Gunicorn """

import os

from src.app import create_app


application = create_app(os.environ.get('FLASK_CONFIG', 'prod'))
