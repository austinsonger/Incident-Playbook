from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.test import TestCase
from django.utils import timezone
from dfirtrack.settings import BASE_DIR
from dfirtrack_main.importer.file.csv import system_cron
from dfirtrack_main.tests.system_importer.config_functions import set_csv_import_username, set_csv_import_filename, set_csv_import_path
import os
import urllib.parse


def create_file_no_read_permission(csv_import_path, csv_import_filename):
    """ create a file and remove all permissions """

    # build csv file path
    csv_path = f'{csv_import_path}/{csv_import_filename}'
    # create file
    csv_file = open(csv_path, 'w')
    # write content to file
    csv_file.write('This is no valid CSV file but that does not matter at the moment.')
    # close file
    csv_file.close()
    # remove all permissions
    os.chmod(csv_path, 0000)

    # return to test function
    return

class SystemImporterFileCsvCheckConfigContentFileSystemViewTestCase(TestCase):
    """ system importer file CSV view tests """

    @classmethod
    def setUpTestData(cls):
        """ one-time setup """

        # create users
        test_user = User.objects.create_user(username='testuser_system_importer_file_csv_check_content_file_system', password='mxsdGwJ2TINdQMq6rMNN')
        User.objects.create_user(username='message_user', password='8LHVC5R5D1bdVBJk56xn')

        # change config
        set_csv_import_username(test_user)

    """ path not existing """

    def test_system_importer_file_csv_check_content_file_system_create_cron_path_not_existing(self):
        """ test importer view """

        # change config
        set_csv_import_path('/path_not_existing')

        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_check_content_file_system', password='mxsdGwJ2TINdQMq6rMNN')
        # create url
        destination = urllib.parse.quote('/system/', safe='/')
        # get response
        response = self.client.get('/system/importer/file/csv/cron/', follow=True)
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)
        self.assertEqual(messages[0].message, 'CSV import path does not exist. Check config or file system!')
        self.assertEqual(messages[0].level_tag, 'error')

    def test_system_importer_file_csv_check_content_file_system_cron_path_not_existing(self):
        """ test importer view """

        # change config
        set_csv_import_path('/path_not_existing')

        # execute cron job / scheduled task
        system_cron()
        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_check_content_file_system', password='mxsdGwJ2TINdQMq6rMNN')
        # get response
        response = self.client.get('/system/')
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare
        self.assertEqual(str(response.context['user']), 'testuser_system_importer_file_csv_check_content_file_system')
        self.assertEqual(messages[0].message, '[Scheduled task CSV system importer] CSV import path does not exist. Check config or file system!')
        self.assertEqual(messages[0].level_tag, 'error')
        # switch user context
        self.client.logout()
        self.client.login(username='message_user', password='8LHVC5R5D1bdVBJk56xn')
        # get response
        response = self.client.get('/system/')
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare
        self.assertEqual(str(response.context['user']), 'message_user')
        self.assertEqual(messages[0].message, '[Scheduled task CSV system importer] CSV import path does not exist. Check config or file system!')
        self.assertEqual(messages[0].level_tag, 'error')

    def test_system_importer_file_csv_check_content_file_system_instant_path_not_existing(self):
        """ test importer view """

        # change config
        set_csv_import_path('/path_not_existing')

        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_check_content_file_system', password='mxsdGwJ2TINdQMq6rMNN')
        # create url
        destination = urllib.parse.quote('/system/', safe='/')
        # get response
        response = self.client.get('/system/importer/file/csv/instant/', follow=True)
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)
        self.assertEqual(messages[0].message, 'CSV import path does not exist. Check config or file system!')
        self.assertEqual(messages[0].level_tag, 'error')

    """ path no read permission """

    def test_system_importer_file_csv_check_content_file_system_create_cron_path_no_read_permission(self):
        """ test importer view """

        # change config
        set_csv_import_path('/root')

        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_check_content_file_system', password='mxsdGwJ2TINdQMq6rMNN')
        # create url
        destination = urllib.parse.quote('/system/', safe='/')
        # get response
        response = self.client.get('/system/importer/file/csv/cron/', follow=True)
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)
        self.assertEqual(messages[0].message, 'No read permission for CSV import path. Check config or file system!')
        self.assertEqual(messages[0].level_tag, 'error')

    def test_system_importer_file_csv_check_content_file_system_cron_path_no_read_permission(self):
        """ test importer view """

        # change config
        set_csv_import_path('/root')

        # execute cron job / scheduled task
        system_cron()
        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_check_content_file_system', password='mxsdGwJ2TINdQMq6rMNN')
        # get response
        response = self.client.get('/system/')
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare
        self.assertEqual(str(response.context['user']), 'testuser_system_importer_file_csv_check_content_file_system')
        self.assertEqual(messages[0].message, '[Scheduled task CSV system importer] No read permission for CSV import path. Check config or file system!')
        self.assertEqual(messages[0].level_tag, 'error')
        # switch user context
        self.client.logout()
        self.client.login(username='message_user', password='8LHVC5R5D1bdVBJk56xn')
        # get response
        response = self.client.get('/system/')
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare
        self.assertEqual(str(response.context['user']), 'message_user')
        self.assertEqual(messages[0].message, '[Scheduled task CSV system importer] No read permission for CSV import path. Check config or file system!')
        self.assertEqual(messages[0].level_tag, 'error')

    def test_system_importer_file_csv_check_content_file_system_instant_path_no_read_permission(self):
        """ test importer view """

        # change config
        set_csv_import_path('/root')

        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_check_content_file_system', password='mxsdGwJ2TINdQMq6rMNN')
        # create url
        destination = urllib.parse.quote('/system/', safe='/')
        # get response
        response = self.client.get('/system/importer/file/csv/instant/', follow=True)
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)
        self.assertEqual(messages[0].message, 'No read permission for CSV import path. Check config or file system!')
        self.assertEqual(messages[0].level_tag, 'error')

    """ file not existing """

    def test_system_importer_file_csv_check_content_file_system_create_cron_file_not_existing(self):
        """ test importer view """

        # change config
        set_csv_import_path('/tmp')
        # change config
        set_csv_import_filename('filename_not_existing.abc')

        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_check_content_file_system', password='mxsdGwJ2TINdQMq6rMNN')
        # create url
        destination = urllib.parse.quote('/system/', safe='/')
        # get response
        response = self.client.get('/system/importer/file/csv/cron/', follow=True)
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)
        self.assertEqual(messages[0].message, 'CSV import file does not exist. Check config or provide file!')
        self.assertEqual(messages[0].level_tag, 'error')

    def test_system_importer_file_csv_check_content_file_system_cron_file_not_existing(self):
        """ test importer view """

        # change config
        set_csv_import_path('/tmp')
        # change config
        set_csv_import_filename('filename_not_existing.abc')

        # execute cron job / scheduled task
        system_cron()
        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_check_content_file_system', password='mxsdGwJ2TINdQMq6rMNN')
        # get response
        response = self.client.get('/system/')
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare
        self.assertEqual(str(response.context['user']), 'testuser_system_importer_file_csv_check_content_file_system')
        self.assertEqual(messages[0].message, '[Scheduled task CSV system importer] CSV import file does not exist. Check config or provide file!')
        self.assertEqual(messages[0].level_tag, 'error')
        # switch user context
        self.client.logout()
        self.client.login(username='message_user', password='8LHVC5R5D1bdVBJk56xn')
        # get response
        response = self.client.get('/system/')
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare
        self.assertEqual(str(response.context['user']), 'message_user')
        self.assertEqual(messages[0].message, '[Scheduled task CSV system importer] CSV import file does not exist. Check config or provide file!')
        self.assertEqual(messages[0].level_tag, 'error')

    def test_system_importer_file_csv_check_content_file_system_instant_file_not_existing(self):
        """ test importer view """

        # change config
        set_csv_import_path('/tmp')
        # change config
        set_csv_import_filename('filename_not_existing.abc')

        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_check_content_file_system', password='mxsdGwJ2TINdQMq6rMNN')
        # create url
        destination = urllib.parse.quote('/system/', safe='/')
        # get response
        response = self.client.get('/system/importer/file/csv/instant/', follow=True)
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)
        self.assertEqual(messages[0].message, 'CSV import file does not exist. Check config or provide file!')
        self.assertEqual(messages[0].level_tag, 'error')

    """ file no read permission """

    def test_system_importer_file_csv_check_content_file_system_create_cron_file_no_read_permission(self):
        """ test importer view """

        # get timestamp string
        t1 = timezone.now().strftime('%Y%m%d_%H%M%S')
        # set file system attributes
        csv_import_path = '/tmp'
        csv_import_filename = f'{t1}_create_cron_no_read_permission.csv'
        # create file
        create_file_no_read_permission(csv_import_path, csv_import_filename)
        # change config
        set_csv_import_path(csv_import_path)
        # change config
        set_csv_import_filename(csv_import_filename)

        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_check_content_file_system', password='mxsdGwJ2TINdQMq6rMNN')
        # create url
        destination = urllib.parse.quote('/system/', safe='/')
        # get response
        response = self.client.get('/system/importer/file/csv/cron/', follow=True)
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)
        self.assertEqual(messages[0].message, 'No read permission for CSV import file. Check config or file system!')
        self.assertEqual(messages[0].level_tag, 'error')

    def test_system_importer_file_csv_check_content_file_system_cron_file_no_read_permission(self):
        """ test importer view """

        # get timestamp string
        t1 = timezone.now().strftime('%Y%m%d_%H%M%S')
        # set file system attributes
        csv_import_path = '/tmp'
        csv_import_filename = f'{t1}_cron_no_read_permission.csv'
        # create file
        create_file_no_read_permission(csv_import_path, csv_import_filename)
        # change config
        set_csv_import_path(csv_import_path)
        # change config
        set_csv_import_filename(csv_import_filename)

        # execute cron job / scheduled task
        system_cron()
        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_check_content_file_system', password='mxsdGwJ2TINdQMq6rMNN')
        # get response
        response = self.client.get('/system/')
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare
        self.assertEqual(str(response.context['user']), 'testuser_system_importer_file_csv_check_content_file_system')
        self.assertEqual(messages[0].message, '[Scheduled task CSV system importer] No read permission for CSV import file. Check config or file system!')
        self.assertEqual(messages[0].level_tag, 'error')
        # switch user context
        self.client.logout()
        self.client.login(username='message_user', password='8LHVC5R5D1bdVBJk56xn')
        # get response
        response = self.client.get('/system/')
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare
        self.assertEqual(str(response.context['user']), 'message_user')
        self.assertEqual(messages[0].message, '[Scheduled task CSV system importer] No read permission for CSV import file. Check config or file system!')
        self.assertEqual(messages[0].level_tag, 'error')

    def test_system_importer_file_csv_check_content_file_system_instant_file_no_read_permission(self):
        """ test importer view """

        # get timestamp string
        t1 = timezone.now().strftime('%Y%m%d_%H%M%S')
        # set file system attributes
        csv_import_path = '/tmp'
        csv_import_filename = f'{t1}_instant_no_read_permission.csv'
        # create file
        create_file_no_read_permission(csv_import_path, csv_import_filename)
        # change config
        set_csv_import_path(csv_import_path)
        # change config
        set_csv_import_filename(csv_import_filename)

        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_check_content_file_system', password='mxsdGwJ2TINdQMq6rMNN')
        # create url
        destination = urllib.parse.quote('/system/', safe='/')
        # get response
        response = self.client.get('/system/importer/file/csv/instant/', follow=True)
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)
        self.assertEqual(messages[0].message, 'No read permission for CSV import file. Check config or file system!')
        self.assertEqual(messages[0].level_tag, 'error')

    """ file empty """

    def test_system_importer_file_csv_check_content_file_system_create_cron_file_empty(self):
        """ test importer view """

        # change config
        set_csv_import_path(os.path.join(BASE_DIR, 'dfirtrack_main/tests/system_importer/system_importer_file_csv_files/'))
        # change config
        set_csv_import_filename('system_importer_file_csv_testfile_06_empty.csv')

        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_check_content_file_system', password='mxsdGwJ2TINdQMq6rMNN')
        # create url
        destination = urllib.parse.quote('/system/', safe='/')
        # get response
        response = self.client.get('/system/importer/file/csv/cron/', follow=True)
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)
        self.assertEqual(messages[0].message, 'CSV import file is empty. Check config or file system!')
        self.assertEqual(messages[0].level_tag, 'error')

    def test_system_importer_file_csv_check_content_file_system_cron_file_empty(self):
        """ test importer view """

        # change config
        set_csv_import_path(os.path.join(BASE_DIR, 'dfirtrack_main/tests/system_importer/system_importer_file_csv_files/'))
        # change config
        set_csv_import_filename('system_importer_file_csv_testfile_06_empty.csv')

        # execute cron job / scheduled task
        system_cron()
        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_check_content_file_system', password='mxsdGwJ2TINdQMq6rMNN')
        # get response
        response = self.client.get('/system/')
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare
        self.assertEqual(str(response.context['user']), 'testuser_system_importer_file_csv_check_content_file_system')
        self.assertEqual(messages[0].message, '[Scheduled task CSV system importer] CSV import file is empty. Check config or file system!')
        self.assertEqual(messages[0].level_tag, 'error')
        # switch user context
        self.client.logout()
        self.client.login(username='message_user', password='8LHVC5R5D1bdVBJk56xn')
        # get response
        response = self.client.get('/system/')
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare
        self.assertEqual(str(response.context['user']), 'message_user')
        self.assertEqual(messages[0].message, '[Scheduled task CSV system importer] CSV import file is empty. Check config or file system!')
        self.assertEqual(messages[0].level_tag, 'error')

    def test_system_importer_file_csv_check_content_file_system_instant_file_empty(self):
        """ test importer view """

        # change config
        set_csv_import_path(os.path.join(BASE_DIR, 'dfirtrack_main/tests/system_importer/system_importer_file_csv_files/'))
        # change config
        set_csv_import_filename('system_importer_file_csv_testfile_06_empty.csv')

        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_check_content_file_system', password='mxsdGwJ2TINdQMq6rMNN')
        # create url
        destination = urllib.parse.quote('/system/', safe='/')
        # get response
        response = self.client.get('/system/importer/file/csv/instant/', follow=True)
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)
        self.assertEqual(messages[0].message, 'CSV import file is empty. Check config or file system!')
        self.assertEqual(messages[0].level_tag, 'error')
