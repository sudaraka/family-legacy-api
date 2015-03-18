""" Tests for main app components """

from . import BaseCase


class AppTest(BaseCase):
    """ App component test case """

    def test_home(self):
        """ API home url must render the homepage template """

        response = self.client.get('/')

        self.assert200(response)
        self.assertTemplateUsed('index.html')
