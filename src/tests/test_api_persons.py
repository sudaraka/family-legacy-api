""" Tests for /persons/ API """

from . import BaseCase
from ..app import db
from ..app.models import Person


class PersonsTest(BaseCase):
    """ /persons/ test case """

    def test_get_non_existing(self):
        """ GET /v1/persons/1 on empty DB must return HTTP 404 """

        response = self.client.get('/v1/persons/1')

        self.assert404(response)
        self.assertEqual('not found', response.json['error'])

    def test_get_existing(self):
        """ GET /v1/persons/1 on DB with valid record must return it """

        p = Person(first_name='Test First Name', last_name='Test Last Name',
                   email='Test Email')

        db.session.add(p)
        db.session.commit()

        response = self.client.get('/v1/persons/1')

        self.assert200(response)
        self.assertEqual(1, response.json['id'])
        self.assertEqual('UNPAID', response.json['status'])
        self.assertEqual('Test First Name', response.json['first_name'])
        self.assertEqual('Test Last Name', response.json['last_name'])
        self.assertEqual('Test Email', response.json['email'])
        self.assertIn('/v1/persons/1', response.json['_links']['self'])
