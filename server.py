#!/usr/bin/env python
"""
server.py: runs development server
"""

import os

from src.app import create_app, db


if '__main__' == __name__:
    app = create_app(os.environ.get('FLASK_CONFIG', 'dev'))

    with app.app_context():
        db.create_all()

    app.run()
