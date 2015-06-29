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

        response = self.client.get('/legacy/2/events')
        self.assert404(response)

        response = self.client.get('/legacy/2/events/1')
        self.assert404(response)

        response = self.client.put('/legacy/2/events/1')
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

    def test_get_non_existing(self):
        """ GET /legacy/1/events on empty DB must return HTTP 404 """

        response = self.client.get('/legacy/1/events/1')

        self.assert404(response)
        self.assertEqual('not found', response.json['error'])

    def test_get_existing(self):
        """
        GET /legacy/1/events/1 on DB with valid record must return it
        """

        self.create_event(1)

        response = self.client.get('/legacy/1/events/1')

        self.assert200(response)
        self.assertEqual('ENABLED', response.json['status'])
        self.assertEqual('Test name1', response.json['name'])
        self.assertEqual('Test description1', response.json['description'])
        self.assertEqual(6, response.json['month'])
        self.assertEqual(29, response.json['day'])
        self.assertIn('/legacy/1', response.json['_links']['legacy'])
        self.assertIn('/legacy/1/events/1', response.json['_links']['self'])

    def test_get_all(self):
        """
        GET /legacy/1/events on DB with valid records must return all of them
        """

        self.create_event(1)
        self.create_event(1)
        self.create_event(1)
        self.create_event(1)

        response = self.client.get('/legacy/1/events')

        self.assert200(response)

        for e in response.json['events']:
            i = response.json['events'].index(e) + 1

            self.assertEqual('ENABLED', e['status'])
            self.assertEqual('Test name{}'.format(i), e['name'])
            self.assertEqual(6, e['month'])
            self.assertEqual(29, e['day'])
            self.assertIn('/legacy/1/events/{}'.format(i), e['_links']['self'])

            self.assertNotIn('description', e)
            self.assertNotIn('legacy', e['_links'])

    def test_edit_non_existing(self):
        """ PUT /legacy/1/events/1 on empty DB must return HTTP 404 """

        response = self.client.put('/legacy/1/events/1')

        self.assert404(response)
        self.assertEqual('not found', response.json['error'])

    def test_edit_existing(self):
        """ PUT /legacy/1/events/1 on DB with valid record must modify it """

        self.create_event(1)

        changes = {
            'name': 'Modified Name',
            'description': 'Modified Description',
            'month': 5,
            'day': 23
        }

        response = self.client.put('/legacy/1/events/1',
                                   data=json.dumps(changes),
                                   content_type='application/json')
        self.assert200(response)

        e = self.get_resource('/legacy/1/events/1')

        self.assertEqual('Modified Name', e['name'])
        self.assertEqual('Modified Description', e['description'])
        self.assertEqual(5, e['month'])
        self.assertEqual(23, e['day'])
        self.assertIn('/legacy/1/events/1', e['_links']['self'])

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
