""" Testing environment configuration settings """

from . import BaseConfiguration


class TestingConfiguration(BaseConfiguration):
    """ Configuration settings for testing environment """

    TESTING = True
