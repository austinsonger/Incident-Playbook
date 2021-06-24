from django.contrib.auth.models import User
from django.test import TestCase
from dfirtrack_main.models import Ip
import urllib.parse

class IpViewTestCase(TestCase):
    """ ip view tests """

    @classmethod
    def setUpTestData(cls):

        # create object
        Ip.objects.create(ip_ip='127.0.0.1')
        # create user
        User.objects.create_user(username='testuser_ip', password='pRs9Ap7oc9W0yjLfnP2Y')

    def test_ip_list_not_logged_in(self):
        """ test list view """

        # create url
        destination = '/login/?next=' + urllib.parse.quote('/ip/', safe='')
        # get response
        response = self.client.get('/ip/', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)

    def test_ip_list_logged_in(self):
        """ test list view """

        # login testuser
        self.client.login(username='testuser_ip', password='pRs9Ap7oc9W0yjLfnP2Y')
        # get response
        response = self.client.get('/ip/')
        # compare
        self.assertEqual(response.status_code, 200)

    def test_ip_list_template(self):
        """ test list view """

        # login testuser
        self.client.login(username='testuser_ip', password='pRs9Ap7oc9W0yjLfnP2Y')
        # get response
        response = self.client.get('/ip/')
        # compare
        self.assertTemplateUsed(response, 'dfirtrack_main/ip/ip_list.html')

    def test_ip_list_get_user_context(self):
        """ test list view """

        # login testuser
        self.client.login(username='testuser_ip', password='pRs9Ap7oc9W0yjLfnP2Y')
        # get response
        response = self.client.get('/ip/')
        # compare
        self.assertEqual(str(response.context['user']), 'testuser_ip')

    def test_ip_list_redirect(self):
        """ test list view """

        # login testuser
        self.client.login(username='testuser_ip', password='pRs9Ap7oc9W0yjLfnP2Y')
        # create url
        destination = urllib.parse.quote('/ip/', safe='/')
        # get response
        response = self.client.get('/ip', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=301, target_status_code=200)

    def test_ip_detail_not_logged_in(self):
        """ test detail view """

        # get object
        ip_1 = Ip.objects.get(ip_ip='127.0.0.1')
        # create url
        destination = '/login/?next=' + urllib.parse.quote('/ip/' + str(ip_1.ip_id) + '/', safe='')
        # get response
        response = self.client.get('/ip/' + str(ip_1.ip_id) + '/', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)

    def test_ip_detail_logged_in(self):
        """ test detail view """

        # get object
        ip_1 = Ip.objects.get(ip_ip='127.0.0.1')
        # login testuser
        self.client.login(username='testuser_ip', password='pRs9Ap7oc9W0yjLfnP2Y')
        # get response
        response = self.client.get('/ip/' + str(ip_1.ip_id) + '/')
        # compare
        self.assertEqual(response.status_code, 200)

    def test_ip_detail_template(self):
        """ test detail view """

        # get object
        ip_1 = Ip.objects.get(ip_ip='127.0.0.1')
        # login testuser
        self.client.login(username='testuser_ip', password='pRs9Ap7oc9W0yjLfnP2Y')
        # get response
        response = self.client.get('/ip/' + str(ip_1.ip_id) + '/')
        # compare
        self.assertTemplateUsed(response, 'dfirtrack_main/ip/ip_detail.html')

    def test_ip_detail_get_user_context(self):
        """ test detail view """

        # get object
        ip_1 = Ip.objects.get(ip_ip='127.0.0.1')
        # login testuser
        self.client.login(username='testuser_ip', password='pRs9Ap7oc9W0yjLfnP2Y')
        # get response
        response = self.client.get('/ip/' + str(ip_1.ip_id) + '/')
        # compare
        self.assertEqual(str(response.context['user']), 'testuser_ip')

    def test_ip_detail_redirect(self):
        """ test detail view """

        # get object
        ip_1 = Ip.objects.get(ip_ip='127.0.0.1')
        # login testuser
        self.client.login(username='testuser_ip', password='pRs9Ap7oc9W0yjLfnP2Y')
        # create url
        destination = urllib.parse.quote('/ip/' + str(ip_1.ip_id) + '/', safe='/')
        # get response
        response = self.client.get('/ip/' + str(ip_1.ip_id), follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=301, target_status_code=200)
