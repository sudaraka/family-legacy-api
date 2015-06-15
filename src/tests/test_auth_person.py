""" Tests for /auth/person API """

from base64 import b64encode

from flask import current_app

from . import BaseCase


class AuthPersonTest(BaseCase):
    """ /auth/person test case """

    def test_authanticate_with_correct_credentials(self):
        """
        GET /auth/person with valid username password returns a access token and
        person record
        """

        self.create_person()

        response = self.client.get('/auth/person',
                                   headers=self.auth_header('test_user',
                                                            'ubersecret'))

        self.assert200(response)

        self.assertGreater(len(response.json['token']), 1)

        p = response.json['user']
        self.assertEqual('UNPAID', p['status'])
        self.assertEqual('Test First Name', p['first_name'])
        self.assertEqual('Test Last Name', p['last_name'])
        self.assertEqual('Test Email', p['email'])
        self.assertIn('/persons/1', p['_links']['self'])

    def test_authanticate_with_empty_credentials(self):
        """
        GET /auth/person without authentication HTTP header returns HTTP 401
        """

        self.create_person()

        response = self.client.get('/auth/person')

        self.assert401(response)

    def test_authanticate_with_incorrect_credentials(self):
        """ GET /auth/person with invalid username password returns HTTP 401 """

        self.create_person()

        response = self.client.get('/auth/person',
                                   headers=self.auth_header('bad_user',
                                                            'bad_password'))

        self.assert401(response)

    def create_person(self):
        """ Create a temporary test record """

        return self.create_resource('/persons/', {
            'first_name': 'Test First Name',
            'last_name': 'Test Last Name',
            'email': 'Test Email',
            'username': 'test_user',
            'password': 'ubersecret'
        })

    # pylint: disable=I0011,R0201
    def auth_header(self, username, password, headers=None):
        """
        Return the HTTP Authorization header created using given username and
        password
        """

        if not isinstance(headers, dict):
            headers = {}

        headers['Authorization'] = 'Basic {}'.format(
            b64encode('{}:{}'.format(username,
                                     password).encode('utf-8')).decode('utf-8')
        )

        return headers
