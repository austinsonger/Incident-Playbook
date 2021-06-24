from django.contrib.auth.models import User
from django.test import TestCase
from dfirtrack_main.models import Domain
import urllib.parse

class DomainAPIViewTestCase(TestCase):
    """ domain API view tests """

    @classmethod
    def setUpTestData(cls):

        # create object
        Domain.objects.create(domain_name='domain_api_1')
        # create user
        User.objects.create_user(username='testuser_domain_api', password='tvjnIPBlhP9P3ixDHVE7')

    def test_domain_list_api_unauthorized(self):
        """ unauthorized access is forbidden"""

        # get response
        response = self.client.get('/api/domain/')
        # compare
        self.assertEqual(response.status_code, 401)

    def test_domain_list_api_method_get(self):
        """ GET is allowed """

        # login testuser
        self.client.login(username='testuser_domain_api', password='tvjnIPBlhP9P3ixDHVE7')
        # get response
        response = self.client.get('/api/domain/')
        # compare
        self.assertEqual(response.status_code, 200)

    def test_domain_list_api_method_post(self):
        """ POST is allowed """

        # login testuser
        self.client.login(username='testuser_domain_api', password='tvjnIPBlhP9P3ixDHVE7')
        # create POST string
        poststring = {"domain_name": "domain_api_2"}
        # get response
        response = self.client.post('/api/domain/', data=poststring)
        # compare
        self.assertEqual(response.status_code, 201)

    def test_domain_list_api_redirect(self):
        """ test redirect with appending slash """

        # login testuser
        self.client.login(username='testuser_domain_api', password='tvjnIPBlhP9P3ixDHVE7')
        # create url
        destination = urllib.parse.quote('/api/domain/', safe='/')
        # get response
        response = self.client.get('/api/domain', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=301, target_status_code=200)

    def test_domain_detail_api_unauthorized (self):
        """ unauthorized access is forbidden"""

        # get object
        domain_api_1 = Domain.objects.get(domain_name='domain_api_1')
        # get response
        response = self.client.get('/api/domain/' + str(domain_api_1.domain_id) + '/')
        # compare
        self.assertEqual(response.status_code, 401)

    def test_domain_detail_api_method_get(self):
        """ GET is allowed """

        # get object
        domain_api_1 = Domain.objects.get(domain_name='domain_api_1')
        # login testuser
        self.client.login(username='testuser_domain_api', password='tvjnIPBlhP9P3ixDHVE7')
        # get response
        response = self.client.get('/api/domain/' + str(domain_api_1.domain_id) + '/')
        # compare
        self.assertEqual(response.status_code, 200)

    def test_domain_detail_api_method_delete(self):
        """ DELETE is forbidden """

        # get object
        domain_api_1 = Domain.objects.get(domain_name='domain_api_1')
        # login testuser
        self.client.login(username='testuser_domain_api', password='tvjnIPBlhP9P3ixDHVE7')
        # get response
        response = self.client.delete('/api/domain/' + str(domain_api_1.domain_id) + '/')
        # compare
        self.assertEqual(response.status_code, 405)

    def test_domain_detail_api_method_put(self):
        """ PUT is allowed """

        # get object
        domain_api_1 = Domain.objects.get(domain_name='domain_api_1')
        # login testuser
        self.client.login(username='testuser_domain_api', password='tvjnIPBlhP9P3ixDHVE7')
        # create url
        destination = urllib.parse.quote('/api/domain/' + str(domain_api_1.domain_id) + '/', safe='/')
        # create PUT string
        putstring = {"domain_name": "new_domain_api_1"}
        # get response
        response = self.client.put(destination, data=putstring, content_type='application/json')
        # compare
        self.assertEqual(response.status_code, 200)

    def test_domain_detail_api_redirect(self):
        """ test redirect with appending slash """

        # get object
        domain_api_1 = Domain.objects.get(domain_name='domain_api_1')
        # login testuser
        self.client.login(username='testuser_domain_api', password='tvjnIPBlhP9P3ixDHVE7')
        # create url
        destination = urllib.parse.quote('/api/domain/' + str(domain_api_1.domain_id) + '/', safe='/')
        # get response
        response = self.client.get('/api/domain/' + str(domain_api_1.domain_id), follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=301, target_status_code=200)
