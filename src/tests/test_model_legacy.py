""" Tests for Legacy Model """

from . import BaseCase
from ..app.models import Person, Legacy
from ..app.exceptions import IncompleteData, IncorrectData


class LegacyTest(BaseCase):
    """ Legacy model test case """

    def test_can_create(self):
        """ Legacy model created with default values """

        l = Legacy()

        # Every thing should be None
        self.assertEqual(None, l.status)
        self.assertEqual(None, l.lock_date)
        self.assertEqual(None, l.archive_hash)
        self.assertEqual(None, l.owner)
        self.assertEqual(None, l.owner_id)
        self.assertEqual(None, l.caretaker)
        self.assertEqual(None, l.caretaker_id)
        self.assertEqual([], l.members)

    def test_can_not_save_empty_name(self):
        """ Legacy object with empty owner can't be saved to db """

        l = Legacy()

        with self.assertRaises(IncompleteData):
            l.save()

    def test_save_legacy(self):
        """
        Saving legacy record successfully updates id and set status to default
        """

        p = self.get_person()

        l = Legacy(owner=p)
        l.save()

        self.assertEqual(1, l.id)
        self.assertEqual('LOCKED', l.status)

    def test_unique_owner(self):
        """ Legacy's owner must be unique across the system """

        p = self.get_person()

        l1 = Legacy(owner=p)
        l1.save()

        l2 = Legacy(owner=p)
        with self.assertRaises(IncompleteData):
            l2.save()

    def test_hide_owner_fields_in_serialization(self):
        """
        Owner fields must not be available in serialized versions of the object
        """

        p = self.get_person()

        l = Legacy(owner=p)
        l.save()

        d = l.to_dict()

        self.assertFalse('owner' in d)
        self.assertFalse('owner_id' in d)

    def test_hide_caretaker_fields_in_serialization(self):
        """
        Caretaker fields must not be available in serialized versions of the
        object
        """

        p = self.get_person()

        l = Legacy(owner=p)
        l.save()

        d = l.to_dict()

        self.assertFalse('caretaker' in d)
        self.assertFalse('caretaker_id' in d)

    def test_from_dict_must_ignore_id(self):
        """
        When dictionary with "id" field passed into Legacy.from_dict, it must
        not change the instance value
        """

        p = self.get_person()

        l = Legacy()
        l.from_dict({'id': 500, 'owner_id': p.id})

        self.assertIsNone(l.id)
        self.assertEquals(p.id, l.owner_id)

    def get_person(self):  # pylint: disable=I0011,R0201
        """ Create new person object and return it """

        return Person(first_name='Test First Name', last_name='Test Last Name',
                      username='Test_User', email='Test Email')
