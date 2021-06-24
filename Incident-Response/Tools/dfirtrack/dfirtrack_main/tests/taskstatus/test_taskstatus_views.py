from django.contrib.auth.models import User
from django.test import TestCase
from dfirtrack_main.models import Taskstatus
import urllib.parse

class TaskstatusViewTestCase(TestCase):
    """ taskstatus view tests """

    @classmethod
    def setUpTestData(cls):

        # create object
        Taskstatus.objects.create(taskstatus_name='taskstatus_1')
        # create user
        User.objects.create_user(username='testuser_taskstatus', password='TZjmjiUQviOnIEral6l9')

    def test_taskstatus_list_not_logged_in(self):
        """ test list view """

        # create url
        destination = '/login/?next=' + urllib.parse.quote('/taskstatus/', safe='')
        # get response
        response = self.client.get('/taskstatus/', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)

    def test_taskstatus_list_logged_in(self):
        """ test list view """

        # login testuser
        self.client.login(username='testuser_taskstatus', password='TZjmjiUQviOnIEral6l9')
        # get response
        response = self.client.get('/taskstatus/')
        # compare
        self.assertEqual(response.status_code, 200)

    def test_taskstatus_list_template(self):
        """ test list view """

        # login testuser
        self.client.login(username='testuser_taskstatus', password='TZjmjiUQviOnIEral6l9')
        # get response
        response = self.client.get('/taskstatus/')
        # compare
        self.assertTemplateUsed(response, 'dfirtrack_main/taskstatus/taskstatus_list.html')

    def test_taskstatus_list_get_user_context(self):
        """ test list view """

        # login testuser
        self.client.login(username='testuser_taskstatus', password='TZjmjiUQviOnIEral6l9')
        # get response
        response = self.client.get('/taskstatus/')
        # compare
        self.assertEqual(str(response.context['user']), 'testuser_taskstatus')

    def test_taskstatus_list_redirect(self):
        """ test list view """

        # login testuser
        self.client.login(username='testuser_taskstatus', password='TZjmjiUQviOnIEral6l9')
        # create url
        destination = urllib.parse.quote('/taskstatus/', safe='/')
        # get response
        response = self.client.get('/taskstatus', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=301, target_status_code=200)

    def test_taskstatus_detail_not_logged_in(self):
        """ test detail view """

        # get object
        taskstatus_1 = Taskstatus.objects.get(taskstatus_name='taskstatus_1')
        # create url
        destination = '/login/?next=' + urllib.parse.quote('/taskstatus/' + str(taskstatus_1.taskstatus_id) + '/', safe='')
        # get response
        response = self.client.get('/taskstatus/' + str(taskstatus_1.taskstatus_id) + '/', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)

    def test_taskstatus_detail_logged_in(self):
        """ test detail view """

        # get object
        taskstatus_1 = Taskstatus.objects.get(taskstatus_name='taskstatus_1')
        # login testuser
        self.client.login(username='testuser_taskstatus', password='TZjmjiUQviOnIEral6l9')
        # get response
        response = self.client.get('/taskstatus/' + str(taskstatus_1.taskstatus_id) + '/')
        # compare
        self.assertEqual(response.status_code, 200)

    def test_taskstatus_detail_template(self):
        """ test detail view """

        # get object
        taskstatus_1 = Taskstatus.objects.get(taskstatus_name='taskstatus_1')
        # login testuser
        self.client.login(username='testuser_taskstatus', password='TZjmjiUQviOnIEral6l9')
        # get response
        response = self.client.get('/taskstatus/' + str(taskstatus_1.taskstatus_id) + '/')
        # compare
        self.assertTemplateUsed(response, 'dfirtrack_main/taskstatus/taskstatus_detail.html')

    def test_taskstatus_detail_get_user_context(self):
        """ test detail view """

        # get object
        taskstatus_1 = Taskstatus.objects.get(taskstatus_name='taskstatus_1')
        # login testuser
        self.client.login(username='testuser_taskstatus', password='TZjmjiUQviOnIEral6l9')
        # get response
        response = self.client.get('/taskstatus/' + str(taskstatus_1.taskstatus_id) + '/')
        # compare
        self.assertEqual(str(response.context['user']), 'testuser_taskstatus')

    def test_taskstatus_detail_redirect(self):
        """ test detail view """

        # get object
        taskstatus_1 = Taskstatus.objects.get(taskstatus_name='taskstatus_1')
        # login testuser
        self.client.login(username='testuser_taskstatus', password='TZjmjiUQviOnIEral6l9')
        # create url
        destination = urllib.parse.quote('/taskstatus/' + str(taskstatus_1.taskstatus_id) + '/', safe='/')
        # get response
        response = self.client.get('/taskstatus/' + str(taskstatus_1.taskstatus_id), follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=301, target_status_code=200)
