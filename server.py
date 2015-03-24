#!/usr/bin/env python
"""
server.py: runs development server
"""

import os


if os.path.exists('.env'):
    print('Importing environment from .env')  # pylint: disable=I0011,C0325

    for line in open('.env'):
        var = line.strip().split('=')
        if 2 == len(var):
            os.environ[var[0]] = var[1]


# Import models to context so they will be created when script runs
from src.app import create_app, db, models


if '__main__' == __name__:
    app = create_app(os.environ.get('FLASK_CONFIG', 'dev'))

    with app.app_context():
        db.create_all()

    app.run()
