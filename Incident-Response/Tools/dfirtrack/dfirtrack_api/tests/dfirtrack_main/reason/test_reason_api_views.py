from django.contrib.auth.models import User
from django.test import TestCase
from dfirtrack_main.models import Reason
import urllib.parse

class ReasonAPIViewTestCase(TestCase):
    """ reason API view tests """

    @classmethod
    def setUpTestData(cls):

        # create object
        Reason.objects.create(reason_name='reason_api_1')
        # create user
        User.objects.create_user(username='testuser_reason_api', password='tvjnIPBlhP9P3ixDHVE7')

    def test_reason_list_api_unauthorized(self):
        """ unauthorized access is forbidden"""

        # get response
        response = self.client.get('/api/reason/')
        # compare
        self.assertEqual(response.status_code, 401)

    def test_reason_list_api_method_get(self):
        """ GET is allowed """

        # login testuser
        self.client.login(username='testuser_reason_api', password='tvjnIPBlhP9P3ixDHVE7')
        # get response
        response = self.client.get('/api/reason/')
        # compare
        self.assertEqual(response.status_code, 200)

    def test_reason_list_api_method_post(self):
        """ POST is allowed """

        # login testuser
        self.client.login(username='testuser_reason_api', password='tvjnIPBlhP9P3ixDHVE7')
        # create POST string
        poststring = {"reason_name": "reason_api_2"}
        # get response
        response = self.client.post('/api/reason/', data=poststring)
        # compare
        self.assertEqual(response.status_code, 201)

    def test_reason_list_api_redirect(self):
        """ test redirect with appending slash """

        # login testuser
        self.client.login(username='testuser_reason_api', password='tvjnIPBlhP9P3ixDHVE7')
        # create url
        destination = urllib.parse.quote('/api/reason/', safe='/')
        # get response
        response = self.client.get('/api/reason', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=301, target_status_code=200)

    def test_reason_detail_api_unauthorized (self):
        """ unauthorized access is forbidden"""

        # get object
        reason_api_1 = Reason.objects.get(reason_name='reason_api_1')
        # get response
        response = self.client.get('/api/reason/' + str(reason_api_1.reason_id) + '/')
        # compare
        self.assertEqual(response.status_code, 401)

    def test_reason_detail_api_method_get(self):
        """ GET is allowed """

        # get object
        reason_api_1 = Reason.objects.get(reason_name='reason_api_1')
        # login testuser
        self.client.login(username='testuser_reason_api', password='tvjnIPBlhP9P3ixDHVE7')
        # get response
        response = self.client.get('/api/reason/' + str(reason_api_1.reason_id) + '/')
        # compare
        self.assertEqual(response.status_code, 200)

    def test_reason_detail_api_method_delete(self):
        """ DELETE is forbidden """

        # get object
        reason_api_1 = Reason.objects.get(reason_name='reason_api_1')
        # login testuser
        self.client.login(username='testuser_reason_api', password='tvjnIPBlhP9P3ixDHVE7')
        # get response
        response = self.client.delete('/api/reason/' + str(reason_api_1.reason_id) + '/')
        # compare
        self.assertEqual(response.status_code, 405)

    def test_reason_detail_api_method_put(self):
        """ PUT is allowed """

        # get object
        reason_api_1 = Reason.objects.get(reason_name='reason_api_1')
        # login testuser
        self.client.login(username='testuser_reason_api', password='tvjnIPBlhP9P3ixDHVE7')
        # create url
        destination = urllib.parse.quote('/api/reason/' + str(reason_api_1.reason_id) + '/', safe='/')
        # create PUT string
        putstring = {"reason_name": "new_reason_api_1"}
        # get response
        response = self.client.put(destination, data=putstring, content_type='application/json')
        # compare
        self.assertEqual(response.status_code, 200)

    def test_reason_detail_api_redirect(self):
        """ test redirect with appending slash """

        # get object
        reason_api_1 = Reason.objects.get(reason_name='reason_api_1')
        # login testuser
        self.client.login(username='testuser_reason_api', password='tvjnIPBlhP9P3ixDHVE7')
        # create url
        destination = urllib.parse.quote('/api/reason/' + str(reason_api_1.reason_id) + '/', safe='/')
        # get response
        response = self.client.get('/api/reason/' + str(reason_api_1.reason_id), follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=301, target_status_code=200)
