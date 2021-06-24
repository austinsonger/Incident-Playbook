from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone
from dfirtrack_main.models import System, Systemstatus, Systemuser
import urllib.parse

class SystemuserAPIViewTestCase(TestCase):
    """ systemuser API view tests """

    @classmethod
    def setUpTestData(cls):

        # create user
        test_user = User.objects.create_user(username='testuser_systemuser_api', password='Yij2up4yTV2BU6x9xKZV')

        # create object
        systemstatus_1 = Systemstatus.objects.create(systemstatus_name='systemstatus_1')

        # create object
        system_1 = System.objects.create(
            system_name = 'system_1',
            systemstatus = systemstatus_1,
            system_modify_time = timezone.now(),
            system_created_by_user_id = test_user,
            system_modified_by_user_id = test_user,
        )

        # create object
        Systemuser.objects.create(
            systemuser_name='systemuser_api_1',
            systemuser_is_systemadmin = True,
            system = system_1,
            systemuser_lastlogon_time = timezone.now(),
        )

    def test_systemuser_list_api_unauthorized(self):
        """ unauthorized access is forbidden"""

        # get response
        response = self.client.get('/api/systemuser/')
        # compare
        self.assertEqual(response.status_code, 401)

    def test_systemuser_list_api_method_get(self):
        """ GET is allowed """

        # login testuser
        self.client.login(username='testuser_systemuser_api', password='Yij2up4yTV2BU6x9xKZV')
        # get response
        response = self.client.get('/api/systemuser/')
        # compare
        self.assertEqual(response.status_code, 200)

    def test_systemuser_list_api_method_post(self):
        """ POST is allowed """

        # login testuser
        self.client.login(username='testuser_systemuser_api', password='Yij2up4yTV2BU6x9xKZV')
        # get object
        system_id = str(System.objects.get(system_name='system_1').system_id)
        # create POST string
        poststring = {
            "systemuser_name": "systemuser_api_2",
            "systemuser_is_systemadmin": False,
            "system": system_id,
        }
        # get response
        response = self.client.post('/api/systemuser/', data=poststring)
        # compare
        self.assertEqual(response.status_code, 201)

    def test_systemuser_list_api_redirect(self):
        """ test redirect with appending slash """

        # login testuser
        self.client.login(username='testuser_systemuser_api', password='Yij2up4yTV2BU6x9xKZV')
        # create url
        destination = urllib.parse.quote('/api/systemuser/', safe='/')
        # get response
        response = self.client.get('/api/systemuser', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=301, target_status_code=200)

    def test_systemuser_detail_api_unauthorized (self):
        """ unauthorized access is forbidden"""

        # get object
        systemuser_api_1 = Systemuser.objects.get(systemuser_name='systemuser_api_1')
        # get response
        response = self.client.get('/api/systemuser/' + str(systemuser_api_1.systemuser_id) + '/')
        # compare
        self.assertEqual(response.status_code, 401)

    def test_systemuser_detail_api_method_get(self):
        """ GET is allowed """

        # get object
        systemuser_api_1 = Systemuser.objects.get(systemuser_name='systemuser_api_1')
        # login testuser
        self.client.login(username='testuser_systemuser_api', password='Yij2up4yTV2BU6x9xKZV')
        # get response
        response = self.client.get('/api/systemuser/' + str(systemuser_api_1.systemuser_id) + '/')
        # compare
        self.assertEqual(response.status_code, 200)

    def test_systemuser_detail_api_method_delete(self):
        """ DELETE is forbidden """

        # get object
        systemuser_api_1 = Systemuser.objects.get(systemuser_name='systemuser_api_1')
        # login testuser
        self.client.login(username='testuser_systemuser_api', password='Yij2up4yTV2BU6x9xKZV')
        # get response
        response = self.client.delete('/api/systemuser/' + str(systemuser_api_1.systemuser_id) + '/')
        # compare
        self.assertEqual(response.status_code, 405)

    def test_systemuser_detail_api_method_put(self):
        """ PUT is allowed """

        # get object
        system_id = str(System.objects.get(system_name='system_1').system_id)
        # get object
        systemuser_api_1 = Systemuser.objects.get(systemuser_name='systemuser_api_1')
        # login testuser
        self.client.login(username='testuser_systemuser_api', password='Yij2up4yTV2BU6x9xKZV')
        # create url
        destination = urllib.parse.quote('/api/systemuser/' + str(systemuser_api_1.systemuser_id) + '/', safe='/')
        # create PUT string
        putstring = {
            "systemuser_name": "systemuser_api_3",
            "systemuser_is_systemadmin": False,
            "system": system_id,
        }
        # get response
        response = self.client.put(destination, data=putstring, content_type='application/json')
        # compare
        self.assertEqual(response.status_code, 200)

    def test_systemuser_detail_api_redirect(self):
        """ test redirect with appending slash """

        # get object
        systemuser_api_1 = Systemuser.objects.get(systemuser_name='systemuser_api_1')
        # login testuser
        self.client.login(username='testuser_systemuser_api', password='Yij2up4yTV2BU6x9xKZV')
        # create url
        destination = urllib.parse.quote('/api/systemuser/' + str(systemuser_api_1.systemuser_id) + '/', safe='/')
        # get response
        response = self.client.get('/api/systemuser/' + str(systemuser_api_1.systemuser_id), follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=301, target_status_code=200)
