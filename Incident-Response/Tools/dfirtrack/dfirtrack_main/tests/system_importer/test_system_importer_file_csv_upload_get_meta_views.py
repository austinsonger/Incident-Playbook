from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.test import TestCase
from dfirtrack_main.tests.system_importer.config_functions import set_csv_skip_existing_system, set_csv_import_username
import urllib.parse


class SystemImporterFileCsvUploadGetMetaViewTestCase(TestCase):
    """ system importer file CSV view tests """

    @classmethod
    def setUpTestData(cls):
        """ one-time setup """

        # create user
        test_user = User.objects.create_user(username='testuser_system_importer_file_csv_upload_get_meta', password='39gE1C0nA1hmlcoxZjAd')

        # change config
        set_csv_import_username(test_user)

    def test_system_importer_file_csv_upload_get_meta_not_logged_in(self):
        """ test importer view """

        # create url
        destination = '/login/?next=' + urllib.parse.quote('/system/importer/file/csv/upload/', safe='')
        # get response
        response = self.client.get('/system/importer/file/csv/upload/', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)

    def test_system_importer_file_csv_upload_get_meta_logged_in(self):
        """ test importer view """

        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_upload_get_meta', password='39gE1C0nA1hmlcoxZjAd')
        # get response
        response = self.client.get('/system/importer/file/csv/upload/')
        # compare
        self.assertEqual(response.status_code, 200)

    def test_system_importer_file_csv_upload_get_meta_template(self):
        """ test importer view """

        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_upload_get_meta', password='39gE1C0nA1hmlcoxZjAd')
        # get response
        response = self.client.get('/system/importer/file/csv/upload/')
        # compare
        self.assertTemplateUsed(response, 'dfirtrack_main/system/system_importer_file_csv.html')

    def test_system_importer_file_csv_upload_get_meta_get_user_context(self):
        """ test importer view """

        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_upload_get_meta', password='39gE1C0nA1hmlcoxZjAd')
        # get response
        response = self.client.get('/system/importer/file/csv/upload/')
        # compare
        self.assertEqual(str(response.context['user']), 'testuser_system_importer_file_csv_upload_get_meta')

    def test_system_importer_file_csv_upload_get_meta_redirect(self):
        """ test importer view """

        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_upload_get_meta', password='39gE1C0nA1hmlcoxZjAd')
        # create url
        destination = urllib.parse.quote('/system/importer/file/csv/upload/', safe='/')
        # get response
        response = self.client.get('/system/importer/file/csv/upload', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=301, target_status_code=200)

    def test_system_importer_file_csv_upload_get_meta_skip_warning(self):
        """ test importer view """

        # change config
        set_csv_skip_existing_system(False)

        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_upload_get_meta', password='39gE1C0nA1hmlcoxZjAd')
        # get response
        response = self.client.get('/system/importer/file/csv/upload/', follow=True)
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare
        self.assertEqual(response.status_code, 200)
        self.assertEqual(messages[0].message, 'WARNING: Existing systems will be updated!')
        self.assertEqual(messages[0].level_tag, 'warning')
