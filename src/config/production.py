""" Production environment configuration settings """

import os

from . import BaseConfiguration


class ProductionConfiguration(BaseConfiguration):
    """ Configuration settings for production environment """

    DEBUG = False

    TESTING = False

    IGNORE_AUTH = False

    # No fall-back for SECRET_KEY in production
    SECRET_KEY = os.environ.get('FLAPI_SECRET_KEY')
