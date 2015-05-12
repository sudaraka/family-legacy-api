#!/usr/bin/env python
"""
manage.py: run application related commands
"""

import os
import sys

sys.path.append(os.path.dirname('..'))

if os.path.exists('.env'):
    print('Importing environment from .env')  # pylint: disable=I0011,C0325

    for line in open('.env'):
        var = line.strip().split('=')
        if 2 == len(var):
            os.environ[var[0]] = var[1]

from flask.ext.script import Manager

from src.app import create_app, db, models


app = create_app(os.environ.get('FLASK_CONFIG', 'prod'))
manager = Manager(app)


@manager.shell
def shell_context():
    """
    Return a cusom context for shell with application object, database and
    models
    """

    return dict(app=app, db=db, models=models)


if '__main__' == __name__:
    manager.run()
