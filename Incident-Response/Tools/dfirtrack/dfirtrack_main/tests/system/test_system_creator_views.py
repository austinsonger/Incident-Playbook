from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.test import TestCase
from django.utils import timezone
from dfirtrack_main.models import Analysisstatus, System, Systemstatus
import urllib.parse

class SystemCreatorViewTestCase(TestCase):
    """ system creator view tests """

    @classmethod
    def setUpTestData(cls):

        # create user
        test_user = User.objects.create_user(username='testuser_system_creator', password='Jbf5fZBhpg1aZsCW6L8r')

        # create objects
        systemstatus_1 = Systemstatus.objects.create(systemstatus_name = 'systemstatus_1')
        Systemstatus.objects.create(systemstatus_name = 'systemstatus_2')
        System.objects.create(
            system_name = 'system_creator_duplicate_system',
            systemstatus = systemstatus_1,
            system_modify_time = timezone.now(),
            system_created_by_user_id = test_user,
            system_modified_by_user_id = test_user,
        )
        System.objects.create(
            system_name = 'system_creator_duplicate_system_2',
            systemstatus = systemstatus_1,
            system_modify_time = timezone.now(),
            system_created_by_user_id = test_user,
            system_modified_by_user_id = test_user,
        )

    def test_system_creator_not_logged_in(self):
        """ test creator view """

        # create url
        destination = '/login/?next=' + urllib.parse.quote('/system/creator/', safe='')
        # get response
        response = self.client.get('/system/creator/', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)

    def test_system_creator_logged_in(self):
        """ test creator view """

        # login testuser
        self.client.login(username='testuser_system_creator', password='Jbf5fZBhpg1aZsCW6L8r')
        # get response
        response = self.client.get('/system/creator/')
        # compare
        self.assertEqual(response.status_code, 200)

    def test_system_creator_template(self):
        """ test creator view """

        # login testuser
        self.client.login(username='testuser_system_creator', password='Jbf5fZBhpg1aZsCW6L8r')
        # get response
        response = self.client.get('/system/creator/')
        # compare
        self.assertTemplateUsed(response, 'dfirtrack_main/system/system_creator.html')

    def test_system_creator_get_user_context(self):
        """ test creator view """

        # login testuser
        self.client.login(username='testuser_system_creator', password='Jbf5fZBhpg1aZsCW6L8r')
        # get response
        response = self.client.get('/system/creator/')
        # compare
        self.assertEqual(str(response.context['user']), 'testuser_system_creator')

    def test_system_creator_redirect(self):
        """ test creator view """

        # login testuser
        self.client.login(username='testuser_system_creator', password='Jbf5fZBhpg1aZsCW6L8r')
        # create url
        destination = urllib.parse.quote('/system/creator/', safe='/')
        # get response
        response = self.client.get('/system/creator', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=301, target_status_code=200)

    def test_system_creator_post_redirect(self):
        """ test creator view """

        # login testuser
        self.client.login(username='testuser_system_creator', password='Jbf5fZBhpg1aZsCW6L8r')
        # get objects
        systemstatus_2 = Systemstatus.objects.get(systemstatus_name = 'systemstatus_2')
        # create post data
        data_dict = {
            'systemlist': 'system_creator_redirect',
            'systemstatus': systemstatus_2.systemstatus_id,
        }
        # create url
        destination = '/system/'
        # get response
        response = self.client.post('/system/creator/', data_dict)
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)

    def test_system_creator_post_systems(self):
        """ test creator view """

        # login testuser
        self.client.login(username='testuser_system_creator', password='Jbf5fZBhpg1aZsCW6L8r')
        # create objects
        analysisstatus_1 = Analysisstatus.objects.create(analysisstatus_name = 'analysisstatus_1')
        systemstatus_2 = Systemstatus.objects.get(systemstatus_name = 'systemstatus_2')
        # create post data
        data_dict = {
            'systemlist': 'system_creator_system_1\nsystem_creator_system_2\nsystem_creator_system_3\n\nxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\nsystem_creator_duplicate_system',
            'analysisstatus': analysisstatus_1.analysisstatus_id,
            'systemstatus': systemstatus_2.systemstatus_id,
        }
        # get response
        self.client.post('/system/creator/', data_dict)
        # compare
        self.assertTrue(System.objects.filter(system_name='system_creator_system_1').exists())
        self.assertTrue(System.objects.filter(system_name='system_creator_system_2').exists())
        self.assertTrue(System.objects.filter(system_name='system_creator_system_3').exists())
        self.assertFalse(System.objects.filter(system_name='system_creator_system_4').exists())
        self.assertEqual(System.objects.get(system_name='system_creator_system_1').analysisstatus, analysisstatus_1)
        self.assertEqual(System.objects.get(system_name='system_creator_system_1').systemstatus, systemstatus_2)
        self.assertEqual(System.objects.filter(system_name='system_creator_duplicate_system').count(), 1)

    def test_system_creator_post_messages(self):
        """ test creator view """

        # login testuser
        self.client.login(username='testuser_system_creator', password='Jbf5fZBhpg1aZsCW6L8r')
        # create objects
        analysisstatus_1 = Analysisstatus.objects.create(analysisstatus_name = 'analysisstatus_1')
        systemstatus_2 = Systemstatus.objects.get(systemstatus_name = 'systemstatus_2')
        # create post data
        data_dict = {
            'systemlist': 'system_creator_message_1\nsystem_creator_message_2\nsystem_creator_message_3\n\nxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\nsystem_creator_duplicate_system',
            'analysisstatus': analysisstatus_1.analysisstatus_id,
            'systemstatus': systemstatus_2.systemstatus_id,
        }
        # get response
        response = self.client.post('/system/creator/', data_dict)
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare
        self.assertEqual(str(messages[0]), 'System creator started')
        self.assertEqual(str(messages[1]), '3 systems were created / modified.')
        self.assertEqual(str(messages[2]), "1 system was skipped. ['system_creator_duplicate_system']")
        self.assertEqual(str(messages[3]), '2 lines out of 6 lines were faulty (see log file for details).')

    def test_system_creator_post_other_messages(self):
        """ test creator view """

        # login testuser
        self.client.login(username='testuser_system_creator', password='Jbf5fZBhpg1aZsCW6L8r')
        # create objects
        analysisstatus_1 = Analysisstatus.objects.create(analysisstatus_name = 'analysisstatus_1')
        systemstatus_2 = Systemstatus.objects.get(systemstatus_name = 'systemstatus_2')
        # create post data
        data_dict = {
            'systemlist': 'system_creator_message_4\n\nsystem_creator_duplicate_system\nsystem_creator_duplicate_system_2',
            'analysisstatus': analysisstatus_1.analysisstatus_id,
            'systemstatus': systemstatus_2.systemstatus_id,
        }
        # get response
        response = self.client.post('/system/creator/', data_dict)
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare
        self.assertEqual(str(messages[1]), '1 system was created / modified.')
        self.assertEqual(str(messages[2]), "2 systems were skipped. ['system_creator_duplicate_system', 'system_creator_duplicate_system_2']")
        self.assertEqual(str(messages[3]), '1 line out of 4 lines was faulty (see log file for details).')
