from django.contrib.auth.models import User
from django.test import TestCase
from dfirtrack_main.models import Domain, Dnsname
import urllib.parse

class DnsnameAPIViewTestCase(TestCase):
    """ dnsname API view tests """

    @classmethod
    def setUpTestData(cls):

        # create object
        Domain.objects.create(domain_name='domain_api_1')
        # create object
        Domain.objects.create(domain_name='domain_api_2')
        # create object
        Dnsname.objects.create(dnsname_name='dnsname_api_1')
        # create user
        User.objects.create_user(username='testuser_dnsname_api', password='tvjnIPBlhP9P3ixDHVE7')

    def test_dnsname_list_api_unauthorized(self):
        """ unauthorized access is forbidden"""

        # get response
        response = self.client.get('/api/dnsname/')
        # compare
        self.assertEqual(response.status_code, 401)

    def test_dnsname_list_api_method_get(self):
        """ GET is allowed """

        # login testuser
        self.client.login(username='testuser_dnsname_api', password='tvjnIPBlhP9P3ixDHVE7')
        # get response
        response = self.client.get('/api/dnsname/')
        # compare
        self.assertEqual(response.status_code, 200)

    def test_dnsname_list_api_method_post(self):
        """ POST is allowed """

        # get object
        domain_id = str(Domain.objects.get(domain_name='domain_api_2').domain_id)
        # login testuser
        self.client.login(username='testuser_dnsname_api', password='tvjnIPBlhP9P3ixDHVE7')
        # create POST string
        poststring = {
            "dnsname_name": "dnsname_api_2",
            "domain": domain_id,
        }
        # get response
        response = self.client.post('/api/dnsname/', data=poststring)
        # compare
        self.assertEqual(response.status_code, 201)

    def test_dnsname_list_api_redirect(self):
        """ test redirect with appending slash """

        # login testuser
        self.client.login(username='testuser_dnsname_api', password='tvjnIPBlhP9P3ixDHVE7')
        # create url
        destination = urllib.parse.quote('/api/dnsname/', safe='/')
        # get response
        response = self.client.get('/api/dnsname', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=301, target_status_code=200)

    def test_dnsname_detail_api_unauthorized (self):
        """ unauthorized access is forbidden"""

        # get object
        dnsname_api_1 = Dnsname.objects.get(dnsname_name='dnsname_api_1')
        # get response
        response = self.client.get('/api/dnsname/' + str(dnsname_api_1.dnsname_id) + '/')
        # compare
        self.assertEqual(response.status_code, 401)

    def test_dnsname_detail_api_method_get(self):
        """ GET is allowed """

        # get object
        dnsname_api_1 = Dnsname.objects.get(dnsname_name='dnsname_api_1')
        # login testuser
        self.client.login(username='testuser_dnsname_api', password='tvjnIPBlhP9P3ixDHVE7')
        # get response
        response = self.client.get('/api/dnsname/' + str(dnsname_api_1.dnsname_id) + '/')
        # compare
        self.assertEqual(response.status_code, 200)

    def test_dnsname_detail_api_method_delete(self):
        """ DELETE is forbidden """

        # get object
        dnsname_api_1 = Dnsname.objects.get(dnsname_name='dnsname_api_1')
        # login testuser
        self.client.login(username='testuser_dnsname_api', password='tvjnIPBlhP9P3ixDHVE7')
        # get response
        response = self.client.delete('/api/dnsname/' + str(dnsname_api_1.dnsname_id) + '/')
        # compare
        self.assertEqual(response.status_code, 405)

    def test_dnsname_detail_api_method_put(self):
        """ PUT is allowed """

        # get object
        domain_id = str(Domain.objects.get(domain_name='domain_api_1').domain_id)
        # get object
        dnsname_api_1 = Dnsname.objects.get(dnsname_name='dnsname_api_1')
        # login testuser
        self.client.login(username='testuser_dnsname_api', password='tvjnIPBlhP9P3ixDHVE7')
        # create url
        destination = urllib.parse.quote('/api/dnsname/' + str(dnsname_api_1.dnsname_id) + '/', safe='/')
        # create PUT string
        putstring = {
            "dnsname_name": "new_dnsname_api_1",
            "domain": domain_id,
        }
        # get response
        response = self.client.put(destination, data=putstring, content_type='application/json')
        # compare
        self.assertEqual(response.status_code, 200)

    def test_dnsname_detail_api_redirect(self):
        """ test redirect with appending slash """

        # get object
        dnsname_api_1 = Dnsname.objects.get(dnsname_name='dnsname_api_1')
        # login testuser
        self.client.login(username='testuser_dnsname_api', password='tvjnIPBlhP9P3ixDHVE7')
        # create url
        destination = urllib.parse.quote('/api/dnsname/' + str(dnsname_api_1.dnsname_id) + '/', safe='/')
        # get response
        response = self.client.get('/api/dnsname/' + str(dnsname_api_1.dnsname_id), follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=301, target_status_code=200)
