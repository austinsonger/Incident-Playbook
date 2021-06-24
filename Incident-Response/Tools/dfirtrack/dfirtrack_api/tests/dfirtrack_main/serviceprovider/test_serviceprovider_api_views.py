from django.contrib.auth.models import User
from django.test import TestCase
from dfirtrack_main.models import Serviceprovider
import urllib.parse

class ServiceproviderAPIViewTestCase(TestCase):
    """ serviceprovider API view tests """

    @classmethod
    def setUpTestData(cls):

        # create object
        Serviceprovider.objects.create(serviceprovider_name='serviceprovider_api_1')
        # create user
        User.objects.create_user(username='testuser_serviceprovider_api', password='ILKjadN2mA971kHquiuI')

    def test_serviceprovider_list_api_unauthorized(self):
        """ unauthorized access is forbidden"""

        # get response
        response = self.client.get('/api/serviceprovider/')
        # compare
        self.assertEqual(response.status_code, 401)

    def test_serviceprovider_list_api_method_get(self):
        """ GET is allowed """

        # login testuser
        self.client.login(username='testuser_serviceprovider_api', password='ILKjadN2mA971kHquiuI')
        # get response
        response = self.client.get('/api/serviceprovider/')
        # compare
        self.assertEqual(response.status_code, 200)

    def test_serviceprovider_list_api_method_post(self):
        """ POST is allowed """

        # login testuser
        self.client.login(username='testuser_serviceprovider_api', password='ILKjadN2mA971kHquiuI')
        # create POST string
        poststring = {"serviceprovider_name": "serviceprovider_api_2"}
        # get response
        response = self.client.post('/api/serviceprovider/', data=poststring)
        # compare
        self.assertEqual(response.status_code, 201)

    def test_serviceprovider_list_api_redirect(self):
        """ test redirect with appending slash """

        # login testuser
        self.client.login(username='testuser_serviceprovider_api', password='ILKjadN2mA971kHquiuI')
        # create url
        destination = urllib.parse.quote('/api/serviceprovider/', safe='/')
        # get response
        response = self.client.get('/api/serviceprovider', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=301, target_status_code=200)

    def test_serviceprovider_detail_api_unauthorized (self):
        """ unauthorized access is forbidden"""

        # get object
        serviceprovider_api_1 = Serviceprovider.objects.get(serviceprovider_name='serviceprovider_api_1')
        # get response
        response = self.client.get('/api/serviceprovider/' + str(serviceprovider_api_1.serviceprovider_id) + '/')
        # compare
        self.assertEqual(response.status_code, 401)

    def test_serviceprovider_detail_api_method_get(self):
        """ GET is allowed """

        # get object
        serviceprovider_api_1 = Serviceprovider.objects.get(serviceprovider_name='serviceprovider_api_1')
        # login testuser
        self.client.login(username='testuser_serviceprovider_api', password='ILKjadN2mA971kHquiuI')
        # get response
        response = self.client.get('/api/serviceprovider/' + str(serviceprovider_api_1.serviceprovider_id) + '/')
        # compare
        self.assertEqual(response.status_code, 200)

    def test_serviceprovider_detail_api_method_delete(self):
        """ DELETE is forbidden """

        # get object
        serviceprovider_api_1 = Serviceprovider.objects.get(serviceprovider_name='serviceprovider_api_1')
        # login testuser
        self.client.login(username='testuser_serviceprovider_api', password='ILKjadN2mA971kHquiuI')
        # get response
        response = self.client.delete('/api/serviceprovider/' + str(serviceprovider_api_1.serviceprovider_id) + '/')
        # compare
        self.assertEqual(response.status_code, 405)

    def test_serviceprovider_detail_api_method_put(self):
        """ PUT is allowed """

        # get object
        serviceprovider_api_1 = Serviceprovider.objects.get(serviceprovider_name='serviceprovider_api_1')
        # login testuser
        self.client.login(username='testuser_serviceprovider_api', password='ILKjadN2mA971kHquiuI')
        # create url
        destination = urllib.parse.quote('/api/serviceprovider/' + str(serviceprovider_api_1.serviceprovider_id) + '/', safe='/')
        # create PUT string
        putstring = {"serviceprovider_name": "new_serviceprovider_api_1"}
        # get response
        response = self.client.put(destination, data=putstring, content_type='application/json')
        # compare
        self.assertEqual(response.status_code, 200)

    def test_serviceprovider_detail_api_redirect(self):
        """ test redirect with appending slash """

        # get object
        serviceprovider_api_1 = Serviceprovider.objects.get(serviceprovider_name='serviceprovider_api_1')
        # login testuser
        self.client.login(username='testuser_serviceprovider_api', password='ILKjadN2mA971kHquiuI')
        # create url
        destination = urllib.parse.quote('/api/serviceprovider/' + str(serviceprovider_api_1.serviceprovider_id) + '/', safe='/')
        # get response
        response = self.client.get('/api/serviceprovider/' + str(serviceprovider_api_1.serviceprovider_id), follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=301, target_status_code=200)
