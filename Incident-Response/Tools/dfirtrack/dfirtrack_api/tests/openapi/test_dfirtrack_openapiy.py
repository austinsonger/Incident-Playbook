from django.contrib.auth.models import User
from django.test import TestCase
import urllib.parse


class DFIRTrackOpenAPIViewTestCase(TestCase):
    """ DFIRTrack OpenAPI 3 view tests """

    @classmethod
    def setUpTestData(cls):

        # create user
        User.objects.create_user(username='testuser_openapi_api_1', password='ZxMzUqYU6mrDzO9q')

    def test_openapi_api_view_unuathorized(self):
        """ unauthorized access is forbidden """

        # get response
        response = self.client.get('/api/openapi/')
        # compare
        self.assertEqual(response.status_code, 401)

    def test_openapi_api_view_authorized_method_get(self):
        """ GET is allowed """

        # login test user
        response = self.client.login(username='testuser_openapi_api_1', password='ZxMzUqYU6mrDzO9q')
        # get response
        response = self.client.get('/api/openapi/')
        # compare
        self.assertEqual(response.status_code, 200)

    def test_openapi_api_view_authorized_method_post(self):
        """ POST is forbidden """

        # login testuser
        self.client.login(username='testuser_openapi_api_1', password='ZxMzUqYU6mrDzO9q')
        # create POST string
        poststring = {"openapi_var": "openapi_value"}
        # get response
        response = self.client.post('/api/openapi/', data=poststring)
        # compare
        self.assertEqual(response.status_code, 405)

    def test_openapi_api_view_authorized_redirect(self):
        """ test redirect with appending slash """

        # login testuser
        self.client.login(username='testuser_openapi_api_1', password='ZxMzUqYU6mrDzO9q')
        # create url
        destination = urllib.parse.quote('/api/openapi/', safe='/')
        # get response
        response = self.client.get('/api/openapi', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=301, target_status_code=200)
