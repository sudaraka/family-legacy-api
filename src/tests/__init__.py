""" Unit test module """

from flask.ext.testing import TestCase

from ..app import create_app, db


class BaseCase(TestCase):
    """ Base test case """

    def create_app(self):  # pylint: disable=I0011,R0201
        """ Create application object for test environment """

        return create_app('test')

    def setUp(self):
        """ Setup test case """

        self.app_context = self.app.app_context()
        self.app_context.push()

        db.drop_all()
        db.create_all()

        self.client = self.app.test_client()

    def tearDown(self):
        """ Tear down test case """

        db.session.remove()
        db.drop_all()

        self.app_context.pop()

    def assert201(self, response):
        """ Custom assert for HTTP 201 """

        self.assertEqual(201, response.status_code)
