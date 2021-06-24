from django.contrib.auth.models import User
from django.test import TestCase
from dfirtrack_main.models import Contact
import urllib.parse

class ContactAPIViewTestCase(TestCase):
    """ contact API view tests """

    @classmethod
    def setUpTestData(cls):

        # create object
        Contact.objects.create(
            contact_name='contact_api_1',
            contact_email='contact@example.com',
        )
        # create user
        User.objects.create_user(username='testuser_contact_api', password='tvjnIPBlhP9P3ixDHVE7')

    def test_contact_list_api_unauthorized(self):
        """ unauthorized access is forbidden"""

        # get response
        response = self.client.get('/api/contact/')
        # compare
        self.assertEqual(response.status_code, 401)

    def test_contact_list_api_method_get(self):
        """ GET is allowed """

        # login testuser
        self.client.login(username='testuser_contact_api', password='tvjnIPBlhP9P3ixDHVE7')
        # get response
        response = self.client.get('/api/contact/')
        # compare
        self.assertEqual(response.status_code, 200)

    def test_contact_list_api_method_post(self):
        """ POST is allowed """

        # login testuser
        self.client.login(username='testuser_contact_api', password='tvjnIPBlhP9P3ixDHVE7')
        # create POST string
        poststring = {
            'contact_name': 'contact_api_2',
            'contact_email': 'contact2@example.com',
        }
        # get response
        response = self.client.post('/api/contact/', data=poststring)
        # compare
        self.assertEqual(response.status_code, 201)

    def test_contact_list_api_redirect(self):
        """ test redirect with appending slash """

        # login testuser
        self.client.login(username='testuser_contact_api', password='tvjnIPBlhP9P3ixDHVE7')
        # create url
        destination = urllib.parse.quote('/api/contact/', safe='/')
        # get response
        response = self.client.get('/api/contact', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=301, target_status_code=200)

    def test_contact_detail_api_unauthorized (self):
        """ unauthorized access is forbidden"""

        # get object
        contact_api_1 = Contact.objects.get(contact_name='contact_api_1')
        # get response
        response = self.client.get('/api/contact/' + str(contact_api_1.contact_id) + '/')
        # compare
        self.assertEqual(response.status_code, 401)

    def test_contact_detail_api_method_get(self):
        """ GET is allowed """

        # get object
        contact_api_1 = Contact.objects.get(contact_name='contact_api_1')
        # login testuser
        self.client.login(username='testuser_contact_api', password='tvjnIPBlhP9P3ixDHVE7')
        # get response
        response = self.client.get('/api/contact/' + str(contact_api_1.contact_id) + '/')
        # compare
        self.assertEqual(response.status_code, 200)

    def test_contact_detail_api_method_delete(self):
        """ DELETE is forbidden """

        # get object
        contact_api_1 = Contact.objects.get(contact_name='contact_api_1')
        # login testuser
        self.client.login(username='testuser_contact_api', password='tvjnIPBlhP9P3ixDHVE7')
        # get response
        response = self.client.delete('/api/contact/' + str(contact_api_1.contact_id) + '/')
        # compare
        self.assertEqual(response.status_code, 405)

    def test_contact_detail_api_method_put(self):
        """ PUT is allowed """

        # get object
        contact_api_1 = Contact.objects.get(contact_name='contact_api_1')
        # login testuser
        self.client.login(username='testuser_contact_api', password='tvjnIPBlhP9P3ixDHVE7')
        # create url
        destination = urllib.parse.quote('/api/contact/' + str(contact_api_1.contact_id) + '/', safe='/')
        # create PUT string
        putstring = {
            'contact_name': 'new_contact_api_1',
            'contact_email': 'contact@example.com',
        }
        # get response
        response = self.client.put(destination, data=putstring, content_type='application/json')
        # compare
        self.assertEqual(response.status_code, 200)

    def test_contact_detail_api_redirect(self):
        """ test redirect with appending slash """

        # get object
        contact_api_1 = Contact.objects.get(contact_name='contact_api_1')
        # login testuser
        self.client.login(username='testuser_contact_api', password='tvjnIPBlhP9P3ixDHVE7')
        # create url
        destination = urllib.parse.quote('/api/contact/' + str(contact_api_1.contact_id) + '/', safe='/')
        # get response
        response = self.client.get('/api/contact/' + str(contact_api_1.contact_id), follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=301, target_status_code=200)
