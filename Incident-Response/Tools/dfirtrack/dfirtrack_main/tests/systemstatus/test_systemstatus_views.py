from django.contrib.auth.models import User
from django.test import TestCase
from dfirtrack_main.models import Systemstatus
import urllib.parse

class SystemstatusViewTestCase(TestCase):
    """ systemstatus view tests """

    @classmethod
    def setUpTestData(cls):

        # create object
        Systemstatus.objects.create(systemstatus_name='systemstatus_1')
        # create user
        User.objects.create_user(username='testuser_systemstatus', password='kWAvcuNoU97qpEy7UpDT')

    def test_systemstatus_list_not_logged_in(self):
        """ test list view """

        # create url
        destination = '/login/?next=' + urllib.parse.quote('/systemstatus/', safe='')
        # get response
        response = self.client.get('/systemstatus/', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)

    def test_systemstatus_list_logged_in(self):
        """ test list view """

        # login testuser
        self.client.login(username='testuser_systemstatus', password='kWAvcuNoU97qpEy7UpDT')
        # get response
        response = self.client.get('/systemstatus/')
        # compare
        self.assertEqual(response.status_code, 200)

    def test_systemstatus_list_template(self):
        """ test list view """

        # login testuser
        self.client.login(username='testuser_systemstatus', password='kWAvcuNoU97qpEy7UpDT')
        # get response
        response = self.client.get('/systemstatus/')
        # compare
        self.assertTemplateUsed(response, 'dfirtrack_main/systemstatus/systemstatus_list.html')

    def test_systemstatus_list_get_user_context(self):
        """ test list view """

        # login testuser
        self.client.login(username='testuser_systemstatus', password='kWAvcuNoU97qpEy7UpDT')
        # get response
        response = self.client.get('/systemstatus/')
        # compare
        self.assertEqual(str(response.context['user']), 'testuser_systemstatus')

    def test_systemstatus_list_redirect(self):
        """ test list view """

        # login testuser
        self.client.login(username='testuser_systemstatus', password='kWAvcuNoU97qpEy7UpDT')
        # create url
        destination = urllib.parse.quote('/systemstatus/', safe='/')
        # get response
        response = self.client.get('/systemstatus', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=301, target_status_code=200)

    def test_systemstatus_detail_not_logged_in(self):
        """ test detail view """

        # get object
        systemstatus_1 = Systemstatus.objects.get(systemstatus_name='systemstatus_1')
        # create url
        destination = '/login/?next=' + urllib.parse.quote('/systemstatus/' + str(systemstatus_1.systemstatus_id) + '/', safe='')
        # get response
        response = self.client.get('/systemstatus/' + str(systemstatus_1.systemstatus_id) + '/', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)

    def test_systemstatus_detail_logged_in(self):
        """ test detail view """

        # get object
        systemstatus_1 = Systemstatus.objects.get(systemstatus_name='systemstatus_1')
        # login testuser
        self.client.login(username='testuser_systemstatus', password='kWAvcuNoU97qpEy7UpDT')
        # get response
        response = self.client.get('/systemstatus/' + str(systemstatus_1.systemstatus_id) + '/')
        # compare
        self.assertEqual(response.status_code, 200)

    def test_systemstatus_detail_template(self):
        """ test detail view """

        # get object
        systemstatus_1 = Systemstatus.objects.get(systemstatus_name='systemstatus_1')
        # login testuser
        self.client.login(username='testuser_systemstatus', password='kWAvcuNoU97qpEy7UpDT')
        # get response
        response = self.client.get('/systemstatus/' + str(systemstatus_1.systemstatus_id) + '/')
        # compare
        self.assertTemplateUsed(response, 'dfirtrack_main/systemstatus/systemstatus_detail.html')

    def test_systemstatus_detail_get_user_context(self):
        """ test detail view """

        # get object
        systemstatus_1 = Systemstatus.objects.get(systemstatus_name='systemstatus_1')
        # login testuser
        self.client.login(username='testuser_systemstatus', password='kWAvcuNoU97qpEy7UpDT')
        # get response
        response = self.client.get('/systemstatus/' + str(systemstatus_1.systemstatus_id) + '/')
        # compare
        self.assertEqual(str(response.context['user']), 'testuser_systemstatus')

    def test_systemstatus_detail_redirect(self):
        """ test detail view """

        # get object
        systemstatus_1 = Systemstatus.objects.get(systemstatus_name='systemstatus_1')
        # login testuser
        self.client.login(username='testuser_systemstatus', password='kWAvcuNoU97qpEy7UpDT')
        # create url
        destination = urllib.parse.quote('/systemstatus/' + str(systemstatus_1.systemstatus_id) + '/', safe='/')
        # get response
        response = self.client.get('/systemstatus/' + str(systemstatus_1.systemstatus_id), follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=301, target_status_code=200)
