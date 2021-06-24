from django.contrib.auth.models import User
from django.test import TestCase
from dfirtrack_main.tests.system_importer.config_functions import set_csv_import_username
import urllib.parse


class SystemImporterFileCsvInstantMetaViewTestCase(TestCase):
    """ system importer file CSV view tests """

    @classmethod
    def setUpTestData(cls):
        """ one-time setup """

        # create user
        test_user = User.objects.create_user(username='testuser_system_importer_file_csv_instant_meta', password='s996KrAi8M5Hev62lP7q')

        # change config
        set_csv_import_username(test_user)

    def test_system_importer_file_csv_instant_meta_not_logged_in(self):
        """ test importer view """

        # create url
        destination = '/login/?next=' + urllib.parse.quote('/system/importer/file/csv/instant/', safe='')
        # get response
        response = self.client.get('/system/importer/file/csv/instant/', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)

    def test_system_importer_file_csv_instant_meta_logged_in(self):
        """ test importer view """

        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_instant_meta', password='s996KrAi8M5Hev62lP7q')
        # create url
        destination = urllib.parse.quote('/system/', safe='/')
        # get response
        response = self.client.get('/system/importer/file/csv/instant/')
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)

    def test_system_importer_file_csv_instant_meta_redirect(self):
        """ test importer view """

        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_instant_meta', password='s996KrAi8M5Hev62lP7q')
        # create url
        destination = urllib.parse.quote('/system/', safe='/')
        # get response
        response = self.client.get('/system/importer/file/csv/instant', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=301, target_status_code=200)
