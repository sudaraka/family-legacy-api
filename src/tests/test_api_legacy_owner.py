""" Tests for /legacy/<id>/owner API """

from .base import BaseCase


class LegacyOwnerTest(BaseCase):
    """ /legacy/<id>/owner test case """

    def test_get_existing(self):
        """ GET /legacy/1/owner must return owner's public information """

        self.create_person(avatar='http://avatar.com/test.jpg')

        self.client.put('/persons/1/pay')

        response = self.client.get('/legacy/1/owner')

        self.assert200(response)
        self.assertEqual('Test first_name', response.json['first_name'])
        self.assertEqual('Test last_name', response.json['last_name'])
        self.assertEqual('Test email', response.json['email'])
        self.assertEqual('http://avatar.com/test.jpg', response.json['avatar'])

    def test_no_private_fields(self):
        """ GET /legacy/1/owner must NOT return owner's private information """

        self.create_person()

        self.client.put('/persons/1/pay')

        response = self.client.get('/legacy/1/owner')

        self.assert200(response)
        self.assertNotIn('status', response.json)
        self.assertNotIn('_links', response.json)
