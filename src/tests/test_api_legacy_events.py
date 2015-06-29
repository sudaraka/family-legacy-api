""" Tests for /legacy/<id>/events API """

import json

from .base import BaseCase


class LegacyEventTest(BaseCase):
    """ /legacy/<id>/events test case """

    event_count = 0

    def setUp(self):
        """ Setup test case """

        BaseCase.setUp(self)

        self.create_person()
        self.client.put('/persons/1/pay')

    def test_bad_legacy(self):
        """
        Any HTTP operation on /legacy/1/events with non-existing legacy must
        return HTTP 404
        """

        response = self.client.post('/legacy/2/events')
        self.assert404(response)

    def test_empty_post(self):
        """ POST /legacy/1/events without any data should return HTTP 400 """

        response = self.client.post('/legacy/1/events')

        self.assert400(response)
        self.assertEqual('No data given to create Event',
                         response.json['message'])

    def test_junk_post(self):
        """ POST /legacy/1/events with junk data should return HTTP 400 """

        response = self.client.post('/legacy/1/events', data='{"x": "y"}',
                                    content_type='application/json')

        self.assert400(response)
        self.assertIn('Unable to save Event', response.json['message'])

    def test_create(self):
        """
        POST /legacy/1/events with valid data should return HTTP 201 and create
        the record in db
        """

        response = self.create_event(1)

        self.assert201(response)
        self.assertIn('/legacy/1/events/1', response.headers['location'])

    def create_event(self, legacy_id, **kwargs):
        """ Create a temporary test event record """

        self.event_count += 1

        for field in ['name', 'month', 'day', 'description']:
            if field not in kwargs:
                if 'day' == field:
                    kwargs['day'] = 29
                elif 'month' == field:
                    kwargs['month'] = 6
                else:
                    kwargs[field] = 'Test {}{}'.format(field,
                                                       str(self.event_count))

        return self.client.post('/legacy/{}/events'.format(legacy_id),
                                data=json.dumps(kwargs),
                                content_type='application/json')
