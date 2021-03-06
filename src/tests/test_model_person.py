""" Tests for Person Model """

from .base import BaseCase
from ..app.models import Person, Legacy
from ..app.exceptions import IncompleteData, AccessViolation, IncorrectData


class PersonTest(BaseCase):
    """ Person model test case """

    def test_can_create(self):
        """ Person model created with default values """

        p = Person()

        # Every thing should be None
        self.assertEqual(None, p.username)
        self.assertEqual(None, p.status)
        self.assertEqual(None, p.first_name)
        self.assertEqual(None, p.last_name)
        self.assertEqual(None, p.email)

    def test_can_not_save_empty_name(self):
        """ Person object with empty first, last name can't be saved to db """

        p = Person()

        with self.assertRaises(IncompleteData):
            p.save()

    def test_save_person(self):
        """
        Saving person record successfully updates id and set status to default
        """

        p = Person(first_name='Test First Name', last_name='Test Last Name',
                   username='Test_User', email='Test Email')

        p.save()

        self.assertEqual(1, p.id)
        self.assertEqual('UNPAID', p.status)
        self.assertEqual('Test First Name', p.first_name)
        self.assertEqual('Test Last Name', p.last_name)
        self.assertEqual('Test_User', p.username)
        self.assertEqual('Test Email', p.email)

    def test_unique_username(self):
        """ Person's username must be unique across the system """

        p1 = Person(first_name='original', last_name='person', email='email',
                    username='user')
        p1.save()

        p2 = Person(first_name='duplicate', last_name='person', email='email',
                    username='user')
        with self.assertRaises(IncompleteData):
            p2.save()

    def test_password_is_not_readable(self):
        """
        Person password must not be readable
        """

        p = Person()

        with self.assertRaises(AccessViolation):
            print(p.password)  # pylint: disable=I0011,C0325

    def test_password_hashing(self):
        """
        Assigning a password generates a hash of it
        """

        p = Person()

        self.assertIsNone(p.password_hash)

        p.password = 'ubersecret'

        self.assertIsNotNone(p.password_hash)

    def test_password_verify(self):
        """
        Assigning a password generates a hash of it
        """

        p = Person()
        p.password = 'ubersecret'

        self.assertFalse(p.verify_password('lamepw'))
        self.assertTrue(p.verify_password('ubersecret'))

    def test_hide_password_fields_in_serialization(self):
        """
        Password or hash fields must not be available in serialized versions of
        the object
        """

        p = Person(first_name='First', last_name='Last', email='Email',
                   username='User')
        p.save()

        d = p.to_dict()

        self.assertFalse('password' in d)
        self.assertFalse('password_hash' in d)

    def test_hide_username_field_in_serialization(self):
        """
        Username field must not be available in serialized versions of the
        object
        """

        p = Person(first_name='First', last_name='Last', email='Email',
                   username='User')
        p.save()

        d = p.to_dict()

        self.assertFalse('username' in d)

    def test_hide_status_field_in_public_only_serialization(self):
        """
        Status field must not be available in public_only serialized versions of
        the object
        """

        p = Person(first_name='First', last_name='Last', email='Email',
                   username='User', status='ACTIVE')
        p.save()

        d = p.to_dict(public_only=True)

        self.assertFalse('status' in d)

    def test_hide_resource_links_in_public_only_serialization(self):
        """
        Links to related resources must not be available in public_only
        serialized versions of the object
        """

        p = Person(first_name='First', last_name='Last', email='Email',
                   username='User', status='ACTIVE')
        p.save()

        d = p.to_dict(public_only=True)

        self.assertFalse('_links' in d)

    def test_show_legacy_url_in_serialization(self):
        """
        Serialized person with legacy assigned must show URL to the legacy in
        _links
        """

        p = Person(first_name='First', last_name='Last', email='Email',
                   username='User')
        Legacy(owner=p)

        p.save()

        d = p.to_dict()

        self.assertTrue('legacy' in d['_links'])
        self.assertIn('/legacy/1', d['_links']['legacy'])

    def test_from_dict_must_ignore_id(self):
        """
        When dictionary with "id" field passed into Person.from_dict, it must
        not change the instance value
        """

        p = Person()
        p.from_dict({'id': 500, 'email': 'test email'})

        self.assertIsNone(p.id)
        self.assertEquals('test email', p.email)

    def test_from_dict_can_not_pass_invalid_status(self):
        """
        When dictionary with "status" field passed into Person.from_dict, it
        must contains an acceptable value
        """

        p = Person()

        with self.assertRaises(IncorrectData):
            p.from_dict({'status': 'NOT_VALID', 'email': 'test email'})
