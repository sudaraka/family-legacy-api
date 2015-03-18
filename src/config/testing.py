""" Testing environment configuration settings """

import os

from ..app import app_dir

from . import BaseConfiguration


class TestingConfiguration(BaseConfiguration):
    """ Configuration settings for testing environment """

    TESTING = True

    SQLALCHEMY_ECHO = False

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(app_dir,
                                                          '../../testdb.sqlite')
