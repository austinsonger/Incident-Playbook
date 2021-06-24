from datetime import datetime
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.test import TestCase
from django.utils import timezone
from dfirtrack_artifacts.models import Artifact, Artifactstatus, Artifacttype
from dfirtrack_config.models import Statushistory, StatushistoryEntry
from dfirtrack_config.views.statushistory import statushistory_save_cron
from dfirtrack_main.models import System, Systemstatus, Task, Taskname, Taskpriority, Taskstatus
from mock import patch
import urllib.parse

class StatushistoryViewTestCase(TestCase):
    """ statushistory view tests """

    @classmethod
    def setUpTestData(cls):

        # create user
        User.objects.create_user(username='testuser_statushistory', password='SXHemnLqF6chIcem5ABs')

        # create user
        test_user = User.objects.create_user(username='testuser_generic_views', password='D9lPsoHFXeCNKEzM3IgE')

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

    def test_statushistory_save_view_not_logged_in(self):
        """ test view """

        # create url
        destination = '/login/?next=' + urllib.parse.quote('/config/statushistory/save/', safe='')
        # get response
        response = self.client.get('/config/statushistory/save/', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)

    def test_statushistory_save_view_logged_in(self):
        """ test view """

        # login testuser
        self.client.login(username='testuser_statushistory', password='SXHemnLqF6chIcem5ABs')
        # get response
        response = self.client.get('/config/statushistory/save/')
        # create url
        destination = '/config/status/'
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)

    def test_statushistory_save_view_redirect(self):
        """ test view """

        # login testuser
        self.client.login(username='testuser_statushistory', password='SXHemnLqF6chIcem5ABs')
        # create url
        destination = '/config/status/'
        # get response
        response = self.client.get('/config/statushistory/save', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=301, target_status_code=200)

    def test_statushistory_save_view_message(self):
        """ test view """

        # login testuser
        self.client.login(username='testuser_statushistory', password='SXHemnLqF6chIcem5ABs')
        # get response
        response = self.client.get('/config/statushistory/save/')
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare
        self.assertEqual(str(messages[-1]), 'Statushistory saved')

    def test_statushistory_save_view_complete(self):
        """ test view """

        # mock timezone.now()
        t_1 = datetime(2020, 5, 4, 3, 2, 1, tzinfo=timezone.utc)
        with patch.object(timezone, 'now', return_value=t_1):

            # login testuser
            self.client.login(username='testuser_statushistory', password='SXHemnLqF6chIcem5ABs')
            # get response
            self.client.get('/config/statushistory/save/')

        # get statushistory object
        statushistory = Statushistory.objects.get(statushistory_time=t_1)

        # get number entries
        artifacts_number = StatushistoryEntry.objects.get(
            statushistory = statushistory,
            statushistoryentry_model_name = 'artifacts_number',
        )
        systems_number = StatushistoryEntry.objects.get(
            statushistory = statushistory,
            statushistoryentry_model_name = 'systems_number',
        )
        tasks_number = StatushistoryEntry.objects.get(
            statushistory = statushistory,
            statushistoryentry_model_name = 'tasks_number',
        )
        # get artifactpriority entries (separately because it was assigned with default value)
        artifactpriority_10_low = StatushistoryEntry.objects.get(
            statushistory = statushistory,
            statushistoryentry_model_name = 'artifactpriority',
            statushistoryentry_model_key = '10_low',
        )
        artifactpriority_20_medium = StatushistoryEntry.objects.get(
            statushistory = statushistory,
            statushistoryentry_model_name = 'artifactpriority',
            statushistoryentry_model_key = '20_medium',
        )
        artifactpriority_30_high = StatushistoryEntry.objects.get(
            statushistory = statushistory,
            statushistoryentry_model_name = 'artifactpriority',
            statushistoryentry_model_key = '30_high',
        )
        # get all other entries as queryset
        analysisstatus_all = StatushistoryEntry.objects.filter(
            statushistory = statushistory,
            statushistoryentry_model_name = 'analysisstatus',
        )
        artifactstatus_all = StatushistoryEntry.objects.filter(
            statushistory = statushistory,
            statushistoryentry_model_name = 'artifactstatus',
        )
        systemstatus_all = StatushistoryEntry.objects.filter(
            statushistory = statushistory,
            statushistoryentry_model_name = 'systemstatus',
        )
        taskpriority_all = StatushistoryEntry.objects.filter(
            statushistory = statushistory,
            statushistoryentry_model_name = 'taskpriority',
        )
        taskstatus_all = StatushistoryEntry.objects.filter(
            statushistory = statushistory,
            statushistoryentry_model_name = 'taskstatus',
        )
        # compare numbers
        self.assertEqual(artifacts_number.statushistoryentry_model_value, 2)
        self.assertEqual(systems_number.statushistoryentry_model_value, 3)
        self.assertEqual(tasks_number.statushistoryentry_model_value, 1)
        # compare artifactpriority
        self.assertEqual(artifactpriority_10_low.statushistoryentry_model_value, 0)
        self.assertEqual(artifactpriority_20_medium.statushistoryentry_model_value, 2)
        self.assertEqual(artifactpriority_30_high.statushistoryentry_model_value, 0)
        # compare querysets
        for analysisstatus in analysisstatus_all:
            if analysisstatus.statushistoryentry_model_key == 'analysisstatus_1':
                self.assertEqual(analysisstatus.statushistoryentry_model_value, 3)
            else:
                self.assertEqual(analysisstatus.statushistoryentry_model_value, 0)
        for artifactstatus in artifactstatus_all:
            if artifactstatus.statushistoryentry_model_key == 'artifactstatus_1':
                self.assertEqual(artifactstatus.statushistoryentry_model_value, 2)
            else:
                self.assertEqual(artifactstatus.statushistoryentry_model_value, 0)
        for systemstatus in systemstatus_all:
            if systemstatus.statushistoryentry_model_key == 'systemstatus_1':
                self.assertEqual(systemstatus.statushistoryentry_model_value, 3)
            else:
                self.assertEqual(systemstatus.statushistoryentry_model_value, 0)
        for taskpriority in taskpriority_all:
            if taskpriority.statushistoryentry_model_key == 'prio_1':
                self.assertEqual(taskpriority.statushistoryentry_model_value, 1)
            else:
                self.assertEqual(taskpriority.statushistoryentry_model_value, 0)
        for taskstatus in taskstatus_all:
            if taskstatus.statushistoryentry_model_key == 'taskstatus_1':
                self.assertEqual(taskstatus.statushistoryentry_model_value, 1)
            else:
                self.assertEqual(taskstatus.statushistoryentry_model_value, 0)

    def test_statushistory_save_cron_view_complete(self):

        # mock timezone.now()
        t_2 = datetime(2020, 1, 2, 3, 4, 5, tzinfo=timezone.utc)
        with patch.object(timezone, 'now', return_value=t_2):

            # save statushistory without GET
            statushistory_save_cron()

        # get statushistory object
        statushistory = Statushistory.objects.get(statushistory_time=t_2)

        # get number entries
        artifacts_number = StatushistoryEntry.objects.get(
            statushistory = statushistory,
            statushistoryentry_model_name = 'artifacts_number',
        )
        systems_number = StatushistoryEntry.objects.get(
            statushistory = statushistory,
            statushistoryentry_model_name = 'systems_number',
        )
        tasks_number = StatushistoryEntry.objects.get(
            statushistory = statushistory,
            statushistoryentry_model_name = 'tasks_number',
        )
        # get artifactpriority entries (separately because it was assigned with default value)
        artifactpriority_10_low = StatushistoryEntry.objects.get(
            statushistory = statushistory,
            statushistoryentry_model_name = 'artifactpriority',
            statushistoryentry_model_key = '10_low',
        )
        artifactpriority_20_medium = StatushistoryEntry.objects.get(
            statushistory = statushistory,
            statushistoryentry_model_name = 'artifactpriority',
            statushistoryentry_model_key = '20_medium',
        )
        artifactpriority_30_high = StatushistoryEntry.objects.get(
            statushistory = statushistory,
            statushistoryentry_model_name = 'artifactpriority',
            statushistoryentry_model_key = '30_high',
        )
        # get all other entries as queryset
        analysisstatus_all = StatushistoryEntry.objects.filter(
            statushistory = statushistory,
            statushistoryentry_model_name = 'analysisstatus',
        )
        artifactstatus_all = StatushistoryEntry.objects.filter(
            statushistory = statushistory,
            statushistoryentry_model_name = 'artifactstatus',
        )
        systemstatus_all = StatushistoryEntry.objects.filter(
            statushistory = statushistory,
            statushistoryentry_model_name = 'systemstatus',
        )
        taskpriority_all = StatushistoryEntry.objects.filter(
            statushistory = statushistory,
            statushistoryentry_model_name = 'taskpriority',
        )
        taskstatus_all = StatushistoryEntry.objects.filter(
            statushistory = statushistory,
            statushistoryentry_model_name = 'taskstatus',
        )
        # compare numbers
        self.assertEqual(artifacts_number.statushistoryentry_model_value, 2)
        self.assertEqual(systems_number.statushistoryentry_model_value, 3)
        self.assertEqual(tasks_number.statushistoryentry_model_value, 1)
        # compare artifactpriority
        self.assertEqual(artifactpriority_10_low.statushistoryentry_model_value, 0)
        self.assertEqual(artifactpriority_20_medium.statushistoryentry_model_value, 2)
        self.assertEqual(artifactpriority_30_high.statushistoryentry_model_value, 0)
        # compare querysets
        for analysisstatus in analysisstatus_all:
            if analysisstatus.statushistoryentry_model_key == 'analysisstatus_1':
                self.assertEqual(analysisstatus.statushistoryentry_model_value, 3)
            else:
                self.assertEqual(analysisstatus.statushistoryentry_model_value, 0)
        for artifactstatus in artifactstatus_all:
            if artifactstatus.statushistoryentry_model_key == 'artifactstatus_1':
                self.assertEqual(artifactstatus.statushistoryentry_model_value, 2)
            else:
                self.assertEqual(artifactstatus.statushistoryentry_model_value, 0)
        for systemstatus in systemstatus_all:
            if systemstatus.statushistoryentry_model_key == 'systemstatus_1':
                self.assertEqual(systemstatus.statushistoryentry_model_value, 3)
            else:
                self.assertEqual(systemstatus.statushistoryentry_model_value, 0)
        for taskpriority in taskpriority_all:
            if taskpriority.statushistoryentry_model_key == 'prio_1':
                self.assertEqual(taskpriority.statushistoryentry_model_value, 1)
            else:
                self.assertEqual(taskpriority.statushistoryentry_model_value, 0)
        for taskstatus in taskstatus_all:
            if taskstatus.statushistoryentry_model_key == 'taskstatus_1':
                self.assertEqual(taskstatus.statushistoryentry_model_value, 1)
            else:
                self.assertEqual(taskstatus.statushistoryentry_model_value, 0)
