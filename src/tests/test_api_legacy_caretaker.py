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

    def test_empty_put_error(self):
        """ PUT /legacy/1/caretaker with empty request must return HTTP 400 """

        self.create_legacy()

        response = self.client.put('/legacy/1/caretaker')

        self.assert400(response)
        self.assertEqual('"caretaker" was not specified',
                         response.json['message'])

    def test_non_existing_caretaker_id_error(self):
        """
        PUT /legacy/1/caretaker with non-existing member id must return HTTP 400
        """

        self.create_legacy()

        data = {
            'caretaker': 4
        }

        response = self.client.put('/legacy/1/caretaker', data=json.dumps(data),
                                   content_type='application/json')

        self.assert400(response)
        self.assertEqual('Caretaker not found',
                         response.json['message'])

    def test_non_existing_caretaker_email_works(self):
        """
        PUT /legacy/1/caretaker with non-existing member email should complete
        successfully.
        """

        self.create_legacy()

        data = {
            'caretaker': 'Test email4'
        }

        response = self.client.put('/legacy/1/caretaker', data=json.dumps(data),
                                   content_type='application/json')

        # TODO: although this return as success, we need additional tests to
        # verify that new (non-existing) user invitation was invoked
        self.assert202(response)

    def test_can_add_caretaker_by_id(self):
        """ PUT /legacy/1/caretaker can add caretaker by id """

        self.create_legacy()

        data = {
            'caretaker': 3
        }

        response = self.client.put('/legacy/1/caretaker', data=json.dumps(data),
                                   content_type='application/json')

        self.assert200(response)

    def test_can_add_caretaker_by_email(self):
        """ PUT /legacy/1/caretaker can add caretaker by email """

        self.create_legacy()

        data = {
            'caretaker': 'Test email3'
        }

        response = self.client.put('/legacy/1/caretaker', data=json.dumps(data),
                                   content_type='application/json')

        self.assert200(response)

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

    def test_can_delete_caretaker(self):
        """ DELETE /legacy/1/caretaker can remove caretaker """

        self.create_legacy(True)

        response = self.client.delete('/legacy/1/caretaker')

        self.assert200(response)

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
