from datetime import datetime
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.test import TestCase
from django.utils import timezone
from dfirtrack_main.models import System, Systemstatus, Task, Taskname, Taskpriority, Taskstatus
from mock import patch
import urllib.parse

class TaskCreatorViewTestCase(TestCase):
    """ task creator view tests """

    @classmethod
    def setUpTestData(cls):

        # create user
        test_user = User.objects.create_user(username='testuser_task_creator', password='E5BGU4meULjw7kdtvnzn')

        # create objects
        Taskname.objects.create(taskname_name = 'task_creator_taskname_1')
        Taskname.objects.create(taskname_name = 'task_creator_taskname_2')
        Taskname.objects.create(taskname_name = 'task_creator_taskname_3')
        Taskpriority.objects.create(taskpriority_name = 'taskpriority_1')

        # create object
        systemstatus_1 = Systemstatus.objects.create(systemstatus_name = 'task_creator_systemstatus_1')
        # create objects
        System.objects.create(
            system_name = 'task_creator_system_1',
            systemstatus = systemstatus_1,
            system_modify_time = timezone.now(),
            system_created_by_user_id = test_user,
            system_modified_by_user_id = test_user,
        )
        System.objects.create(
            system_name = 'task_creator_system_2',
            systemstatus = systemstatus_1,
            system_modify_time = timezone.now(),
            system_created_by_user_id = test_user,
            system_modified_by_user_id = test_user,
        )
        System.objects.create(
            system_name = 'task_creator_system_3',
            systemstatus = systemstatus_1,
            system_modify_time = timezone.now(),
            system_created_by_user_id = test_user,
            system_modified_by_user_id = test_user,
        )

    def test_task_creator_not_logged_in(self):
        """ test creator view """

        # create url
        destination = '/login/?next=' + urllib.parse.quote('/task/creator/', safe='')
        # get response
        response = self.client.get('/task/creator/', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)

    def test_task_creator_logged_in(self):
        """ test creator view """

        # login testuser
        self.client.login(username='testuser_task_creator', password='E5BGU4meULjw7kdtvnzn')
        # get response
        response = self.client.get('/task/creator/')
        # compare
        self.assertEqual(response.status_code, 200)

    def test_task_creator_template(self):
        """ test creator view """

        # login testuser
        self.client.login(username='testuser_task_creator', password='E5BGU4meULjw7kdtvnzn')
        # get response
        response = self.client.get('/task/creator/')
        # compare
        self.assertTemplateUsed(response, 'dfirtrack_main/task/task_creator.html')

    def test_task_creator_get_user_context(self):
        """ test creator view """

        # login testuser
        self.client.login(username='testuser_task_creator', password='E5BGU4meULjw7kdtvnzn')
        # get response
        response = self.client.get('/task/creator/')
        # compare
        self.assertEqual(str(response.context['user']), 'testuser_task_creator')

    def test_task_creator_redirect(self):
        """ test creator view """

        # login testuser
        self.client.login(username='testuser_task_creator', password='E5BGU4meULjw7kdtvnzn')
        # create url
        destination = urllib.parse.quote('/task/creator/', safe='/')
        # get response
        response = self.client.get('/task/creator', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=301, target_status_code=200)

    def test_task_creator_post_redirect(self):
        """ test creator view """

        # login testuser
        self.client.login(username='testuser_task_creator', password='E5BGU4meULjw7kdtvnzn')
        # get objects
        taskname_1 = Taskname.objects.get(taskname_name = 'task_creator_taskname_1')
        taskpriority_1 = Taskpriority.objects.get(taskpriority_name = 'taskpriority_1')
        taskstatus_pending = Taskstatus.objects.get(taskstatus_name = '10_pending')
        system_1 = System.objects.get(system_name = 'task_creator_system_1')
        # create post data
        data_dict = {
            'taskname': [taskname_1.taskname_id,],
            'taskpriority': taskpriority_1.taskpriority_id,
            'taskstatus': taskstatus_pending.taskstatus_id,
            'system': [system_1.system_id,],
        }
        # create url
        destination = '/task/'
        # get response
        response = self.client.post('/task/creator/', data_dict)
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)

    def test_task_creator_post_system_and_tasks(self):
        """ test creator view """

        # login testuser
        self.client.login(username='testuser_task_creator', password='E5BGU4meULjw7kdtvnzn')
        # get objects
        taskname_1 = Taskname.objects.get(taskname_name = 'task_creator_taskname_1')
        taskname_2 = Taskname.objects.get(taskname_name = 'task_creator_taskname_2')
        taskname_3 = Taskname.objects.get(taskname_name = 'task_creator_taskname_3')
        taskpriority_1 = Taskpriority.objects.get(taskpriority_name = 'taskpriority_1')
        taskstatus_pending = Taskstatus.objects.get(taskstatus_name = '10_pending')
        system_1 = System.objects.get(system_name = 'task_creator_system_1')
        system_2 = System.objects.get(system_name = 'task_creator_system_2')
        system_3 = System.objects.get(system_name = 'task_creator_system_3')
        # create post data
        data_dict = {
            'taskname': [taskname_1.taskname_id, taskname_2.taskname_id],
            'taskpriority': taskpriority_1.taskpriority_id,
            'taskstatus': taskstatus_pending.taskstatus_id,
            'system': [system_1.system_id, system_2.system_id],
        }
        # get response
        self.client.post('/task/creator/', data_dict)
        # get object
        task_1 = Task.objects.get(
            system = system_1,
            taskname = taskname_1,
        )
        # compare
        self.assertTrue(system_1.task_set.filter(taskname=taskname_1).exists())
        self.assertTrue(system_1.task_set.filter(taskname=taskname_2).exists())
        self.assertFalse(system_1.task_set.filter(taskname=taskname_3).exists())
        self.assertTrue(system_2.task_set.filter(taskname=taskname_1).exists())
        self.assertTrue(system_2.task_set.filter(taskname=taskname_2).exists())
        self.assertFalse(system_2.task_set.filter(taskname=taskname_3).exists())
        self.assertFalse(system_3.task_set.filter(taskname=taskname_1).exists())
        self.assertFalse(system_3.task_set.filter(taskname=taskname_2).exists())
        self.assertFalse(system_3.task_set.filter(taskname=taskname_3).exists())
        self.assertEqual(task_1.task_started_time, None)
        self.assertEqual(task_1.task_finished_time, None)

    def test_task_creator_post_times_working(self):
        """ test creator view """

        # mock timezone.now()
        dt = datetime(2020, 1, 2, tzinfo=timezone.utc)
        with patch.object(timezone, 'now', return_value=dt):

            # login testuser
            self.client.login(username='testuser_task_creator', password='E5BGU4meULjw7kdtvnzn')
            # get objects
            taskname_started = Taskname.objects.create(taskname_name = 'task_creator_started_time_working')
            taskpriority_1 = Taskpriority.objects.get(taskpriority_name = 'taskpriority_1')
            taskstatus_working = Taskstatus.objects.get(taskstatus_name = '20_working')
            system_1 = System.objects.get(system_name = 'task_creator_system_1')
            # create post data
            data_dict = {
                'taskname': [taskname_started.taskname_id,],
                'taskpriority': taskpriority_1.taskpriority_id,
                'taskstatus': taskstatus_working.taskstatus_id,
                'system': [system_1.system_id,],
            }
            # get response
            self.client.post('/task/creator/', data_dict)
            # get object
            task_started = Task.objects.get(
                system = system_1,
                taskname = taskname_started,
            )
            # compare
            self.assertEqual(task_started.task_started_time, timezone.now())
            self.assertEqual(task_started.task_finished_time, None)

    def test_task_creator_post_times_done(self):
        """ test creator view """

        # mock timezone.now()
        dt = datetime(2020, 3, 4, tzinfo=timezone.utc)
        with patch.object(timezone, 'now', return_value=dt):

            # login testuser
            self.client.login(username='testuser_task_creator', password='E5BGU4meULjw7kdtvnzn')
            # get objects
            taskname_finished = Taskname.objects.create(taskname_name = 'task_creator_finished_time_working')
            taskpriority_1 = Taskpriority.objects.get(taskpriority_name = 'taskpriority_1')
            taskstatus_done = Taskstatus.objects.get(taskstatus_name = '30_done')
            system_1 = System.objects.get(system_name = 'task_creator_system_1')
            # create post data
            data_dict = {
                'taskname': [taskname_finished.taskname_id,],
                'taskpriority': taskpriority_1.taskpriority_id,
                'taskstatus': taskstatus_done.taskstatus_id,
                'system': [system_1.system_id,],
            }
            # get response
            self.client.post('/task/creator/', data_dict)
            # get object
            task_finished = Task.objects.get(
                system = system_1,
                taskname = taskname_finished,
            )
            # compare
            self.assertEqual(task_finished.task_started_time, timezone.now())
            self.assertEqual(task_finished.task_finished_time, timezone.now())

    def test_task_creator_empty_redirect(self):
        """ test creator view """

        # login testuser
        self.client.login(username='testuser_task_creator', password='E5BGU4meULjw7kdtvnzn')
        # create post data
        data_dict = {}
        # create url
        destination = '/task/'
        # get response
        response = self.client.post('/task/creator/', data_dict)
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)

    def test_task_creator_post_messages(self):
        """ test creator view """

        # login testuser
        self.client.login(username='testuser_task_creator', password='E5BGU4meULjw7kdtvnzn')
        # get objects
        taskname_1 = Taskname.objects.get(taskname_name = 'task_creator_taskname_1')
        taskname_2 = Taskname.objects.get(taskname_name = 'task_creator_taskname_2')
        taskname_3 = Taskname.objects.get(taskname_name = 'task_creator_taskname_3')
        taskpriority_1 = Taskpriority.objects.get(taskpriority_name = 'taskpriority_1')
        taskstatus_pending = Taskstatus.objects.get(taskstatus_name = '10_pending')
        system_1 = System.objects.get(system_name = 'task_creator_system_1')
        system_2 = System.objects.get(system_name = 'task_creator_system_2')
        system_3 = System.objects.get(system_name = 'task_creator_system_3')
        # create post data
        data_dict = {
            'taskname': [taskname_1.taskname_id, taskname_2.taskname_id, taskname_3.taskname_id],
            'taskpriority': taskpriority_1.taskpriority_id,
            'taskstatus': taskstatus_pending.taskstatus_id,
            'system': [system_1.system_id, system_2.system_id, system_3.system_id],
        }
        # get response
        response = self.client.post('/task/creator/', data_dict)
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare
        self.assertEqual(str(messages[0]), 'Task creator started')
        self.assertEqual(str(messages[1]), '9 tasks created for 3 systems.')
