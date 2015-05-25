""" Application Configurations """

import os


class BaseConfiguration(object):
    """ Base/Shared configuration settings for all environments """

    DEBUG = True

    IGNORE_AUTH = False

    SECRET_KEY = os.environ.get('FLAPI_SECRET_KEY',
                                'g78v6R5aA59qg7u63fH68n8ap5g2FC5x')

    SQLALCHEMY_ECHO = False

    SQLALCHEMY_DATABASE_URI = 'mysql://%s:%s@%s/%s' % (
        os.environ.get('FLAPI_DB_USER', 'flapi'),
        os.environ.get('FLAPI_DB_PW', ''),
        os.environ.get('FLAPI_DB_HOST', 'localhost'),
        os.environ.get('FLAPI_DB_NAME', 'flapi'),
    )

    LEGACY_LOCK_DAYS = 30

    LEGACY_EXTEND_DAYS = 30


from .development import DevelopmentConfiguration
from .production import ProductionConfiguration
from .testing import TestingConfiguration


config_map = {
    'dev': DevelopmentConfiguration,
    'prod': ProductionConfiguration,
    'test': TestingConfiguration
}
