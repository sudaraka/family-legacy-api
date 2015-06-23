""" Tests for /persons/ API """

import json

from datetime import datetime

from .base import BaseCase
from ..app.models import Legacy


class PersonsTest(BaseCase):
    """ /persons/ test case """

    user_count = 0

    def test_get_non_existing(self):
        """ GET /persons/1 on empty DB must return HTTP 404 """

        response = self.client.get('/persons/1')

        self.assert404(response)
        self.assertEqual('not found', response.json['error'])

    def test_get_existing(self):
        """ GET /persons/1 on DB with valid record must return it """

        self.create_person()

        response = self.client.get('/persons/1')

        self.assert200(response)
        self.assertEqual('UNPAID', response.json['status'])
        self.assertEqual('Test first_name', response.json['first_name'])
        self.assertEqual('Test last_name', response.json['last_name'])
        self.assertEqual('Test email', response.json['email'])
        self.assertIn('/persons/1', response.json['_links']['self'])

    def test_empty_post(self):
        """ POST /persons/ without any data should return HTTP 400 """

        response = self.client.post('/persons/')

        self.assert400(response)
        self.assertEqual('No data given to create Person',
                         response.json['message'])

    def test_junk_post(self):
        """ POST /persons/ with junk data should return HTTP 400 """

        response = self.client.post('/persons/', data='{"x": "y"}',
                                    content_type='application/json')

        self.assert400(response)
        self.assertIn('Unable to save Person', response.json['message'])

    def test_create(self):
        """
        POST /persons/ with valid data should return HTTP 201 and create the
        record in db
        """

        data = {
            'first_name': 'First 1',
            'last_name': 'Last 1',
            'email': 'email@test.com',
            'username': 'user1'
        }

        response = self.client.post('/persons/', data=json.dumps(data),
                                    content_type='application/json')

        self.assert201(response)

    def test_get_all_not_implemented(self):
        """ /persons/ resource doesn't implement HTTP GET """

        response = self.client.get('/persons/')

        self.assert405(response)

    def test_edit_non_existing(self):
        """ PUT /persons/1 on empty DB must return HTTP 404 """

        response = self.client.put('/persons/1')

        self.assert404(response)
        self.assertEqual('not found', response.json['error'])

    def test_edit_existing(self):
        """ PUT /persons/1 on DB with valid record must modify it """

        self.create_person()

        changes = {
            'first_name': 'Modified First Name',
            'last_name': 'Modified Last Name',
            'email': 'Modified Email'
        }

        response = self.client.put('/persons/1', data=json.dumps(changes),
                                   content_type='application/json')
        self.assert200(response)

        p = self.get_resource('/persons/1')

        self.assertEqual('Modified First Name', p['first_name'])
        self.assertEqual('Modified Last Name', p['last_name'])
        self.assertEqual('Modified Email', p['email'])
        self.assertIn('/persons/1', p['_links']['self'])

    def test_pay_non_existing(self):
        """ PUT /persons/1/pay on empty DB must return HTTP 404 """

        response = self.client.put('/persons/1/pay')

        self.assert404(response)
        self.assertEqual('not found', response.json['error'])

    def test_only_active_or_unpaied_person_can_pay(self):
        """
        PUT /persons/1/pay while person status is nether ACTIVE not UNPAID
        should return HTTP 400
        """

        self.create_person(status='DISABLED')

        response = self.client.put('/persons/1/pay')

        self.assert405(response)
        self.assertIn('Current user is not allowed to make a payment',
                      response.json['message'])

        self.create_person(status='DECEASED')

        response = self.client.put('/persons/2/pay')

        self.assert405(response)
        self.assertIn('Current user is not allowed to make a payment',
                      response.json['message'])

    def test_pay_activate_person(self):
        """ PUT /persons/1/pay must set person status to ACTIVE """

        self.create_person(status='UNPAID')

        self.client.put('/persons/1/pay')

        response = self.client.get('/persons/1')
        self.assertEqual('ACTIVE', response.json['status'])

    def test_pay_create_new_legacy(self):
        """
        PUT /persons/1/pay on when person doesn't have a legacy should create
        new one
        """

        self.create_person()

        self.client.put('/persons/1/pay')

        response = self.client.get('/legacy/1')

        self.assert200(response)
        self.assertEqual('ACTIVE', response.json['status'])

        lock_date = datetime.strptime(response.json['lock_date'],
                                      '%a, %d %b %Y %H:%M:%S %Z')
        lock_date -= datetime.now()

        self.assertLessEqual(
            abs(self.app.config.get('LEGACY_EXTEND_DAYS') - lock_date.days), 1
        )

    def test_pay_update_existing_legacy(self):
        """
        PUT /persons/1/pay on when person have a legacy should update it
        """

        self.create_person()
        l = Legacy(owner_id=1, status='LOCKED')
        l.save()

        self.client.put('/persons/1/pay')

        response = self.client.get('/legacy/1')

        self.assertEqual('ACTIVE', response.json['status'])

        lock_date = datetime.strptime(response.json['lock_date'],
                                      '%a, %d %b %Y %H:%M:%S %Z')
        lock_date -= datetime.now()

        self.assertLessEqual(
            abs(self.app.config.get('LEGACY_LOCK_DAYS') - lock_date.days), 1
        )

        self.client.put('/persons/1/pay')
        response = self.client.get('/legacy/1')

        lock_date = datetime.strptime(response.json['lock_date'],
                                      '%a, %d %b %Y %H:%M:%S %Z')
        lock_date -= datetime.now()

        self.assertLessEqual(
            abs(self.app.config.get('LEGACY_LOCK_DAYS') * 2 - lock_date.days), 1
        )

    def create_person(self, **kwargs):
        """ Create a temporary test person record """

        self.user_count += 1

        for field in ['first_name', 'last_name', 'email', 'username']:
            if field not in kwargs:
                kwargs[field] = 'Test {}'.format(field)

        kwargs['username'] += str(self.user_count)

        return self.create_resource('/persons/', kwargs)
