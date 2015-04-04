""" Tests for /persons/ API """

import json

from . import BaseCase
from ..app import db
from ..app.models import Person


class PersonsTest(BaseCase):
    """ /persons/ test case """

    def test_get_non_existing(self):
        """ GET /persons/1 on empty DB must return HTTP 404 """

        response = self.client.get('/persons/1')

        self.assert404(response)
        self.assertEqual('not found', response.json['error'])

    def test_get_existing(self):
        """ GET /persons/1 on DB with valid record must return it """

        p = Person(first_name='Test First Name', last_name='Test Last Name',
                   email='Test Email')

        db.session.add(p)
        db.session.commit()

        response = self.client.get('/persons/1')

        self.assert200(response)
        self.assertEqual(1, response.json['id'])
        self.assertEqual('UNPAID', response.json['status'])
        self.assertEqual('Test First Name', response.json['first_name'])
        self.assertEqual('Test Last Name', response.json['last_name'])
        self.assertEqual('Test Email', response.json['email'])
        self.assertIn('/persons/1', response.json['_links']['self'])

    def test_empty_post(self):
        """ POST /persons/ without any data should return HTTP 400 """

        response = self.client.post('/persons/')

        self.assert400(response)
        self.assertEqual('No data given to create Person',
                         response.json['message'])

    def test_junk_post(self):
        """ POST /persons/ with junk data should return HTTP 400 """

        response = self.client.post('/persons/', data='{"x": "y"}',
                                    content_type='application/json')

        self.assert400(response)
        self.assertIn('Unable to save Person', response.json['message'])

    def test_create(self):
        """
        POST /persons/ with valid data should return HTTP 201 and create the
        record in db
        """

        data = {
            'first_name': 'First 1',
            'last_name': 'Last 1',
            'email': 'email@test.com'
        }

        response = self.client.post('/persons/', data=json.dumps(data),
                                    content_type='application/json')

        self.assert201(response)

    def test_get_all_not_implemented(self):
        """ /persons/ resource doesn't implement HTTP GET """

        response = self.client.get('/persons/')

        self.assert405(response)
