from django.contrib.auth.models import User
from django.test import TestCase
from dfirtrack_main.models import Company, Division
import urllib.parse

class CompanyAPIViewTestCase(TestCase):
    """ company API view tests """

    @classmethod
    def setUpTestData(cls):

        # create object
        Division.objects.create(division_name='division_api_1')
        # create object
        Division.objects.create(division_name='division_api_2')
        # create object
        Company.objects.create(
            company_name='company_api_1'
        )
        # create user
        User.objects.create_user(username='testuser_company_api', password='tvjnIPBlhP9P3ixDHVE7')

    def test_company_list_api_unauthorized(self):
        """ unauthorized access is forbidden"""

        # get response
        response = self.client.get('/api/company/')
        # compare
        self.assertEqual(response.status_code, 401)

    def test_company_list_api_method_get(self):
        """ GET is allowed """

        # login testuser
        self.client.login(username='testuser_company_api', password='tvjnIPBlhP9P3ixDHVE7')
        # get response
        response = self.client.get('/api/company/')
        # compare
        self.assertEqual(response.status_code, 200)

    def test_company_list_api_method_post(self):
        """ POST is allowed """

        # get object
        division_id = str(Division.objects.get(division_name='division_api_2').division_id)
        # login testuser
        self.client.login(username='testuser_company_api', password='tvjnIPBlhP9P3ixDHVE7')
        # create POST string
        poststring = {
            "company_name": "company_api_2",
            "division": division_id,
        }
        # get response
        response = self.client.post('/api/company/', data=poststring)
        # compare
        self.assertEqual(response.status_code, 201)

    def test_company_list_api_redirect(self):
        """ test redirect with appending slash """

        # login testuser
        self.client.login(username='testuser_company_api', password='tvjnIPBlhP9P3ixDHVE7')
        # create url
        destination = urllib.parse.quote('/api/company/', safe='/')
        # get response
        response = self.client.get('/api/company', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=301, target_status_code=200)

    def test_company_detail_api_unauthorized (self):
        """ unauthorized access is forbidden"""

        # get object
        company_api_1 = Company.objects.get(company_name='company_api_1')
        # get response
        response = self.client.get('/api/company/' + str(company_api_1.company_id) + '/')
        # compare
        self.assertEqual(response.status_code, 401)

    def test_company_detail_api_method_get(self):
        """ GET is allowed """

        # get object
        company_api_1 = Company.objects.get(company_name='company_api_1')
        # login testuser
        self.client.login(username='testuser_company_api', password='tvjnIPBlhP9P3ixDHVE7')
        # get response
        response = self.client.get('/api/company/' + str(company_api_1.company_id) + '/')
        # compare
        self.assertEqual(response.status_code, 200)

    def test_company_detail_api_method_delete(self):
        """ DELETE is forbidden """

        # get object
        company_api_1 = Company.objects.get(company_name='company_api_1')
        # login testuser
        self.client.login(username='testuser_company_api', password='tvjnIPBlhP9P3ixDHVE7')
        # get response
        response = self.client.delete('/api/company/' + str(company_api_1.company_id) + '/')
        # compare
        self.assertEqual(response.status_code, 405)

    def test_company_detail_api_method_put(self):
        """ PUT is allowed """

        # get object
        division_id = str(Division.objects.get(division_name='division_api_1').division_id)
        # get object
        company_api_1 = Company.objects.get(company_name='company_api_1')
        # login testuser
        self.client.login(username='testuser_company_api', password='tvjnIPBlhP9P3ixDHVE7')
        # create url
        destination = urllib.parse.quote('/api/company/' + str(company_api_1.company_id) + '/', safe='/')
        # create PUT string
        putstring = {
            "company_name": "new_company_api_1",
            "division": division_id,
        }
        # get response
        response = self.client.put(destination, data=putstring, content_type='application/json')
        # compare
        self.assertEqual(response.status_code, 200)

    def test_company_detail_api_redirect(self):
        """ test redirect with appending slash """

        # get object
        company_api_1 = Company.objects.get(company_name='company_api_1')
        # login testuser
        self.client.login(username='testuser_company_api', password='tvjnIPBlhP9P3ixDHVE7')
        # create url
        destination = urllib.parse.quote('/api/company/' + str(company_api_1.company_id) + '/', safe='/')
        # get response
        response = self.client.get('/api/company/' + str(company_api_1.company_id), follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=301, target_status_code=200)
