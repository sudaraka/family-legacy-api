""" Development environment configuration settings """

from . import BaseConfiguration


class DevelopmentConfiguration(BaseConfiguration):
    """ Configuration settings for development environment """

    MAIL_PORT = 8025
