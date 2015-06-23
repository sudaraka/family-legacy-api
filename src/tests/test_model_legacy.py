""" Tests for Legacy Model """

from .base import BaseCase
from ..app.models import Person, Legacy
from ..app.exceptions import IncompleteData, IncorrectData


class LegacyTest(BaseCase):
    """ Legacy model test case """

    person_count = 0

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

        p1 = self.get_person()
        p2 = self.get_person()

        l = Legacy(owner=p1, caretaker=p2)
        l.save()

        d = l.to_dict()

        self.assertFalse('caretaker' in d)
        self.assertFalse('caretaker_id' in d)

    def test_show_owner_url_in_serialization(self):
        """
        Serialized legacy must show URL to the owner, caretaker, members and
        events in _links
        """

        p = self.get_person()

        l = Legacy(owner=p)
        l.save()

        d = l.to_dict()

        for resource in ['owner', 'caretaker', 'members', 'events']:
            self.assertTrue(resource in d['_links'])
            self.assertIn('/legacy/1/{}'.format(resource),
                          d['_links'][resource])

    def test_owner_can_modify_active_legacy_only(self):
        """
        Owner can only modify legacy as long as it is in ACTIVE state.
        """

        p = self.get_person()
        l = Legacy(owner=p)
        l.save()

        l.status = 'ACTIVE'
        self.assertTrue(l.can_modify(p.id))

        l.status = 'LOCKED'
        self.assertFalse(l.can_modify(p.id))

        l.status = 'LEGEND'
        self.assertFalse(l.can_modify(p.id))

    def test_caretaker_can_modify_legacy_when_owner_is_deceased(self):
        """
        Caretaker can only modify legacy when the owner status is DECEASED
        """

        p1 = self.get_person()
        p2 = self.get_person()
        l = Legacy(owner=p1, caretaker=p2)
        l.save()

        l.status = 'ACTIVE'
        self.assertFalse(l.can_modify(p2.id))

        l.status = 'LOCKED'
        self.assertFalse(l.can_modify(p2.id))

        l.status = 'LEGEND'
        self.assertFalse(l.can_modify(p2.id))

        p1.status = 'DECEASED'

        l.status = 'ACTIVE'
        self.assertTrue(l.can_modify(p2.id))

        l.status = 'LOCKED'
        self.assertTrue(l.can_modify(p2.id))

        l.status = 'LEGEND'
        self.assertFalse(l.can_modify(p2.id))

    def test_members_can_not_modify_legacy(self):
        """ Members can NOT modify legacy in any state """

        p1 = self.get_person()
        p2 = self.get_person()
        p3 = self.get_person()
        l = Legacy(owner=p1, caretaker=p2)
        l.members.append(p3)

        l.save()

        l.status = 'ACTIVE'
        self.assertFalse(l.can_modify(p3.id))

        l.status = 'LOCKED'
        self.assertFalse(l.can_modify(p3.id))

        l.status = 'LEGEND'
        self.assertFalse(l.can_modify(p3.id))

    def test_unrelated_person_can_not_modify_legacy(self):
        """ Any unrelated person can NOT modify legacy in any state """

        p1 = self.get_person()
        p2 = self.get_person()
        p3 = self.get_person()
        p4 = self.get_person()  # Not related to this Legacy
        l = Legacy(owner=p1, caretaker=p2)
        l.members.append(p3)

        l.save()

        l.status = 'ACTIVE'
        self.assertFalse(l.can_modify(p4.id))

        l.status = 'LOCKED'
        self.assertFalse(l.can_modify(p4.id))

        l.status = 'LEGEND'
        self.assertFalse(l.can_modify(p4.id))

    def test_everyone_except_unrelated_person_can_view_legacy(self):
        """ Everyone except unrelated person can view legacy """

        p1 = self.get_person()
        p2 = self.get_person()
        p3 = self.get_person()
        p4 = self.get_person()  # Not related to this Legacy
        l = Legacy(owner=p1, caretaker=p2)
        l.members.append(p3)

        l.save()

        self.assertTrue(l.can_view(p1.id))
        self.assertTrue(l.can_view(p2.id))
        self.assertTrue(l.can_view(p3.id))

        self.assertFalse(l.can_view(p4.id))

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

    def test_from_dict_can_not_pass_invalid_status(self):
        """
        When dictionary with "status" field passed into Legacy.from_dict, it
        must contains an acceptable value
        """

        p = self.get_person()

        l = Legacy()

        with self.assertRaises(IncorrectData):
            l.from_dict({'status': 'NOT_VALID', 'owner_id': p.id})

    def get_person(self):  # pylint: disable=I0011,R0201
        """ Create new person object and return it """

        self.person_count += 1

        return Person(first_name='Test First Name', last_name='Test Last Name',
                      username='Test_User_{}'.format(self.person_count),
                      email='Test Email')
