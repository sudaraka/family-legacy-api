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

    def test_get_existing(self):
        """
        GET /legacy/1/members must return public information of all members
        """

        self.create_person(avatar='http://avatar.com/test1.jpg')
        self.create_person(avatar='http://avatar.com/test2.jpg')
        self.create_person(avatar='http://avatar.com/test3.jpg')
        self.create_person(avatar='http://avatar.com/test4.jpg')

        self.client.put('/persons/1/pay')

        data = {
            'members': [2, 4]
        }

        self.client.post('/legacy/1/members', data=json.dumps(data),
                         content_type='application/json')

        response = self.client.get('/legacy/1/members')

        self.assert200(response)

        self.assertEqual(2, len(response.json['members']))

        m = response.json['members'][0]
        self.assertEqual('Test first_name2', m['first_name'])
        self.assertEqual('Test last_name2', m['last_name'])
        self.assertEqual('Test email2', m['email'])
        self.assertEqual('http://avatar.com/test2.jpg', m['avatar'])

        m = response.json['members'][1]
        self.assertEqual('Test first_name4', m['first_name'])
        self.assertEqual('Test last_name4', m['last_name'])
        self.assertEqual('Test email4', m['email'])
        self.assertEqual('http://avatar.com/test4.jpg', m['avatar'])

    def test_no_private_fields(self):
        """
        GET /legacy/1/members must NOT return member's private information
        """

        self.create_person()
        self.create_person()

        self.client.put('/persons/1/pay')

        self.client.post('/legacy/1/members', data='{"members":[2]}',
                         content_type='application/json')

        response = self.client.get('/legacy/1/members')

        self.assert200(response)

        m = response.json['members'][0]
        self.assertNotIn('status', m)
        self.assertNotIn('_links', m)
