""" Tests for /auth/* API """

from . import BaseCase


class AuthBaseTest(BaseCase):
    """ /auth/* test case """

    def test_get_non_existing(self):
        """ GET /auth/nx-resource on empty DB must return HTTP 404 """

        response = self.client.get('/auth/non-existing-resource')

        self.assert404(response)
        self.assertEqual('not found', response.json['error'])
