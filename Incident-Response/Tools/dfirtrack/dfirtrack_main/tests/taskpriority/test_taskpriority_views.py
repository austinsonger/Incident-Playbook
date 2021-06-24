from django.contrib.auth.models import User
from django.test import TestCase
from dfirtrack_main.models import Taskpriority
import urllib.parse

class TaskpriorityViewTestCase(TestCase):
    """ taskpriority view tests """

    @classmethod
    def setUpTestData(cls):

        # create object
        Taskpriority.objects.create(taskpriority_name='prio_1')
        # create user
        User.objects.create_user(username='testuser_taskpriority', password='VxuP85UUDkfXwRuwRFqA')

    def test_taskpriority_list_not_logged_in(self):
        """ test list view """

        # create url
        destination = '/login/?next=' + urllib.parse.quote('/taskpriority/', safe='')
        # get response
        response = self.client.get('/taskpriority/', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)

    def test_taskpriority_list_logged_in(self):
        """ test list view """

        # login testuser
        self.client.login(username='testuser_taskpriority', password='VxuP85UUDkfXwRuwRFqA')
        # get response
        response = self.client.get('/taskpriority/')
        # compare
        self.assertEqual(response.status_code, 200)

    def test_taskpriority_list_template(self):
        """ test list view """

        # login testuser
        self.client.login(username='testuser_taskpriority', password='VxuP85UUDkfXwRuwRFqA')
        # get response
        response = self.client.get('/taskpriority/')
        # compare
        self.assertTemplateUsed(response, 'dfirtrack_main/taskpriority/taskpriority_list.html')

    def test_taskpriority_list_get_user_context(self):
        """ test list view """

        # login testuser
        self.client.login(username='testuser_taskpriority', password='VxuP85UUDkfXwRuwRFqA')
        # get response
        response = self.client.get('/taskpriority/')
        # compare
        self.assertEqual(str(response.context['user']), 'testuser_taskpriority')

    def test_taskpriority_list_redirect(self):
        """ test list view """

        # login testuser
        self.client.login(username='testuser_taskpriority', password='VxuP85UUDkfXwRuwRFqA')
        # create url
        destination = urllib.parse.quote('/taskpriority/', safe='/')
        # get response
        response = self.client.get('/taskpriority', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=301, target_status_code=200)

    def test_taskpriority_detail_not_logged_in(self):
        """ test detail view """

        # get object
        taskpriority_1 = Taskpriority.objects.get(taskpriority_name='prio_1')
        # create url
        destination = '/login/?next=' + urllib.parse.quote('/taskpriority/' + str(taskpriority_1.taskpriority_id) + '/', safe='')
        # get response
        response = self.client.get('/taskpriority/' + str(taskpriority_1.taskpriority_id) + '/', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)

    def test_taskpriority_detail_logged_in(self):
        """ test detail view """

        # get object
        taskpriority_1 = Taskpriority.objects.get(taskpriority_name='prio_1')
        # login testuser
        self.client.login(username='testuser_taskpriority', password='VxuP85UUDkfXwRuwRFqA')
        # get response
        response = self.client.get('/taskpriority/' + str(taskpriority_1.taskpriority_id) + '/')
        # compare
        self.assertEqual(response.status_code, 200)

    def test_taskpriority_detail_template(self):
        """ test detail view """

        # get object
        taskpriority_1 = Taskpriority.objects.get(taskpriority_name='prio_1')
        # login testuser
        self.client.login(username='testuser_taskpriority', password='VxuP85UUDkfXwRuwRFqA')
        # get response
        response = self.client.get('/taskpriority/' + str(taskpriority_1.taskpriority_id) + '/')
        # compare
        self.assertTemplateUsed(response, 'dfirtrack_main/taskpriority/taskpriority_detail.html')

    def test_taskpriority_detail_get_user_context(self):
        """ test detail view """

        # get object
        taskpriority_1 = Taskpriority.objects.get(taskpriority_name='prio_1')
        # login testuser
        self.client.login(username='testuser_taskpriority', password='VxuP85UUDkfXwRuwRFqA')
        # get response
        response = self.client.get('/taskpriority/' + str(taskpriority_1.taskpriority_id) + '/')
        # compare
        self.assertEqual(str(response.context['user']), 'testuser_taskpriority')

    def test_taskpriority_detail_redirect(self):
        """ test detail view """

        # get object
        taskpriority_1 = Taskpriority.objects.get(taskpriority_name='prio_1')
        # login testuser
        self.client.login(username='testuser_taskpriority', password='VxuP85UUDkfXwRuwRFqA')
        # create url
        destination = urllib.parse.quote('/taskpriority/' + str(taskpriority_1.taskpriority_id) + '/', safe='/')
        # get response
        response = self.client.get('/taskpriority/' + str(taskpriority_1.taskpriority_id), follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=301, target_status_code=200)
