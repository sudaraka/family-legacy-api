""" Tests for /legacy/<id>/members API """

import json

from .base import BaseCase


class LegacyMembersTest(BaseCase):
    """ /legacy/<id>/members test case """

    def test_empty_post_error(self):
        """ POST /legacy/1/members with empty request must return HTTP 400 """

        self.create_person()

        self.client.put('/persons/1/pay')

        response = self.client.post('/legacy/1/members')

        self.assert400(response)
        self.assertEqual('"members" was not specified',
                         response.json['message'])

    def test_junk_post(self):
        """
        POST /legacy/1/members without a list of members must return HTTP 400
        """

        self.create_person()

        self.client.put('/persons/1/pay')

        response = self.client.post('/legacy/1/members', data='{"members":""}',
                                    content_type='application/json')

        self.assert400(response)
        self.assertEqual('"members" was not a valid list',
                         response.json['message'])

    def test_non_existing_member_id_error(self):
        """
        POST /legacy/1/members with non-existing member id must return HTTP 400
        """

        self.create_person()
        self.create_person()

        self.client.put('/persons/1/pay')

        data = {
            'members': [2, 4]
        }

        response = self.client.post('/legacy/1/members', data=json.dumps(data),
                                    content_type='application/json')

        self.assert400(response)
        self.assertEqual('Member not found',
                         response.json['message'])

    def test_non_existing_member_email_works(self):
        """
        POST /legacy/1/members with non-existing member email should complete
        successfully.
        """

        self.create_person()
        self.create_person()

        self.client.put('/persons/1/pay')

        data = {
            'members': ['Test email2', 'Test email4']
        }

        response = self.client.post('/legacy/1/members', data=json.dumps(data),
                                    content_type='application/json')

        # TODO: although this return as success, we need additional tests to
        # verify that new (non-existing) user invitation was invoked
        self.assert200(response)

    def test_can_add_member_by_id(self):
        """ POST /legacy/1/members can add members by id """

        self.create_person()
        self.create_person()
        self.create_person()
        self.create_person()

        self.client.put('/persons/1/pay')

        data = {
            'members': [2, 4]
        }

        response = self.client.post('/legacy/1/members', data=json.dumps(data),
                                    content_type='application/json')

        self.assert200(response)

    def test_can_add_member_by_email(self):
        """ POST /legacy/1/members can add members by email address """

        self.create_person()
        self.create_person()
        self.create_person()
        self.create_person()

        self.client.put('/persons/1/pay')

        data = {
            'members': ['Test email3', 4]
        }

        response = self.client.post('/legacy/1/members', data=json.dumps(data),
                                    content_type='application/json')

        self.assert200(response)
