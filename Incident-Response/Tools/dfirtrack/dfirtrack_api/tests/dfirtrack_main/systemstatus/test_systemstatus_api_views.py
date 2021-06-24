from django.contrib.auth.models import User
from django.test import TestCase
from dfirtrack_main.models import Systemstatus
import urllib.parse

class SystemstatusAPIViewTestCase(TestCase):
    """ systemstatus API view tests """

    @classmethod
    def setUpTestData(cls):

        # create object
        Systemstatus.objects.create(systemstatus_name='systemstatus_api_1')
        # create user
        User.objects.create_user(username='testuser_systemstatus_api', password='aCTVRIdJ4cyVSkYiJKrM')

    def test_systemstatus_list_api_unauthorized(self):
        """ unauthorized access is forbidden"""

        # get response
        response = self.client.get('/api/systemstatus/')
        # compare
        self.assertEqual(response.status_code, 401)

    def test_systemstatus_list_api_method_get(self):
        """ GET is allowed """

        # login testuser
        self.client.login(username='testuser_systemstatus_api', password='aCTVRIdJ4cyVSkYiJKrM')
        # get response
        response = self.client.get('/api/systemstatus/')
        # compare
        self.assertEqual(response.status_code, 200)

    def test_systemstatus_list_api_method_post(self):
        """ POST is forbidden """

        # login testuser
        self.client.login(username='testuser_systemstatus_api', password='aCTVRIdJ4cyVSkYiJKrM')
        # create POST string
        poststring = {"systemstatus_name": "systemstatus_api_2"}
        # get response
        response = self.client.post('/api/systemstatus/', data=poststring)
        # compare
        self.assertEqual(response.status_code, 405)

    def test_systemstatus_list_api_redirect(self):
        """ test redirect with appending slash """

        # login testuser
        self.client.login(username='testuser_systemstatus_api', password='aCTVRIdJ4cyVSkYiJKrM')
        # create url
        destination = urllib.parse.quote('/api/systemstatus/', safe='/')
        # get response
        response = self.client.get('/api/systemstatus', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=301, target_status_code=200)

    def test_systemstatus_detail_api_unauthorized (self):
        """ unauthorized access is forbidden"""

        # get object
        systemstatus_api_1 = Systemstatus.objects.get(systemstatus_name='systemstatus_api_1')
        # get response
        response = self.client.get('/api/systemstatus/' + str(systemstatus_api_1.systemstatus_id) + '/')
        # compare
        self.assertEqual(response.status_code, 401)

    def test_systemstatus_detail_api_method_get(self):
        """ GET is allowed """

        # get object
        systemstatus_api_1 = Systemstatus.objects.get(systemstatus_name='systemstatus_api_1')
        # login testuser
        self.client.login(username='testuser_systemstatus_api', password='aCTVRIdJ4cyVSkYiJKrM')
        # get response
        response = self.client.get('/api/systemstatus/' + str(systemstatus_api_1.systemstatus_id) + '/')
        # compare
        self.assertEqual(response.status_code, 200)

    def test_systemstatus_detail_api_method_delete(self):
        """ DELETE is forbidden """

        # get object
        systemstatus_api_1 = Systemstatus.objects.get(systemstatus_name='systemstatus_api_1')
        # login testuser
        self.client.login(username='testuser_systemstatus_api', password='aCTVRIdJ4cyVSkYiJKrM')
        # get response
        response = self.client.delete('/api/systemstatus/' + str(systemstatus_api_1.systemstatus_id) + '/')
        # compare
        self.assertEqual(response.status_code, 405)

    def test_systemstatus_detail_api_method_put(self):
        """ PUT is forbidden """

        # get object
        systemstatus_api_1 = Systemstatus.objects.get(systemstatus_name='systemstatus_api_1')
        # login testuser
        self.client.login(username='testuser_systemstatus_api', password='aCTVRIdJ4cyVSkYiJKrM')
        # create url
        destination = urllib.parse.quote('/api/systemstatus/' + str(systemstatus_api_1.systemstatus_id) + '/', safe='/')
        # create PUT string
        putstring = {"systemstatus_name": "new_systemstatus_api_1"}
        # get response
        response = self.client.put(destination, data=putstring, content_type='application/json')
        # compare
        self.assertEqual(response.status_code, 405)

    def test_systemstatus_detail_api_redirect(self):
        """ test redirect with appending slash """

        # get object
        systemstatus_api_1 = Systemstatus.objects.get(systemstatus_name='systemstatus_api_1')
        # login testuser
        self.client.login(username='testuser_systemstatus_api', password='aCTVRIdJ4cyVSkYiJKrM')
        # create url
        destination = urllib.parse.quote('/api/systemstatus/' + str(systemstatus_api_1.systemstatus_id) + '/', safe='/')
        # get response
        response = self.client.get('/api/systemstatus/' + str(systemstatus_api_1.systemstatus_id), follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=301, target_status_code=200)
