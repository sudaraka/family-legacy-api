""" Testing environment configuration settings """

import os
import logging

from ..app import app_dir

from . import BaseConfiguration


class TestingConfiguration(BaseConfiguration):
    """ Configuration settings for testing environment """

    TESTING = True

    IGNORE_AUTH = True

    PRESERVE_CONTEXT_ON_EXCEPTION = False

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(app_dir,
                                                          '../../testdb.sqlite')

    LEGACY_LOCK_DAYS = 15

    LEGACY_EXTEND_DAYS = 45

    LOG_LEVEL = logging.WARNING
