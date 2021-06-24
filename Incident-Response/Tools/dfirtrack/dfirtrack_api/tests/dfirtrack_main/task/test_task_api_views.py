from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone
from dfirtrack_main.models import System, Systemstatus, Tag, Tagcolor, Task, Taskname, Taskpriority, Taskstatus
import urllib.parse

class TaskAPIViewTestCase(TestCase):
    """ task API view tests """

    @classmethod
    def setUpTestData(cls):

        # create user
        test_user = User.objects.create_user(username='testuser_task_api', password='jmvsz1Z551zZ4E3Cnp8D')

        # create mandatory foreign key objects

        # create object
        systemstatus_1 = Systemstatus.objects.create(systemstatus_name='systemstatus_1')
        # create object
        taskname_1 = Taskname.objects.create(taskname_name='taskname_1')
        # create object
        Taskname.objects.create(taskname_name='taskname_2')
        # create object
        Taskname.objects.create(taskname_name='taskname_3')
        # create object
        taskpriority_1 = Taskpriority.objects.create(taskpriority_name='prio_1')
        # create object
        Taskpriority.objects.create(taskpriority_name='prio_2')
        # create object
        Taskpriority.objects.create(taskpriority_name='prio_3')
        # create object
        taskstatus_1 = Taskstatus.objects.create(taskstatus_name='taskstatus_1')

        # create optional foreign key objects

        # create object
        tagcolor_1 = Tagcolor.objects.create(tagcolor_name='tagcolor_1')
        # create object
        Tag.objects.create(
            tagcolor = tagcolor_1,
            tag_name = 'tag_1',
        )

        # create object
        System.objects.create(
            system_name = 'system_api_1',
            systemstatus = systemstatus_1,
            system_modify_time = timezone.now(),
            system_created_by_user_id = test_user,
            system_modified_by_user_id = test_user,
        )

        # create object
        Task.objects.create(
            taskname = taskname_1,
            taskpriority = taskpriority_1,
            taskstatus = taskstatus_1,
            task_created_by_user_id = test_user,
            task_modified_by_user_id = test_user,
        )

        # create object
        taskname_parent = Taskname.objects.create(taskname_name='taskname_parent')

        # create object
        Task.objects.create(
            taskname = taskname_parent,
            taskpriority = taskpriority_1,
            taskstatus = taskstatus_1,
            task_created_by_user_id = test_user,
            task_modified_by_user_id = test_user,
        )

    def test_task_list_api_unauthorized(self):
        """ unauthorized access is forbidden"""

        # get response
        response = self.client.get('/api/task/')
        # compare
        self.assertEqual(response.status_code, 401)

    def test_task_list_api_method_get(self):
        """ GET is allowed """

        # login testuser
        self.client.login(username='testuser_task_api', password='jmvsz1Z551zZ4E3Cnp8D')
        # get response
        response = self.client.get('/api/task/')
        # compare
        self.assertEqual(response.status_code, 200)

    def test_task_list_api_method_post(self):
        """ POST is allowed """

        # login testuser
        self.client.login(username='testuser_task_api', password='jmvsz1Z551zZ4E3Cnp8D')
        # get user
        test_user_id = User.objects.get(username='testuser_task_api').id
        # get object
        taskname_id = Taskname.objects.get(taskname_name='taskname_2').taskname_id
        # get object
        taskpriority_id = Taskpriority.objects.get(taskpriority_name='prio_1').taskpriority_id
        # get object
        taskstatus_id = Taskstatus.objects.get(taskstatus_name='taskstatus_1').taskstatus_id
        # create POST string
        poststring = {
            "taskname": taskname_id,
            "taskpriority": taskpriority_id,
            "taskstatus": taskstatus_id,
            "task_created_by_user_id": test_user_id,
            "task_modified_by_user_id": test_user_id,
        }
        # get response
        response = self.client.post('/api/task/', data=poststring, content_type='application/json')
        # compare
        self.assertEqual(response.status_code, 201)

    def test_task_list_api_method_post_all_id(self):
        """ POST is allowed """

        # login testuser
        self.client.login(username='testuser_task_api', password='jmvsz1Z551zZ4E3Cnp8D')
        # get user
        test_user_id = User.objects.get(username='testuser_task_api').id
        # get object
        taskname_id = Taskname.objects.get(taskname_name='taskname_3').taskname_id
        # get object
        taskpriority_id = Taskpriority.objects.get(taskpriority_name='prio_1').taskpriority_id
        # get object
        taskstatus_id = Taskstatus.objects.get(taskstatus_name='taskstatus_1').taskstatus_id
        # get object
        taskname_parent_id = Taskname.objects.get(taskname_name='taskname_parent').taskname_id
        # get object
        parenttask_id = Task.objects.get(taskname=taskname_parent_id).task_id
        # get object
        system_id = System.objects.get(system_name='system_api_1').system_id
        # get object
        tag_id = Tag.objects.get(tag_name='tag_1').tag_id
        # create POST string
        poststring = {
            "parent_task": parenttask_id,
            "system": system_id,
            "tag": [
                tag_id,
            ],
            "taskname": taskname_id,
            "taskpriority": taskpriority_id,
            "taskstatus": taskstatus_id,
            "task_scheduled_time": timezone.now().strftime('%Y-%m-%dT%H:%M'),
            "task_started_time": timezone.now().strftime('%Y-%m-%dT%H:%M'),
            "task_finished_time": timezone.now().strftime('%Y-%m-%dT%H:%M'),
            "task_due_time": timezone.now().strftime('%Y-%m-%dT%H:%M'),
            "task_assigned_to_user_id": test_user_id,
            "task_created_by_user_id": test_user_id,
            "task_modified_by_user_id": test_user_id,
        }
        # get response
        response = self.client.post('/api/task/', data=poststring, content_type='application/json')
        # compare
        self.assertEqual(response.status_code, 201)

    def test_task_list_api_redirect(self):
        """ test redirect with appending slash """

        # login testuser
        self.client.login(username='testuser_task_api', password='jmvsz1Z551zZ4E3Cnp8D')
        # create url
        destination = urllib.parse.quote('/api/task/', safe='/')
        # get response
        response = self.client.get('/api/task', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=301, target_status_code=200)

    def test_task_detail_api_unauthorized (self):
        """ unauthorized access is forbidden"""

        # get object
        taskname_id = Taskname.objects.get(taskname_name='taskname_1').taskname_id
        # get object
        task_api_1 = Task.objects.get(
            taskname = taskname_id,
        )
        # get response
        response = self.client.get('/api/task/' + str(task_api_1.task_id) + '/')
        # compare
        self.assertEqual(response.status_code, 401)

    def test_task_detail_api_method_get(self):
        """ GET is allowed """

        # login testuser
        self.client.login(username='testuser_task_api', password='jmvsz1Z551zZ4E3Cnp8D')
        # get object
        taskname_id = Taskname.objects.get(taskname_name='taskname_1').taskname_id
        # get object
        task_api_1 = Task.objects.get(
            taskname = taskname_id,
        )
        # get response
        response = self.client.get('/api/task/' + str(task_api_1.task_id) + '/')
        # compare
        self.assertEqual(response.status_code, 200)

    def test_task_detail_api_method_delete(self):
        """ DELETE is forbidden """

        # login testuser
        self.client.login(username='testuser_task_api', password='jmvsz1Z551zZ4E3Cnp8D')
        # get object
        taskname_id = Taskname.objects.get(taskname_name='taskname_1').taskname_id
        # get object
        task_api_1 = Task.objects.get(
            taskname = taskname_id,
        )
        # get response
        response = self.client.delete('/api/task/' + str(task_api_1.task_id) + '/')
        # compare
        self.assertEqual(response.status_code, 405)

    def test_task_detail_api_method_put(self):
        """ PUT is allowed """

        # login testuser
        self.client.login(username='testuser_task_api', password='jmvsz1Z551zZ4E3Cnp8D')
        # get user
        test_user_id = User.objects.get(username='testuser_task_api').id
        # get object
        taskname_id = Taskname.objects.get(taskname_name='taskname_1').taskname_id
        # get object
        new_taskpriority_id = Taskpriority.objects.get(taskpriority_name='prio_2').taskpriority_id
        # get object
        taskstatus_id = Taskstatus.objects.get(taskstatus_name='taskstatus_1').taskstatus_id
        # get object
        task_api_1 = Task.objects.get(
            taskname = taskname_id,
        )
        # create url
        destination = urllib.parse.quote('/api/task/' + str(task_api_1.task_id) + '/', safe='/')
        # create PUT string
        putstring = {
            "taskname": taskname_id,
            "taskpriority": new_taskpriority_id,
            "taskstatus": taskstatus_id,
            "task_created_by_user_id": test_user_id,
            "task_modified_by_user_id": test_user_id,
        }
        # get response
        response = self.client.put(destination, data=putstring, content_type='application/json')
        # compare
        self.assertEqual(response.status_code, 200)

    def test_task_detail_api_method_put_all_id(self):
        """ PUT is allowed """

        # login testuser
        self.client.login(username='testuser_task_api', password='jmvsz1Z551zZ4E3Cnp8D')
        # get user
        test_user_id = User.objects.get(username='testuser_task_api').id
        # get object
        taskname_id = Taskname.objects.get(taskname_name='taskname_1').taskname_id
        # get object
        new_taskpriority_id = Taskpriority.objects.get(taskpriority_name='prio_3').taskpriority_id
        # get object
        taskstatus_id = Taskstatus.objects.get(taskstatus_name='taskstatus_1').taskstatus_id
        # get object
        task_api_1 = Task.objects.get(
            taskname = taskname_id,
        )
        # get object
        taskname_parent_id = Taskname.objects.get(taskname_name='taskname_parent').taskname_id
        # get object
        parenttask_id = Task.objects.get(taskname=taskname_parent_id).task_id
        # get object
        system_id = System.objects.get(system_name='system_api_1').system_id
        # get object
        tag_id = Tag.objects.get(tag_name='tag_1').tag_id
        # create url
        destination = urllib.parse.quote('/api/task/' + str(task_api_1.task_id) + '/', safe='/')
        # create PUT string
        putstring = {
            "parent_task": parenttask_id,
            "system": system_id,
            "tag": [
                tag_id,
            ],
            "taskname": taskname_id,
            "taskpriority": new_taskpriority_id,
            "taskstatus": taskstatus_id,
            "task_scheduled_time": timezone.now().strftime('%Y-%m-%dT%H:%M'),
            "task_started_time": timezone.now().strftime('%Y-%m-%dT%H:%M'),
            "task_finished_time": timezone.now().strftime('%Y-%m-%dT%H:%M'),
            "task_due_time": timezone.now().strftime('%Y-%m-%dT%H:%M'),
            "task_assigned_to_user_id": test_user_id,
            "task_created_by_user_id": test_user_id,
            "task_modified_by_user_id": test_user_id,
        }
        # get response
        response = self.client.put(destination, data=putstring, content_type='application/json')
        # compare
        self.assertEqual(response.status_code, 200)

    def test_task_detail_api_redirect(self):
        """ test redirect with appending slash """

        # login testuser
        self.client.login(username='testuser_task_api', password='jmvsz1Z551zZ4E3Cnp8D')
        # get object
        taskname_id = Taskname.objects.get(taskname_name='taskname_1').taskname_id
        # get object
        task_api_1 = Task.objects.get(
            taskname = taskname_id,
        )
        # create url
        destination = urllib.parse.quote('/api/task/' + str(task_api_1.task_id) + '/', safe='/')
        # get response
        response = self.client.get('/api/task/' + str(task_api_1.task_id), follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=301, target_status_code=200)
