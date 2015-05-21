""" Tests for API caching functions """

from . import BaseCase


class CachingTest(BaseCase):
    """ Caching test case """

    P1_ETAG = 'e8259b42dfd55a8130662194107b2929'

    def test_no_etag_in_404(self):
        """ 404 (or any error) response must not have an Etag """

        response = self.client.get('/persons/1')

        self.assert404(response)

        self.assertNotIn('ETag', response.headers)

    def test_etag_match(self):
        """
        With If-Match header set only response with matching ETag should return
        """

        self.create_persons()

        response = self.client.get('/persons/1', headers={
            'If-Match': '"{}"'.format(self.P1_ETAG)
        })

        self.assert200(response)

        response = self.client.get('/persons/1', headers={
            'If-Match': '"bad-tag"'
        })

        self.assertEqual(412, response.status_code)

    def test_etag_none_match(self):
        """
        With If-None-Match header set only response with non-matching ETag
        should return
        """

        self.create_persons()

        response = self.client.get('/persons/1', headers={
            'If-None-Match': '"{}"'.format(self.P1_ETAG)
        })

        self.assertEqual(304, response.status_code)

        response = self.client.get('/persons/1', headers={
            'If-None-Match': '"bad-tag"'
        })

        self.assert200(response)

        response = self.client.get('/persons/2', headers={
            'If-None-Match': '"{}"'.format(self.P1_ETAG)
        })

        self.assert200(response)

    def create_persons(self):
        """ Create a temporary test record """

        self.create_resource('/persons/', {
            'first_name': 'P1 First Name',
            'last_name': 'P1 Last Name',
            'email': 'P1 Email',
            'username': 'P1_User'
        })

        self.create_resource('/persons/', {
            'first_name': 'P2 First Name',
            'last_name': 'P2 Last Name',
            'email': 'P2 Email',
            'username': 'P2_User'
        })
