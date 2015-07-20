""" Base Unit Test Case """

import json

from flask.ext.testing import TestCase

from ..app import create_app, db


class BaseCase(TestCase):
    """ Base test case """

    user_count = 0

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

    def assert202(self, response):
        """ Custom assert for HTTP 202 """

        self.assertEqual(202, response.status_code)

    def create_resource(self, url, data):
        """
        Return the HTTP response of POST of data to the given resource url
        """

        return self.client.post(url, data=json.dumps(data),
                                content_type='application/json')

    def get_resource(self, url):
        """
        Return the dictionary (JSON) obtained by making HTTP GET request to
        given resource url
        """

        response = self.client.get(url)

        self.assert200(response)

        return response.json

    def create_person(self, **kwargs):
        """ Create a temporary test person record """

        self.user_count += 1

        for field in ['first_name', 'last_name', 'email', 'username']:
            if field not in kwargs:
                kwargs[field] = 'Test {}{}'.format(field, str(self.user_count))

        return self.create_resource('/persons/', kwargs)
