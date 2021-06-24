from django.contrib.auth.models import User
from django.test import TestCase
from dfirtrack_main.models import Tagcolor
import urllib.parse

class TagcolorAPIViewTestCase(TestCase):
    """ tagcolor API view tests """

    @classmethod
    def setUpTestData(cls):

        # create object
        Tagcolor.objects.create(tagcolor_name='tagcolor_api_1')
        # create user
        User.objects.create_user(username='testuser_tagcolor_api', password='twvVpQ4LBNN9swnJcy2f')

    def test_tagcolor_list_api_unauthorized(self):
        """ unauthorized access is forbidden"""

        # get response
        response = self.client.get('/api/tagcolor/')
        # compare
        self.assertEqual(response.status_code, 401)

    def test_tagcolor_list_api_method_get(self):
        """ GET is allowed """

        # login testuser
        self.client.login(username='testuser_tagcolor_api', password='twvVpQ4LBNN9swnJcy2f')
        # get response
        response = self.client.get('/api/tagcolor/')
        # compare
        self.assertEqual(response.status_code, 200)

    def test_tagcolor_list_api_method_post(self):
        """ POST is forbidden """

        # login testuser
        self.client.login(username='testuser_tagcolor_api', password='twvVpQ4LBNN9swnJcy2f')
        # create POST string
        poststring = {"tagcolor_name": "tagcolor_api_2"}
        # get response
        response = self.client.post('/api/tagcolor/', data=poststring)
        # compare
        self.assertEqual(response.status_code, 405)

    def test_tagcolor_list_api_redirect(self):
        """ test redirect with appending slash """

        # login testuser
        self.client.login(username='testuser_tagcolor_api', password='twvVpQ4LBNN9swnJcy2f')
        # create url
        destination = urllib.parse.quote('/api/tagcolor/', safe='/')
        # get response
        response = self.client.get('/api/tagcolor', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=301, target_status_code=200)

    def test_tagcolor_detail_api_unauthorized (self):
        """ unauthorized access is forbidden"""

        # get object
        tagcolor_api_1 = Tagcolor.objects.get(tagcolor_name='tagcolor_api_1')
        # get response
        response = self.client.get('/api/tagcolor/' + str(tagcolor_api_1.tagcolor_id) + '/')
        # compare
        self.assertEqual(response.status_code, 401)

    def test_tagcolor_detail_api_method_get(self):
        """ GET is allowed """

        # get object
        tagcolor_api_1 = Tagcolor.objects.get(tagcolor_name='tagcolor_api_1')
        # login testuser
        self.client.login(username='testuser_tagcolor_api', password='twvVpQ4LBNN9swnJcy2f')
        # get response
        response = self.client.get('/api/tagcolor/' + str(tagcolor_api_1.tagcolor_id) + '/')
        # compare
        self.assertEqual(response.status_code, 200)

    def test_tagcolor_detail_api_method_delete(self):
        """ DELETE is forbidden """

        # get object
        tagcolor_api_1 = Tagcolor.objects.get(tagcolor_name='tagcolor_api_1')
        # login testuser
        self.client.login(username='testuser_tagcolor_api', password='twvVpQ4LBNN9swnJcy2f')
        # get response
        response = self.client.delete('/api/tagcolor/' + str(tagcolor_api_1.tagcolor_id) + '/')
        # compare
        self.assertEqual(response.status_code, 405)

    def test_tagcolor_detail_api_method_put(self):
        """ PUT is forbidden """

        # get object
        tagcolor_api_1 = Tagcolor.objects.get(tagcolor_name='tagcolor_api_1')
        # login testuser
        self.client.login(username='testuser_tagcolor_api', password='twvVpQ4LBNN9swnJcy2f')
        # create url
        destination = urllib.parse.quote('/api/tagcolor/' + str(tagcolor_api_1.tagcolor_id) + '/', safe='/')
        # create PUT string
        putstring = {"tagcolor_name": "new_tagcolor_api_1"}
        # get response
        response = self.client.put(destination, data=putstring, content_type='application/json')
        # compare
        self.assertEqual(response.status_code, 405)

    def test_tagcolor_detail_api_redirect(self):
        """ test redirect with appending slash """

        # get object
        tagcolor_api_1 = Tagcolor.objects.get(tagcolor_name='tagcolor_api_1')
        # login testuser
        self.client.login(username='testuser_tagcolor_api', password='twvVpQ4LBNN9swnJcy2f')
        # create url
        destination = urllib.parse.quote('/api/tagcolor/' + str(tagcolor_api_1.tagcolor_id) + '/', safe='/')
        # get response
        response = self.client.get('/api/tagcolor/' + str(tagcolor_api_1.tagcolor_id), follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=301, target_status_code=200)
