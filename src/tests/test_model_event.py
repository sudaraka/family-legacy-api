""" Tests for Event Model """

from . import BaseCase
from ..app.models import Person, Legacy, Event
from ..app.exceptions import IncompleteData, IncorrectData


class LegacyTest(BaseCase):
    """ Event model test case """

    person_count = 0

    def test_can_create(self):
        """ Event model created with default values """

        e = Event()

        # Every thing should be None
        self.assertEqual(None, e.status)
        self.assertEqual(None, e.name)
        self.assertEqual(None, e.description)
        self.assertEqual(None, e.month)
        self.assertEqual(None, e.day)
        self.assertEqual(None, e.legacy)
        self.assertEqual(None, e.legacy_id)
        self.assertEqual([], e.messages)
        self.assertEqual([], e.photos)

    def test_can_not_save_empty_name(self):
        """
        Event object with empty legacy, name, month or day can't be saved to db
        """

        e = Event()

        with self.assertRaises(IncompleteData):
            e.save()

    def test_save_event(self):
        """
        Saving legacy record successfully updates id and set status to default
        """

        e = Event(name='Test Event', month=6, day=15, legacy=self.get_legacy())
        e.save()

        self.assertEqual(1, e.id)
        self.assertEqual('ENABLED', e.status)

    def test_hide_legacy_fields_in_serialization(self):
        """
        Legacy fields must not be available in serialized versions of the object
        """

        e = Event(name='Test Event', month=6, day=15, legacy=self.get_legacy())
        e.save()

        d = e.to_dict()

        self.assertFalse('legacy' in d)
        self.assertFalse('legacy_id' in d)

    def test_hide_desc_and_legacy_fields_in_public_only_serialization(self):
        """
        Description and legacy (link) fields must not be available in
        public_only serialized versions of the object
        """

        e = Event(name='Test Event', month=6, day=15, legacy=self.get_legacy(),
                  description='Test Description')
        e.save()

        d = e.to_dict(public_only=True)

        self.assertFalse('description' in d)
        self.assertFalse('legacy' in d['_links'])

    def test_show_legacy_url_in_serialization(self):
        """ Serialized event must show URL to the legacy in _links """

        e = Event(name='Test Event', month=6, day=15, legacy=self.get_legacy())
        e.save()

        d = e.to_dict()

        self.assertTrue('legacy' in d['_links'])
        self.assertIn('/legacy/1', d['_links']['legacy'])

    def test_from_dict_must_ignore_id(self):
        """
        When dictionary with "id" field passed into Legacy.from_dict, it must
        not change the instance value
        """

        l = self.get_legacy()

        e = Event()

        e.from_dict({'id': 500, 'legacy_id': l.id})

        self.assertIsNone(e.id)
        self.assertEquals(e.legacy_id, l.id)

    def test_from_dict_can_not_pass_invalid_status(self):
        """
        When dictionary with "status" field passed into Event.from_dict, it
        must contains an acceptable value
        """

        l = self.get_legacy()

        e = Event()

        with self.assertRaises(IncorrectData):
            e.from_dict({'status': 'NOT_VALID', 'legacy_id': l.id})

    def get_person(self):  # pylint: disable=I0011,R0201
        """ Create new person object and return it """

        self.person_count += 1

        return Person(first_name='Test First Name', last_name='Test Last Name',
                      username='Test_User_{}'.format(self.person_count),
                      email='Test Email')

    def get_legacy(self):  # pylint: disable=I0011,R0201
        """ Create new person object and return it """

        return Legacy(owner=self.get_person())
