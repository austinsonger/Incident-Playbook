from django.contrib.auth.models import User
from django.test import TestCase
from dfirtrack_main.models import Location
import urllib.parse

class LocationAPIViewTestCase(TestCase):
    """ location API view tests """

    @classmethod
    def setUpTestData(cls):

        # create object
        Location.objects.create(location_name='location_api_1')
        # create user
        User.objects.create_user(username='testuser_location_api', password='tvjnIPBlhP9P3ixDHVE7')

    def test_location_list_api_unauthorized(self):
        """ unauthorized access is forbidden"""

        # get response
        response = self.client.get('/api/location/')
        # compare
        self.assertEqual(response.status_code, 401)

    def test_location_list_api_method_get(self):
        """ GET is allowed """

        # login testuser
        self.client.login(username='testuser_location_api', password='tvjnIPBlhP9P3ixDHVE7')
        # get response
        response = self.client.get('/api/location/')
        # compare
        self.assertEqual(response.status_code, 200)

    def test_location_list_api_method_post(self):
        """ POST is allowed """

        # login testuser
        self.client.login(username='testuser_location_api', password='tvjnIPBlhP9P3ixDHVE7')
        # create POST string
        poststring = {"location_name": "location_api_2"}
        # get response
        response = self.client.post('/api/location/', data=poststring)
        # compare
        self.assertEqual(response.status_code, 201)

    def test_location_list_api_redirect(self):
        """ test redirect with appending slash """

        # login testuser
        self.client.login(username='testuser_location_api', password='tvjnIPBlhP9P3ixDHVE7')
        # create url
        destination = urllib.parse.quote('/api/location/', safe='/')
        # get response
        response = self.client.get('/api/location', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=301, target_status_code=200)

    def test_location_detail_api_unauthorized (self):
        """ unauthorized access is forbidden"""

        # get object
        location_api_1 = Location.objects.get(location_name='location_api_1')
        # get response
        response = self.client.get('/api/location/' + str(location_api_1.location_id) + '/')
        # compare
        self.assertEqual(response.status_code, 401)

    def test_location_detail_api_method_get(self):
        """ GET is allowed """

        # get object
        location_api_1 = Location.objects.get(location_name='location_api_1')
        # login testuser
        self.client.login(username='testuser_location_api', password='tvjnIPBlhP9P3ixDHVE7')
        # get response
        response = self.client.get('/api/location/' + str(location_api_1.location_id) + '/')
        # compare
        self.assertEqual(response.status_code, 200)

    def test_location_detail_api_method_delete(self):
        """ DELETE is forbidden """

        # get object
        location_api_1 = Location.objects.get(location_name='location_api_1')
        # login testuser
        self.client.login(username='testuser_location_api', password='tvjnIPBlhP9P3ixDHVE7')
        # get response
        response = self.client.delete('/api/location/' + str(location_api_1.location_id) + '/')
        # compare
        self.assertEqual(response.status_code, 405)

    def test_location_detail_api_method_put(self):
        """ PUT is allowed """

        # get object
        location_api_1 = Location.objects.get(location_name='location_api_1')
        # login testuser
        self.client.login(username='testuser_location_api', password='tvjnIPBlhP9P3ixDHVE7')
        # create url
        destination = urllib.parse.quote('/api/location/' + str(location_api_1.location_id) + '/', safe='/')
        # create PUT string
        putstring = {"location_name": "new_location_api_1"}
        # get response
        response = self.client.put(destination, data=putstring, content_type='application/json')
        # compare
        self.assertEqual(response.status_code, 200)

    def test_location_detail_api_redirect(self):
        """ test redirect with appending slash """

        # get object
        location_api_1 = Location.objects.get(location_name='location_api_1')
        # login testuser
        self.client.login(username='testuser_location_api', password='tvjnIPBlhP9P3ixDHVE7')
        # create url
        destination = urllib.parse.quote('/api/location/' + str(location_api_1.location_id) + '/', safe='/')
        # get response
        response = self.client.get('/api/location/' + str(location_api_1.location_id), follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=301, target_status_code=200)
