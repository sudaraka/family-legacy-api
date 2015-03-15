#!/usr/bin/env python
"""
server.py: runs development server
"""

import os

from src.app import create_app

if '__main__' == __name__:
    app = create_app(os.environ.get('FLASK_CONFIG', 'dev'))

    app.run()
