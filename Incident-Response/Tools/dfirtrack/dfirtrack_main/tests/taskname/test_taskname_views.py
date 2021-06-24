from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.test import TestCase
from dfirtrack_main.models import Task, Taskname, Taskpriority, Taskstatus
import urllib.parse

class TasknameViewTestCase(TestCase):
    """ taskname view tests """

    @classmethod
    def setUpTestData(cls):

        # create user
        User.objects.create_user(username='testuser_taskname', password='7xajmDLqQh1hs8i5PAx7')

        # create object
        Taskname.objects.create(taskname_name='taskname_1')

        # create object
        Taskpriority.objects.create(taskpriority_name='prio_1')

        # create object
        Taskstatus.objects.create(taskstatus_name='taskstatus_1')

    def test_taskname_list_not_logged_in(self):
        """ test list view """

        # create url
        destination = '/login/?next=' + urllib.parse.quote('/taskname/', safe='')
        # get response
        response = self.client.get('/taskname/', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)

    def test_taskname_list_logged_in(self):
        """ test list view """

        # login testuser
        self.client.login(username='testuser_taskname', password='7xajmDLqQh1hs8i5PAx7')
        # get response
        response = self.client.get('/taskname/')
        # compare
        self.assertEqual(response.status_code, 200)

    def test_taskname_list_template(self):
        """ test list view """

        # login testuser
        self.client.login(username='testuser_taskname', password='7xajmDLqQh1hs8i5PAx7')
        # get response
        response = self.client.get('/taskname/')
        # compare
        self.assertTemplateUsed(response, 'dfirtrack_main/taskname/taskname_list.html')

    def test_taskname_list_get_user_context(self):
        """ test list view """

        # login testuser
        self.client.login(username='testuser_taskname', password='7xajmDLqQh1hs8i5PAx7')
        # get response
        response = self.client.get('/taskname/')
        # compare
        self.assertEqual(str(response.context['user']), 'testuser_taskname')

    def test_taskname_list_redirect(self):
        """ test list view """

        # login testuser
        self.client.login(username='testuser_taskname', password='7xajmDLqQh1hs8i5PAx7')
        # create url
        destination = urllib.parse.quote('/taskname/', safe='/')
        # get response
        response = self.client.get('/taskname', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=301, target_status_code=200)

    def test_taskname_detail_not_logged_in(self):
        """ test detail view """

        # get object
        taskname_1 = Taskname.objects.get(taskname_name='taskname_1')
        # create url
        destination = '/login/?next=' + urllib.parse.quote('/taskname/' + str(taskname_1.taskname_id) + '/', safe='')
        # get response
        response = self.client.get('/taskname/' + str(taskname_1.taskname_id) + '/', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)

    def test_taskname_detail_logged_in(self):
        """ test detail view """

        # get object
        taskname_1 = Taskname.objects.get(taskname_name='taskname_1')
        # login testuser
        self.client.login(username='testuser_taskname', password='7xajmDLqQh1hs8i5PAx7')
        # get response
        response = self.client.get('/taskname/' + str(taskname_1.taskname_id) + '/')
        # compare
        self.assertEqual(response.status_code, 200)

    def test_taskname_detail_template(self):
        """ test detail view """

        # get object
        taskname_1 = Taskname.objects.get(taskname_name='taskname_1')
        # login testuser
        self.client.login(username='testuser_taskname', password='7xajmDLqQh1hs8i5PAx7')
        # get response
        response = self.client.get('/taskname/' + str(taskname_1.taskname_id) + '/')
        # compare
        self.assertTemplateUsed(response, 'dfirtrack_main/taskname/taskname_detail.html')

    def test_taskname_detail_get_user_context(self):
        """ test detail view """

        # get object
        taskname_1 = Taskname.objects.get(taskname_name='taskname_1')
        # login testuser
        self.client.login(username='testuser_taskname', password='7xajmDLqQh1hs8i5PAx7')
        # get response
        response = self.client.get('/taskname/' + str(taskname_1.taskname_id) + '/')
        # compare
        self.assertEqual(str(response.context['user']), 'testuser_taskname')

    def test_taskname_detail_redirect(self):
        """ test detail view """

        # get object
        taskname_1 = Taskname.objects.get(taskname_name='taskname_1')
        # login testuser
        self.client.login(username='testuser_taskname', password='7xajmDLqQh1hs8i5PAx7')
        # create url
        destination = urllib.parse.quote('/taskname/' + str(taskname_1.taskname_id) + '/', safe='/')
        # get response
        response = self.client.get('/taskname/' + str(taskname_1.taskname_id), follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=301, target_status_code=200)

    def test_taskname_add_not_logged_in(self):
        """ test add view """

        # create url
        destination = '/login/?next=' + urllib.parse.quote('/taskname/add/', safe='')
        # get response
        response = self.client.get('/taskname/add/', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)

    def test_taskname_add_logged_in(self):
        """ test add view """

        # login testuser
        self.client.login(username='testuser_taskname', password='7xajmDLqQh1hs8i5PAx7')
        # get response
        response = self.client.get('/taskname/add/')
        # compare
        self.assertEqual(response.status_code, 200)

    def test_taskname_add_template(self):
        """ test add view """

        # login testuser
        self.client.login(username='testuser_taskname', password='7xajmDLqQh1hs8i5PAx7')
        # get response
        response = self.client.get('/taskname/add/')
        # compare
        self.assertTemplateUsed(response, 'dfirtrack_main/taskname/taskname_add.html')

    def test_taskname_add_get_user_context(self):
        """ test add view """

        # login testuser
        self.client.login(username='testuser_taskname', password='7xajmDLqQh1hs8i5PAx7')
        # get response
        response = self.client.get('/taskname/add/')
        # compare
        self.assertEqual(str(response.context['user']), 'testuser_taskname')

    def test_taskname_add_redirect(self):
        """ test add view """

        # login testuser
        self.client.login(username='testuser_taskname', password='7xajmDLqQh1hs8i5PAx7')
        # create url
        destination = urllib.parse.quote('/taskname/add/', safe='/')
        # get response
        response = self.client.get('/taskname/add', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=301, target_status_code=200)

    def test_taskname_add_post_redirect(self):
        """ test add view """

        # login testuser
        self.client.login(username='testuser_taskname', password='7xajmDLqQh1hs8i5PAx7')
        # create post data
        data_dict = {
            'taskname_name': 'taskname_add_post_test',
        }
        # get response
        response = self.client.post('/taskname/add/', data_dict)
        # get object
        taskname_id = Taskname.objects.get(taskname_name = 'taskname_add_post_test').taskname_id
        # create url
        destination = urllib.parse.quote('/taskname/' + str(taskname_id) + '/', safe='/')
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)

    def test_taskname_add_post_invalid_reload(self):
        """ test add view """

        # login testuser
        self.client.login(username='testuser_taskname', password='7xajmDLqQh1hs8i5PAx7')
        # create post data
        data_dict = {}
        # get response
        response = self.client.post('/taskname/add/', data_dict)
        # compare
        self.assertEqual(response.status_code, 200)

    def test_taskname_add_post_invalid_template(self):
        """ test add view """

        # login testuser
        self.client.login(username='testuser_taskname', password='7xajmDLqQh1hs8i5PAx7')
        # create post data
        data_dict = {}
        # get response
        response = self.client.post('/taskname/add/', data_dict)
        # compare
        self.assertTemplateUsed(response, 'dfirtrack_main/taskname/taskname_add.html')

    def test_taskname_edit_not_logged_in(self):
        """ test edit view """

        # get object
        taskname_1 = Taskname.objects.get(taskname_name='taskname_1')
        # create url
        destination = '/login/?next=' + urllib.parse.quote('/taskname/' + str(taskname_1.taskname_id) + '/edit/', safe='')
        # get response
        response = self.client.get('/taskname/' + str(taskname_1.taskname_id) + '/edit/', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)

    def test_taskname_edit_logged_in(self):
        """ test edit view """

        # get object
        taskname_1 = Taskname.objects.get(taskname_name='taskname_1')
        # login testuser
        self.client.login(username='testuser_taskname', password='7xajmDLqQh1hs8i5PAx7')
        # get response
        response = self.client.get('/taskname/' + str(taskname_1.taskname_id) + '/edit/')
        # compare
        self.assertEqual(response.status_code, 200)

    def test_taskname_edit_template(self):
        """ test edit view """

        # get object
        taskname_1 = Taskname.objects.get(taskname_name='taskname_1')
        # login testuser
        self.client.login(username='testuser_taskname', password='7xajmDLqQh1hs8i5PAx7')
        # get response
        response = self.client.get('/taskname/' + str(taskname_1.taskname_id) + '/edit/')
        # compare
        self.assertTemplateUsed(response, 'dfirtrack_main/taskname/taskname_edit.html')

    def test_taskname_edit_get_user_context(self):
        """ test edit view """

        # get object
        taskname_1 = Taskname.objects.get(taskname_name='taskname_1')
        # login testuser
        self.client.login(username='testuser_taskname', password='7xajmDLqQh1hs8i5PAx7')
        # get response
        response = self.client.get('/taskname/' + str(taskname_1.taskname_id) + '/edit/')
        # compare
        self.assertEqual(str(response.context['user']), 'testuser_taskname')

    def test_taskname_edit_redirect(self):
        """ test edit view """

        # get object
        taskname_1 = Taskname.objects.get(taskname_name='taskname_1')
        # login testuser
        self.client.login(username='testuser_taskname', password='7xajmDLqQh1hs8i5PAx7')
        # create url
        destination = urllib.parse.quote('/taskname/' + str(taskname_1.taskname_id) + '/edit/', safe='/')
        # get response
        response = self.client.get('/taskname/' + str(taskname_1.taskname_id) + '/edit', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=301, target_status_code=200)

    def test_taskname_edit_post_redirect(self):
        """ test edit view """

        # login testuser
        self.client.login(username='testuser_taskname', password='7xajmDLqQh1hs8i5PAx7')
        # create object
        taskname_1 = Taskname.objects.create(taskname_name='taskname_edit_post_test_1')
        # create post data
        data_dict = {
            'taskname_name': 'taskname_edit_post_test_2',
        }
        # get response
        response = self.client.post('/taskname/' + str(taskname_1.taskname_id) + '/edit/', data_dict)
        # get object
        taskname_2 = Taskname.objects.get(taskname_name='taskname_edit_post_test_2')
        # create url
        destination = urllib.parse.quote('/taskname/' + str(taskname_2.taskname_id) + '/', safe='/')
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)

    def test_taskname_edit_post_invalid_reload(self):
        """ test edit view """

        # login testuser
        self.client.login(username='testuser_taskname', password='7xajmDLqQh1hs8i5PAx7')
        # get object
        taskname_id = Taskname.objects.get(taskname_name='taskname_1').taskname_id
        # create post data
        data_dict = {}
        # get response
        response = self.client.post('/taskname/' + str(taskname_id) + '/edit/', data_dict)
        # compare
        self.assertEqual(response.status_code, 200)

    def test_taskname_edit_post_invalid_template(self):
        """ test edit view """

        # login testuser
        self.client.login(username='testuser_taskname', password='7xajmDLqQh1hs8i5PAx7')
        # get object
        taskname_id = Taskname.objects.get(taskname_name='taskname_1').taskname_id
        # create post data
        data_dict = {}
        # get response
        response = self.client.post('/taskname/' + str(taskname_id) + '/edit/', data_dict)
        # compare
        self.assertTemplateUsed(response, 'dfirtrack_main/taskname/taskname_edit.html')

    def test_taskname_close_not_logged_in(self):
        """ test close view """

        # get object
        taskname_1 = Taskname.objects.get(taskname_name='taskname_1')
        # create url
        destination = '/login/?next=' + urllib.parse.quote('/taskname/' + str(taskname_1.taskname_id) + '/close/', safe='')
        # get response
        response = self.client.get('/taskname/' + str(taskname_1.taskname_id) + '/close/', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)

    def test_taskname_close_logged_in(self):
        """ test close view """

        # get object
        taskname_1 = Taskname.objects.get(taskname_name='taskname_1')
        # login testuser
        self.client.login(username='testuser_taskname', password='7xajmDLqQh1hs8i5PAx7')
        # get response
        response = self.client.get('/taskname/' + str(taskname_1.taskname_id) + '/close/')
        # compare
        self.assertEqual(response.status_code, 200)

    def test_taskname_close_template(self):
        """ test close view """

        # get object
        taskname_1 = Taskname.objects.get(taskname_name='taskname_1')
        # login testuser
        self.client.login(username='testuser_taskname', password='7xajmDLqQh1hs8i5PAx7')
        # get response
        response = self.client.get('/taskname/' + str(taskname_1.taskname_id) + '/close/')
        # compare
        self.assertTemplateUsed(response, 'dfirtrack_main/taskname/taskname_close.html')

    def test_taskname_close_get_user_context(self):
        """ test close view """

        # get object
        taskname_1 = Taskname.objects.get(taskname_name='taskname_1')
        # login testuser
        self.client.login(username='testuser_taskname', password='7xajmDLqQh1hs8i5PAx7')
        # get response
        response = self.client.get('/taskname/' + str(taskname_1.taskname_id) + '/close/')
        # compare
        self.assertEqual(str(response.context['user']), 'testuser_taskname')

    def test_taskname_close_redirect(self):
        """ test close view """

        # get object
        taskname_1 = Taskname.objects.get(taskname_name='taskname_1')
        # login testuser
        self.client.login(username='testuser_taskname', password='7xajmDLqQh1hs8i5PAx7')
        # create url
        destination = urllib.parse.quote('/taskname/' + str(taskname_1.taskname_id) + '/close/', safe='/')
        # get response
        response = self.client.get('/taskname/' + str(taskname_1.taskname_id) + '/close', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=301, target_status_code=200)

    def test_taskname_close_post_tasks_to_close(self):
        """ test close view """

        # login testuser
        self.client.login(username='testuser_taskname', password='7xajmDLqQh1hs8i5PAx7')
        # get user
        test_user = User.objects.get(username='testuser_taskname')
        # create object
        taskname_close = Taskname.objects.create(taskname_name='test_taskname_close')
        # get object
        taskpriority_1 = Taskpriority.objects.get(taskpriority_name='prio_1')
        # get object
        taskstatus_1 = Taskstatus.objects.get(taskstatus_name='taskstatus_1')
        # create objects
        task_close_1 = Task.objects.create(
            taskname = taskname_close,
            taskpriority = taskpriority_1,
            taskstatus = taskstatus_1,
            task_created_by_user_id = test_user,
            task_modified_by_user_id = test_user,
        )
        task_close_2 = Task.objects.create(
            taskname = taskname_close,
            taskpriority = taskpriority_1,
            taskstatus = taskstatus_1,
            task_created_by_user_id = test_user,
            task_modified_by_user_id = test_user,
        )
        # get object (does not work the usual way because form with available choices is build before model instance is created during the test)
        taskstatus_done = Taskstatus.objects.get(taskstatus_name='30_done')
        # get response
        response = self.client.post('/taskname/' + str(taskname_close.taskname_id) + '/close/')
        # refresh objects
        task_close_1.refresh_from_db()
        task_close_2.refresh_from_db()
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dfirtrack_main/taskname/taskname_close.html')
        self.assertEqual(task_close_1.taskstatus, taskstatus_done)
        self.assertEqual(task_close_2.taskstatus, taskstatus_done)
        self.assertEqual(str(messages[-1]), 'Closed task IDs: [' + str(task_close_1.task_id) + ', ' + str(task_close_2.task_id) + ']')

    def test_taskname_close_post_nothing_to_close(self):
        """ test close view """

        # login testuser
        self.client.login(username='testuser_taskname', password='7xajmDLqQh1hs8i5PAx7')
        # create object
        taskname_void = Taskname.objects.create(taskname_name='test_taskname_void')
        # get response
        response = self.client.post('/taskname/' + str(taskname_void.taskname_id) + '/close/')
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dfirtrack_main/taskname/taskname_close.html')
        self.assertEqual(str(messages[-1]), 'No tasks to close.')
