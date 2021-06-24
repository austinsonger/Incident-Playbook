from django.contrib.auth.models import User
from django.test import TestCase
from dfirtrack_main.models import Taskstatus
import urllib.parse

class TaskstatusAPIViewTestCase(TestCase):
    """ taskstatus API view tests """

    @classmethod
    def setUpTestData(cls):

        # create object
        Taskstatus.objects.create(taskstatus_name='taskstatus_api_1')
        # create user
        User.objects.create_user(username='testuser_taskstatus_api', password='aCTVRIdJ4cyVSkYiJKrM')

    def test_taskstatus_list_api_unauthorized(self):
        """ unauthorized access is forbidden"""

        # get response
        response = self.client.get('/api/taskstatus/')
        # compare
        self.assertEqual(response.status_code, 401)

    def test_taskstatus_list_api_method_get(self):
        """ GET is allowed """

        # login testuser
        self.client.login(username='testuser_taskstatus_api', password='aCTVRIdJ4cyVSkYiJKrM')
        # get response
        response = self.client.get('/api/taskstatus/')
        # compare
        self.assertEqual(response.status_code, 200)

    def test_taskstatus_list_api_method_post(self):
        """ POST is forbidden """

        # login testuser
        self.client.login(username='testuser_taskstatus_api', password='aCTVRIdJ4cyVSkYiJKrM')
        # create POST string
        poststring = {"taskstatus_name": "taskstatus_api_2"}
        # get response
        response = self.client.post('/api/taskstatus/', data=poststring)
        # compare
        self.assertEqual(response.status_code, 405)

    def test_taskstatus_list_api_redirect(self):
        """ test redirect with appending slash """

        # login testuser
        self.client.login(username='testuser_taskstatus_api', password='aCTVRIdJ4cyVSkYiJKrM')
        # create url
        destination = urllib.parse.quote('/api/taskstatus/', safe='/')
        # get response
        response = self.client.get('/api/taskstatus', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=301, target_status_code=200)

    def test_taskstatus_detail_api_unauthorized (self):
        """ unauthorized access is forbidden"""

        # get object
        taskstatus_api_1 = Taskstatus.objects.get(taskstatus_name='taskstatus_api_1')
        # get response
        response = self.client.get('/api/taskstatus/' + str(taskstatus_api_1.taskstatus_id) + '/')
        # compare
        self.assertEqual(response.status_code, 401)

    def test_taskstatus_detail_api_method_get(self):
        """ GET is allowed """

        # get object
        taskstatus_api_1 = Taskstatus.objects.get(taskstatus_name='taskstatus_api_1')
        # login testuser
        self.client.login(username='testuser_taskstatus_api', password='aCTVRIdJ4cyVSkYiJKrM')
        # get response
        response = self.client.get('/api/taskstatus/' + str(taskstatus_api_1.taskstatus_id) + '/')
        # compare
        self.assertEqual(response.status_code, 200)

    def test_taskstatus_detail_api_method_delete(self):
        """ DELETE is forbidden """

        # get object
        taskstatus_api_1 = Taskstatus.objects.get(taskstatus_name='taskstatus_api_1')
        # login testuser
        self.client.login(username='testuser_taskstatus_api', password='aCTVRIdJ4cyVSkYiJKrM')
        # get response
        response = self.client.delete('/api/taskstatus/' + str(taskstatus_api_1.taskstatus_id) + '/')
        # compare
        self.assertEqual(response.status_code, 405)

    def test_taskstatus_detail_api_method_put(self):
        """ PUT is forbidden """

        # get object
        taskstatus_api_1 = Taskstatus.objects.get(taskstatus_name='taskstatus_api_1')
        # login testuser
        self.client.login(username='testuser_taskstatus_api', password='aCTVRIdJ4cyVSkYiJKrM')
        # create url
        destination = urllib.parse.quote('/api/taskstatus/' + str(taskstatus_api_1.taskstatus_id) + '/', safe='/')
        # create PUT string
        putstring = {"taskstatus_name": "new_taskstatus_api_1"}
        # get response
        response = self.client.put(destination, data=putstring, content_type='application/json')
        # compare
        self.assertEqual(response.status_code, 405)

    def test_taskstatus_detail_api_redirect(self):
        """ test redirect with appending slash """

        # get object
        taskstatus_api_1 = Taskstatus.objects.get(taskstatus_name='taskstatus_api_1')
        # login testuser
        self.client.login(username='testuser_taskstatus_api', password='aCTVRIdJ4cyVSkYiJKrM')
        # create url
        destination = urllib.parse.quote('/api/taskstatus/' + str(taskstatus_api_1.taskstatus_id) + '/', safe='/')
        # get response
        response = self.client.get('/api/taskstatus/' + str(taskstatus_api_1.taskstatus_id), follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=301, target_status_code=200)
