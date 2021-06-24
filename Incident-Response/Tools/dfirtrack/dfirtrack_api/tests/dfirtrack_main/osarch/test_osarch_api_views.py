from django.contrib.auth.models import User
from django.test import TestCase
from dfirtrack_main.models import Osarch
import urllib.parse

class OsarchAPIViewTestCase(TestCase):
    """ osarch API view tests """

    @classmethod
    def setUpTestData(cls):

        # create object
        Osarch.objects.create(osarch_name='osarch_1')
        # create user
        User.objects.create_user(username='testuser_osarch_api', password='baxmijIgjTfCzy9w8lrF')

    def test_osarch_list_api_unauthorized(self):
        """ unauthorized access is forbidden"""

        # get response
        response = self.client.get('/api/osarch/')
        # compare
        self.assertEqual(response.status_code, 401)

    def test_osarch_list_api_method_get(self):
        """ GET is allowed """

        # login testuser
        self.client.login(username='testuser_osarch_api', password='baxmijIgjTfCzy9w8lrF')
        # get response
        response = self.client.get('/api/osarch/')
        # compare
        self.assertEqual(response.status_code, 200)

    def test_osarch_list_api_method_post(self):
        """ POST is allowed """

        # login testuser
        self.client.login(username='testuser_osarch_api', password='baxmijIgjTfCzy9w8lrF')
        # create POST string
        poststring = {"osarch_name": "osarch_2"}
        # get response
        response = self.client.post('/api/osarch/', data=poststring)
        # compare
        self.assertEqual(response.status_code, 201)

    def test_osarch_list_api_redirect(self):
        """ test redirect with appending slash """

        # login testuser
        self.client.login(username='testuser_osarch_api', password='baxmijIgjTfCzy9w8lrF')
        # create url
        destination = urllib.parse.quote('/api/osarch/', safe='/')
        # get response
        response = self.client.get('/api/osarch', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=301, target_status_code=200)

    def test_osarch_detail_api_unauthorized (self):
        """ unauthorized access is forbidden"""

        # get object
        osarch_api_1 = Osarch.objects.get(osarch_name='osarch_1')
        # get response
        response = self.client.get('/api/osarch/' + str(osarch_api_1.osarch_id) + '/')
        # compare
        self.assertEqual(response.status_code, 401)

    def test_osarch_detail_api_method_get(self):
        """ GET is allowed """

        # get object
        osarch_api_1 = Osarch.objects.get(osarch_name='osarch_1')
        # login testuser
        self.client.login(username='testuser_osarch_api', password='baxmijIgjTfCzy9w8lrF')
        # get response
        response = self.client.get('/api/osarch/' + str(osarch_api_1.osarch_id) + '/')
        # compare
        self.assertEqual(response.status_code, 200)

    def test_osarch_detail_api_method_delete(self):
        """ DELETE is forbidden """

        # get object
        osarch_api_1 = Osarch.objects.get(osarch_name='osarch_1')
        # login testuser
        self.client.login(username='testuser_osarch_api', password='baxmijIgjTfCzy9w8lrF')
        # get response
        response = self.client.delete('/api/osarch/' + str(osarch_api_1.osarch_id) + '/')
        # compare
        self.assertEqual(response.status_code, 405)

    def test_osarch_detail_api_method_put(self):
        """ PUT is allowed """

        # get object
        osarch_api_1 = Osarch.objects.get(osarch_name='osarch_1')
        # login testuser
        self.client.login(username='testuser_osarch_api', password='baxmijIgjTfCzy9w8lrF')
        # create url
        destination = urllib.parse.quote('/api/osarch/' + str(osarch_api_1.osarch_id) + '/', safe='/')
        # create PUT string
        putstring = {"osarch_name": "osarch_3"}
        # get response
        response = self.client.put(destination, data=putstring, content_type='application/json')
        # compare
        self.assertEqual(response.status_code, 200)

    def test_osarch_detail_api_redirect(self):
        """ test redirect with appending slash """

        # get object
        osarch_api_1 = Osarch.objects.get(osarch_name='osarch_1')
        # login testuser
        self.client.login(username='testuser_osarch_api', password='baxmijIgjTfCzy9w8lrF')
        # create url
        destination = urllib.parse.quote('/api/osarch/' + str(osarch_api_1.osarch_id) + '/', safe='/')
        # get response
        response = self.client.get('/api/osarch/' + str(osarch_api_1.osarch_id), follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=301, target_status_code=200)
