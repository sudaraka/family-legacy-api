""" Application Configurations """

import os


class BaseConfiguration(object):
    """ Base/Shared configuration settings for all environments """

    DEBUG = True

    SECRET_KEY = os.environ.get('SECRET_KEY', 'OuK5jz82GD33Dy7LzD5UX2Gj956Cz89')


from .development import DevelopmentConfiguration
from .production import ProductionConfiguration
from .testing import TestingConfiguration


config_map = {
    'dev': DevelopmentConfiguration,
    'prod': ProductionConfiguration,
    'test': TestingConfiguration
}
