""" Tests for Person Model """

from . import BaseCase
from ..app.models import Person
from ..app.exceptions import IncompleteData


class PersonTest(BaseCase):
    """ Person model test case """

    def test_can_create(self):
        """ Person model created with default values """

        p = Person()

        # Every thing should be None
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
                   email='Test Email')

        p.save()

        self.assertEqual(1, p.id)
        self.assertEqual('UNPAID', p.status)
        self.assertEqual('Test First Name', p.first_name)
        self.assertEqual('Test Last Name', p.last_name)
        self.assertEqual('Test Email', p.email)
