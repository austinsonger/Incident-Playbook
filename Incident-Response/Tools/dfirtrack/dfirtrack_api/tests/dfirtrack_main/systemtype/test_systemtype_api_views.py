from django.contrib.auth.models import User
from django.test import TestCase
from dfirtrack_main.models import Systemtype
import urllib.parse

class SystemtypeAPIViewTestCase(TestCase):
    """ systemtype API view tests """

    @classmethod
    def setUpTestData(cls):

        # create object
        Systemtype.objects.create(systemtype_name='systemtype_api_1')
        # create user
        User.objects.create_user(username='testuser_systemtype_api', password='ma1QFeT2G9ifUeETRwvK')

    def test_systemtype_list_api_unauthorized(self):
        """ unauthorized access is forbidden"""

        # get response
        response = self.client.get('/api/systemtype/')
        # compare
        self.assertEqual(response.status_code, 401)

    def test_systemtype_list_api_method_get(self):
        """ GET is allowed """

        # login testuser
        self.client.login(username='testuser_systemtype_api', password='ma1QFeT2G9ifUeETRwvK')
        # get response
        response = self.client.get('/api/systemtype/')
        # compare
        self.assertEqual(response.status_code, 200)

    def test_systemtype_list_api_method_post(self):
        """ POST is allowed """

        # login testuser
        self.client.login(username='testuser_systemtype_api', password='ma1QFeT2G9ifUeETRwvK')
        # create POST string
        poststring = {"systemtype_name": "systemtype_api_2"}
        # get response
        response = self.client.post('/api/systemtype/', data=poststring)
        # compare
        self.assertEqual(response.status_code, 201)

    def test_systemtype_list_api_redirect(self):
        """ test redirect with appending slash """

        # login testuser
        self.client.login(username='testuser_systemtype_api', password='ma1QFeT2G9ifUeETRwvK')
        # create url
        destination = urllib.parse.quote('/api/systemtype/', safe='/')
        # get response
        response = self.client.get('/api/systemtype', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=301, target_status_code=200)

    def test_systemtype_detail_api_unauthorized (self):
        """ unauthorized access is forbidden"""

        # get object
        systemtype_api_1 = Systemtype.objects.get(systemtype_name='systemtype_api_1')
        # get response
        response = self.client.get('/api/systemtype/' + str(systemtype_api_1.systemtype_id) + '/')
        # compare
        self.assertEqual(response.status_code, 401)

    def test_systemtype_detail_api_method_get(self):
        """ GET is allowed """

        # get object
        systemtype_api_1 = Systemtype.objects.get(systemtype_name='systemtype_api_1')
        # login testuser
        self.client.login(username='testuser_systemtype_api', password='ma1QFeT2G9ifUeETRwvK')
        # get response
        response = self.client.get('/api/systemtype/' + str(systemtype_api_1.systemtype_id) + '/')
        # compare
        self.assertEqual(response.status_code, 200)

    def test_systemtype_detail_api_method_delete(self):
        """ DELETE is forbidden """

        # get object
        systemtype_api_1 = Systemtype.objects.get(systemtype_name='systemtype_api_1')
        # login testuser
        self.client.login(username='testuser_systemtype_api', password='ma1QFeT2G9ifUeETRwvK')
        # get response
        response = self.client.delete('/api/systemtype/' + str(systemtype_api_1.systemtype_id) + '/')
        # compare
        self.assertEqual(response.status_code, 405)

    def test_systemtype_detail_api_method_put(self):
        """ PUT is allowed """

        # get object
        systemtype_api_1 = Systemtype.objects.get(systemtype_name='systemtype_api_1')
        # login testuser
        self.client.login(username='testuser_systemtype_api', password='ma1QFeT2G9ifUeETRwvK')
        # create url
        destination = urllib.parse.quote('/api/systemtype/' + str(systemtype_api_1.systemtype_id) + '/', safe='/')
        # create PUT string
        putstring = {"systemtype_name": "new_systemtype_api_1"}
        # get response
        response = self.client.put(destination, data=putstring, content_type='application/json')
        # compare
        self.assertEqual(response.status_code, 200)

    def test_systemtype_detail_api_redirect(self):
        """ test redirect with appending slash """

        # get object
        systemtype_api_1 = Systemtype.objects.get(systemtype_name='systemtype_api_1')
        # login testuser
        self.client.login(username='testuser_systemtype_api', password='ma1QFeT2G9ifUeETRwvK')
        # create url
        destination = urllib.parse.quote('/api/systemtype/' + str(systemtype_api_1.systemtype_id) + '/', safe='/')
        # get response
        response = self.client.get('/api/systemtype/' + str(systemtype_api_1.systemtype_id), follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=301, target_status_code=200)
