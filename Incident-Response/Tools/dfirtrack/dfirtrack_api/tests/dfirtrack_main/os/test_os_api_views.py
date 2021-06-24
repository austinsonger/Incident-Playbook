from django.contrib.auth.models import User
from django.test import TestCase
from dfirtrack_main.models import Os
import urllib.parse

class IpAPIViewTestCase(TestCase):
    """ os API view tests """

    @classmethod
    def setUpTestData(cls):

        # create object
        Os.objects.create(os_name='os_api_1')
        # create user
        User.objects.create_user(username='testuser_os_api', password='Ty8sCsWifIJmxx4KaJd6')

    def test_os_list_api_unauthorized(self):
        """ unauthorized access is forbidden"""

        # get response
        response = self.client.get('/api/os/')
        # compare
        self.assertEqual(response.status_code, 401)

    def test_os_list_api_method_get(self):
        """ GET is allowed """

        # login testuser
        self.client.login(username='testuser_os_api', password='Ty8sCsWifIJmxx4KaJd6')
        # get response
        response = self.client.get('/api/os/')
        # compare
        self.assertEqual(response.status_code, 200)

    def test_os_list_api_method_post(self):
        """ POST is allowed """

        # login testuser
        self.client.login(username='testuser_os_api', password='Ty8sCsWifIJmxx4KaJd6')
        # create POST string
        poststring = {"os_name": "os_api_2"}
        # get response
        response = self.client.post('/api/os/', data=poststring)
        # compare
        self.assertEqual(response.status_code, 201)

    def test_os_list_api_redirect(self):
        """ test redirect with appending slash """

        # login testuser
        self.client.login(username='testuser_os_api', password='Ty8sCsWifIJmxx4KaJd6')
        # create url
        destination = urllib.parse.quote('/api/os/', safe='/')
        # get response
        response = self.client.get('/api/os', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=301, target_status_code=200)

    def test_os_detail_api_unauthorized (self):
        """ unauthorized access is forbidden"""

        # get object
        os_api_1 = Os.objects.get(os_name='os_api_1')
        # get response
        response = self.client.get('/api/os/' + str(os_api_1.os_id) + '/')
        # compare
        self.assertEqual(response.status_code, 401)

    def test_os_detail_api_method_get(self):
        """ GET is allowed """

        # get object
        os_api_1 = Os.objects.get(os_name='os_api_1')
        # login testuser
        self.client.login(username='testuser_os_api', password='Ty8sCsWifIJmxx4KaJd6')
        # get response
        response = self.client.get('/api/os/' + str(os_api_1.os_id) + '/')
        # compare
        self.assertEqual(response.status_code, 200)

    def test_os_detail_api_method_delete(self):
        """ DELETE is forbidden """

        # get object
        os_api_1 = Os.objects.get(os_name='os_api_1')
        # login testuser
        self.client.login(username='testuser_os_api', password='Ty8sCsWifIJmxx4KaJd6')
        # get response
        response = self.client.delete('/api/os/' + str(os_api_1.os_id) + '/')
        # compare
        self.assertEqual(response.status_code, 405)

    def test_os_detail_api_method_put(self):
        """ PUT is allowed """

        # get object
        os_api_1 = Os.objects.get(os_name='os_api_1')
        # login testuser
        self.client.login(username='testuser_os_api', password='Ty8sCsWifIJmxx4KaJd6')
        # create url
        destination = urllib.parse.quote('/api/os/' + str(os_api_1.os_id) + '/', safe='/')
        # create PUT string
        putstring = {"os_name": "new_os_api_1"}
        # get response
        response = self.client.put(destination, data=putstring, content_type='application/json')
        # compare
        self.assertEqual(response.status_code, 200)

    def test_os_detail_api_redirect(self):
        """ test redirect with appending slash """

        # get object
        os_api_1 = Os.objects.get(os_name='os_api_1')
        # login testuser
        self.client.login(username='testuser_os_api', password='Ty8sCsWifIJmxx4KaJd6')
        # create url
        destination = urllib.parse.quote('/api/os/' + str(os_api_1.os_id) + '/', safe='/')
        # get response
        response = self.client.get('/api/os/' + str(os_api_1.os_id), follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=301, target_status_code=200)
