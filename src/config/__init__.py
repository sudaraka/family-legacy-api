""" Application Configurations """

import os


class BaseConfiguration(object):
    """ Base/Shared configuration settings for all environments """

    # Flask
    DEBUG = True

    IGNORE_AUTH = False

    SECRET_KEY = os.environ.get('FLAPI_SECRET_KEY',
                                'g78v6R5aA59qg7u63fH68n8ap5g2FC5x')

    # SQL Alchemy
    SQLALCHEMY_ECHO = False

    SQLALCHEMY_DATABASE_URI = 'mysql://%s:%s@%s/%s' % (
        os.environ.get('FLAPI_DB_USER', 'flapi'),
        os.environ.get('FLAPI_DB_PW', ''),
        os.environ.get('FLAPI_DB_HOST', 'localhost'),
        os.environ.get('FLAPI_DB_NAME', 'flapi'),
    )

    # Celery
    BROKER_URL = 'redis://localhost:35275'
    CELERY_RESULT_BACKEND = 'redis://localhost:35275'

    CELERY_ACCEPT_CONTENT = ['json']
    CELERY_TASK_SERIALIZER = 'json'
    CELERY_RESULT_SERIALIZER = 'json'

    # Family Legacy API
    LEGACY_LOCK_DAYS = 30
    LEGACY_EXTEND_DAYS = 30
    EVENT_RUN_COUNT = 2

    # Content location
    CONTENT_DIR = os.path.abspath(os.path.join(
        os.path.dirname(__file__),
        '../../var/content'
    ))

    # Email
    MAIL_SERVER = 'localhost'
    MAIL_PORT = 25
    MAIL_SENDER = 'noreplay@ourfamilylegacy.org'


from .development import DevelopmentConfiguration
from .production import ProductionConfiguration
from .testing import TestingConfiguration


config_map = {
    'dev': DevelopmentConfiguration,
    'prod': ProductionConfiguration,
    'test': TestingConfiguration
}
