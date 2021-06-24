from django.contrib.auth.models import User
from django.test import TestCase

class GenericViewTestCase(TestCase):
    """ generic view tests """

    @classmethod
    def setUpTestData(cls):

        # create user
        User.objects.create_user(username='testuser_generic_views', password='D9lPsoHFXeCNKEzM3IgE')

    def test_login_view(self):
        """ test generic view """

        # create url
        destination = '/login'
        # get response
        response = self.client.get('')
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=301)

# TODO: does not work so far, no template used
#    def test_login_view_template(self):
#        """ test generic view """
#
#        # login testuser
#        self.client.login(username='testuser_generic_views', password='D9lPsoHFXeCNKEzM3IgE')
#        # get response
#        response = self.client.get('')
#        # compare
#        self.assertTemplateUsed(response, 'dfirtrack_main/login.html')

# TODO: does not work so far, no context at all
#    def test_login_view_get_user_context(self):
#        """ test generic view """
#
#        # login testuser
#        self.client.login(username='testuser_generic_views', password='D9lPsoHFXeCNKEzM3IgE')
#        # get response
#        response = self.client.get('')
#        # compare
#        self.assertEqual(str(response.context['user']), 'testuser_generic_views')
