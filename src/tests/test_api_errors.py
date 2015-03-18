""" Tests for API error handling """

from . import BaseCase


class ErrorsTest(BaseCase):
    """ Errors test case """

    def test_404(self):
        """ Invalid URLs must generate 404 error """

        response = self.client.get('/v1/bad-url/')

        self.assert404(response)
        self.assertEqual('not found', response.json['error'])
