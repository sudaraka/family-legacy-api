""" Celery worker """

import os
import sys

sys.path.append(os.path.dirname('..'))

if os.path.exists('.env'):
    print('Importing environment from .env')  # pylint: disable=I0011,C0325

    for line in open('.env'):
        var = line.strip().split('=')
        if 2 == len(var):
            os.environ[var[0]] = var[1]

from ..app import celery, create_app

app = create_app(os.environ.get('FLASK_CONFIG', 'prod'))
app.app_context().push()
