from datetime import datetime
from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone
from dfirtrack_artifacts.models import Artifact, Artifactpriority, Artifactstatus, Artifacttype
from dfirtrack_config.models import Statushistory
from dfirtrack_main.models import Analysisstatus, System, Systemstatus, Task, Taskname, Taskpriority, Taskstatus
from mock import patch
import urllib.parse

class StatusViewTestCase(TestCase):
    """ status view tests """

    @classmethod
    def setUpTestData(cls):

        # create user
        test_user = User.objects.create_user(username='testuser_status', password='D9lPsoHFXeCNKEzM3IgE')

        # create object
        artifactstatus_1 = Artifactstatus.objects.create(artifactstatus_name='artifactstatus_1')

        # create object
        artifacttype_1 = Artifacttype.objects.create(artifacttype_name='artifacttype_1')

        # create object
        systemstatus_1 = Systemstatus.objects.create(systemstatus_name='systemstatus_1')

        # create object
        taskname_1 = Taskname.objects.create(taskname_name='taskname_1')

        # create object
        taskpriority_1 = Taskpriority.objects.create(taskpriority_name='prio_1')

        # create object
        taskstatus_1 = Taskstatus.objects.create(taskstatus_name='taskstatus_1')

        # create object
        system_1 = System.objects.create(
            system_name = 'system_1',
            systemstatus = systemstatus_1,
            system_modify_time = timezone.now(),
            system_created_by_user_id = test_user,
            system_modified_by_user_id = test_user,
        )
        System.objects.create(
            system_name = 'system_2',
            systemstatus = systemstatus_1,
            system_modify_time = timezone.now(),
            system_created_by_user_id = test_user,
            system_modified_by_user_id = test_user,
        )
        System.objects.create(
            system_name = 'system_3',
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
            task_modify_time = timezone.now(),
            task_created_by_user_id = test_user,
            task_modified_by_user_id = test_user,
        )

        # create object
        Artifact.objects.create(
            artifact_name = 'artifact_1',
            artifactstatus = artifactstatus_1,
            artifacttype = artifacttype_1,
            system = system_1,
            artifact_created_by_user_id = test_user,
            artifact_modified_by_user_id = test_user,
        )
        Artifact.objects.create(
            artifact_name = 'artifact_2',
            artifactstatus = artifactstatus_1,
            artifacttype = artifacttype_1,
            system = system_1,
            artifact_created_by_user_id = test_user,
            artifact_modified_by_user_id = test_user,
        )

        # mock timezone.now()
        t_1 = datetime(2020, 11, 22, 11, 22, 33, tzinfo=timezone.utc)
        with patch.object(timezone, 'now', return_value=t_1):

            # create empty object (for simple testing get request for empty detail view this should be sufficient)
            Statushistory.objects.create()

    def test_status_view_not_logged_in(self):
        """ test status view """

        # create url
        destination = '/login/?next=' + urllib.parse.quote('/config/status/', safe='')
        # get response
        response = self.client.get('/config/status/', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)

    def test_status_view_logged_in(self):
        """ test status view """

        # login testuser
        self.client.login(username='testuser_status', password='D9lPsoHFXeCNKEzM3IgE')
        # get response
        response = self.client.get('/config/status/')
        # compare
        self.assertEqual(response.status_code, 200)

    def test_status_view_template(self):
        """ test status view """

        # login testuser
        self.client.login(username='testuser_status', password='D9lPsoHFXeCNKEzM3IgE')
        # get response
        response = self.client.get('/config/status/')
        # compare
        self.assertTemplateUsed(response, 'dfirtrack_config/status/status.html')

    def test_status_view_get_user_context(self):
        """ test status view """

        # login testuser
        self.client.login(username='testuser_status', password='D9lPsoHFXeCNKEzM3IgE')
        # get response
        response = self.client.get('/config/status/')
        # compare
        self.assertEqual(str(response.context['user']), 'testuser_status')

    def test_status_view_redirect(self):
        """ test status view """

        # login testuser
        self.client.login(username='testuser_status', password='D9lPsoHFXeCNKEzM3IgE')
        # create url
        destination = urllib.parse.quote('/config/status/', safe='/')
        # get response
        response = self.client.get('/config/status', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=301, target_status_code=200)

    def test_status_view_get_object_context(self):
        """ test status view """

        # login testuser
        self.client.login(username='testuser_status', password='D9lPsoHFXeCNKEzM3IgE')
        # get response
        response = self.client.get('/config/status/')
        # get querysets
        analysisstatus_all = Analysisstatus.objects.all().order_by('analysisstatus_name')
        artifactpriority_all = Artifactpriority.objects.all().order_by('artifactpriority_name')
        artifactstatus_all = Artifactstatus.objects.all().order_by('artifactstatus_name')
        systemstatus_all = Systemstatus.objects.all().order_by('systemstatus_name')
        taskstatus_all = Taskstatus.objects.all().order_by('taskstatus_name')
        taskpriority_all = Taskpriority.objects.all().order_by('taskpriority_name')
        # compare
        self.assertEqual(response.context['artifacts_number'], 2)
        self.assertEqual(response.context['systems_number'], 3)
        self.assertEqual(response.context['tasks_number'], 1)
        self.assertEqual(type(response.context['analysisstatus_all']), type(analysisstatus_all))
        self.assertEqual(type(response.context['artifactpriority_all']), type(artifactpriority_all))
        self.assertEqual(type(response.context['artifactstatus_all']), type(artifactstatus_all))
        self.assertEqual(type(response.context['systemstatus_all']), type(systemstatus_all))
        self.assertEqual(type(response.context['taskpriority_all']), type(taskpriority_all))
        self.assertEqual(type(response.context['taskstatus_all']), type(taskstatus_all))

    def test_status_view_get_statushistory_entry_numbers_context(self):
        """ test status view """

        # login testuser
        self.client.login(username='testuser_status', password='D9lPsoHFXeCNKEzM3IgE')
        # get response
        response = self.client.get('/config/status/')
        # compare
        self.assertEqual(type(response.context['statushistory_all']), type(reversed(Statushistory.objects.all())))
        # TODO: test number of queryset elements in context element 'statushistory_all' according to 'statushistory_last_entrys' in MainConfigModel
        # TODO: number also depends on available statushistory elements
        # TODO: find a way to count reversed queryset
        #self.assertEqual(response.context['statushistory_all'].count(), 2)

    def test_status_detail_view_not_logged_in(self):
        """ test status view """

        # get time
        t_1 = datetime(2020, 11, 22, 11, 22, 33, tzinfo=timezone.utc)
        # get object
        statushistory_id = Statushistory.objects.get(statushistory_time=t_1).statushistory_id
        # create url
        destination = '/login/?next=' + urllib.parse.quote('/config/status/' + str(statushistory_id) + '/', safe='')
        # get response
        response = self.client.get('/config/status/' + str(statushistory_id) + '/', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)

    def test_status_detail_view_logged_in(self):
        """ test status view """

        # login testuser
        self.client.login(username='testuser_status', password='D9lPsoHFXeCNKEzM3IgE')
        # get time
        t_1 = datetime(2020, 11, 22, 11, 22, 33, tzinfo=timezone.utc)
        # get object
        statushistory_id = Statushistory.objects.get(statushistory_time=t_1).statushistory_id
        # get response
        response = self.client.get('/config/status/' + str(statushistory_id) + '/')
        # compare
        self.assertEqual(response.status_code, 200)

    def test_status_detail_view_template(self):
        """ test status view """

        # login testuser
        self.client.login(username='testuser_status', password='D9lPsoHFXeCNKEzM3IgE')
        # get time
        t_1 = datetime(2020, 11, 22, 11, 22, 33, tzinfo=timezone.utc)
        # get object
        statushistory_id = Statushistory.objects.get(statushistory_time=t_1).statushistory_id
        # get response
        response = self.client.get('/config/status/' + str(statushistory_id) + '/')
        # compare
        self.assertTemplateUsed(response, 'dfirtrack_config/status/status_detail.html')

    def test_status_detail_view_get_user_context(self):
        """ test status view """

        # login testuser
        self.client.login(username='testuser_status', password='D9lPsoHFXeCNKEzM3IgE')
        # get time
        t_1 = datetime(2020, 11, 22, 11, 22, 33, tzinfo=timezone.utc)
        # get object
        statushistory_id = Statushistory.objects.get(statushistory_time=t_1).statushistory_id
        # get response
        response = self.client.get('/config/status/' + str(statushistory_id) + '/')
        # compare
        self.assertEqual(str(response.context['user']), 'testuser_status')

    def test_status_detail_view_redirect(self):
        """ test status view """

        # login testuser
        self.client.login(username='testuser_status', password='D9lPsoHFXeCNKEzM3IgE')
        # get time
        t_1 = datetime(2020, 11, 22, 11, 22, 33, tzinfo=timezone.utc)
        # get object
        statushistory_id = Statushistory.objects.get(statushistory_time=t_1).statushistory_id
        # create url
        destination = urllib.parse.quote('/config/status/' + str(statushistory_id) + '/', safe='/')
        # get response
        response = self.client.get('/config/status/' + str(statushistory_id), follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=301, target_status_code=200)
