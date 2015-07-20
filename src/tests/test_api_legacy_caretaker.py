""" Tests for /legacy/<id>/caretaker API """

import json

from .base import BaseCase


class LegacyCaretakerTest(BaseCase):
    """ /legacy/<id>/caretaker test case """

    def test_get_non_existing(self):
        """
        GET /legacy/1/caretaker when caretaker not assigned must return HTTP 404
        """

        self.create_legacy()

        response = self.client.get('/legacy/1/caretaker')

        self.assert404(response)

    def test_get_existing(self):
        """
        GET /legacy/1/caretaker must return caretaker's public information
        """

        self.create_legacy(True)

        response = self.client.get('/legacy/1/caretaker')

        self.assert200(response)
        self.assertEqual('Test first_name3', response.json['first_name'])
        self.assertEqual('Test last_name3', response.json['last_name'])
        self.assertEqual('Test email3', response.json['email'])

    def test_no_private_fields(self):
        """
        GET /legacy/1/caretaker must NOT return caretaker's private information
        """

        self.create_legacy(True)

        response = self.client.get('/legacy/1/caretaker')

        self.assert200(response)

        self.assertNotIn('status', response.json)
        self.assertNotIn('_links', response.json)

    def create_legacy(self, with_caretaker=False):
        """
        Create records to test:
            - 3 Persons
            - Legacy owned by person 1
            - Assign Person #3 as caretaker if the flag is set
        """

        self.create_person()
        self.create_person()
        self.create_person()

        self.client.put('/persons/1/pay')

        if with_caretaker:
            data = {
                'caretaker': 3
            }

            self.client.put('/legacy/1/caretaker', data=json.dumps(data),
                            content_type='application/json')
