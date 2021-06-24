from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.test import TestCase
from dfirtrack_main.importer.file.csv import system_cron
from dfirtrack_main.tests.system_importer.config_functions import set_csv_import_username
import urllib.parse


class SystemImporterFileCsvCheckConfigCronUserViewTestCase(TestCase):
    """ system importer file CSV view tests """

    @classmethod
    def setUpTestData(cls):
        """ one-time setup """

        # create users
        User.objects.create_user(username='testuser_system_importer_file_csv_check_config_cron_user', password='gRknQm6WAhvUc8uzYhbe')
        User.objects.create_user(username='message_user', password='HmiOhvi5RNzrM8UAjy7v')

        # change config
        set_csv_import_username(None)

    def test_system_importer_file_csv_check_config_cron_user_create_cron_no_import_user(self):
        """ test importer view """

        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_check_config_cron_user', password='gRknQm6WAhvUc8uzYhbe')
        # create url
        destination = urllib.parse.quote('/system/', safe='/')
        # get response
        response = self.client.get('/system/importer/file/csv/cron/', follow=True)
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)
        self.assertEqual(messages[0].message, 'No user for import defined. Check config!')
        self.assertEqual(messages[0].level_tag, 'error')

    def test_system_importer_file_csv_check_config_cron_user_cron_no_import_user(self):
        """ test importer view """

        # execute cron job / scheduled task
        system_cron()
        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_check_config_cron_user', password='gRknQm6WAhvUc8uzYhbe')
        # get response
        response = self.client.get('/system/')
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare
        self.assertEqual(str(response.context['user']), 'testuser_system_importer_file_csv_check_config_cron_user')
        self.assertEqual(messages[0].message, '[Scheduled task CSV system importer] No user for import defined. Check config!')
        self.assertEqual(messages[0].level_tag, 'error')
        # switch user context
        self.client.logout()
        self.client.login(username='message_user', password='HmiOhvi5RNzrM8UAjy7v')
        # get response
        response = self.client.get('/system/')
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare
        self.assertEqual(str(response.context['user']), 'message_user')
        self.assertEqual(messages[0].message, '[Scheduled task CSV system importer] No user for import defined. Check config!')
        self.assertEqual(messages[0].level_tag, 'error')
