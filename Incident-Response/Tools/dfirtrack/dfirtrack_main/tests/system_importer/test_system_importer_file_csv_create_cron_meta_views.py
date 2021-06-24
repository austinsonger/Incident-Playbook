from django.contrib.auth.models import User
from django.test import TestCase
from dfirtrack.settings import BASE_DIR
from dfirtrack_config.models import SystemImporterFileCsvConfigModel
from dfirtrack_main.tests.system_importer.config_functions import set_csv_import_filename, set_csv_import_path
import os
import urllib.parse


class SystemImporterFileCsvCreateCronMetaViewTestCase(TestCase):
    """ system importer file CSV view tests """

    @classmethod
    def setUpTestData(cls):
        """ one-time setup """

        # create user
        test_user = User.objects.create_user(
            username = 'testuser_system_importer_file_csv_create_cron_meta',
            is_staff = True,
            is_superuser = True,
            password = '4Ka6NQdzpkuUIWqfqRE6',
        )

        # change config
        set_csv_import_path(os.path.join(BASE_DIR, 'dfirtrack_main/tests/system_importer/system_importer_file_csv_files/'))
        # change config
        set_csv_import_filename('system_importer_file_csv_testfile_01_minimal_double_quotation.csv')

        system_importer_file_csv_config_model = SystemImporterFileCsvConfigModel.objects.get(system_importer_file_csv_config_name='SystemImporterFileCsvConfig')
        system_importer_file_csv_config_model.csv_import_username = test_user
        system_importer_file_csv_config_model.save()

    def test_system_importer_file_csv_create_cron_meta_not_logged_in(self):
        """ test importer view """

        # create url
        destination = '/login/?next=' + urllib.parse.quote('/system/importer/file/csv/cron/', safe='')
        # get response
        response = self.client.get('/system/importer/file/csv/cron/', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)

    def test_system_importer_file_csv_create_cron_meta_logged_in(self):
        """ test importer view """

        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_create_cron_meta', password='4Ka6NQdzpkuUIWqfqRE6')
        # create url (test seem to switch GET parameters)
        #destination = urllib.parse.quote('/admin/django_q/schedule/add/?name=system_importer_file_csv&func=dfirtrack_main.importer.file.csv.system_cron', safe='/?=&')
        destination = urllib.parse.quote('/admin/django_q/schedule/add/?func=dfirtrack_main.importer.file.csv.system_cron&name=system_importer_file_csv', safe='/?=&')
        # get response
        response = self.client.get('/system/importer/file/csv/cron/')
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)

    def test_system_importer_file_csv_create_cron_meta_redirect(self):
        """ test importer view """

        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_create_cron_meta', password='4Ka6NQdzpkuUIWqfqRE6')
        # create url (test seem to switch GET parameters)
        #destination = urllib.parse.quote('/admin/django_q/schedule/add/?name=system_importer_file_csv&func=dfirtrack_main.importer.file.csv.system_cron', safe='/?=&')
        destination = urllib.parse.quote('/admin/django_q/schedule/add/?func=dfirtrack_main.importer.file.csv.system_cron&name=system_importer_file_csv', safe='/?=&')
        # get response
        response = self.client.get('/system/importer/file/csv/cron', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=301, target_status_code=200)
