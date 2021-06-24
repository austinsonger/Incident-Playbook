from datetime import datetime
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.test import TestCase
from django.utils import timezone
from dfirtrack.settings import BASE_DIR
from dfirtrack_config.models import SystemImporterFileCsvConfigModel
from dfirtrack_main.importer.file.csv import system_cron
from dfirtrack_main.models import Analysisstatus, System, Systemstatus
from dfirtrack_main.tests.system_importer.config_functions import set_csv_import_filename, set_csv_skip_existing_system
from mock import patch
import os


def create_system(system_name):
    """ create system (only needed in some tests, therefore not implemented with 'setUp()') """

    # get user
    test_user = User.objects.get(username='testuser_system_importer_file_csv_messages')
    # get object
    systemstatus_1 = Systemstatus.objects.get(systemstatus_name='systemstatus_1')

    # create object
    System.objects.create(
        system_name = system_name,
        systemstatus = systemstatus_1,
        system_modify_time = timezone.now(),
        system_created_by_user_id = test_user,
        system_modified_by_user_id = test_user,
    )

    # return to test function
    return

class SystemImporterFileCsvMessagesViewTestCase(TestCase):
    """ system importer file CSV view tests """

    @classmethod
    def setUpTestData(cls):
        """ one-time setup """

        # create user
        test_user = User.objects.create_user(username='testuser_system_importer_file_csv_messages', password='a9aZU5mlnXbVv4TTgcMW')
        User.objects.create_user(username='message_user', password='uNQIBX9woW0M834mJWex')

        # create objects
        analysisstatus_1 = Analysisstatus.objects.create(analysisstatus_name='analysisstatus_1')
        analysisstatus_2 = Analysisstatus.objects.create(analysisstatus_name='analysisstatus_2')
        systemstatus_1 = Systemstatus.objects.create(systemstatus_name='systemstatus_1')
        systemstatus_2 = Systemstatus.objects.create(systemstatus_name='systemstatus_2')

        # build local path with test files
        csv_import_path = os.path.join(BASE_DIR, 'dfirtrack_main/tests/system_importer/system_importer_file_csv_files/')

        # change config
        system_importer_file_csv_config_model = SystemImporterFileCsvConfigModel.objects.get(system_importer_file_csv_config_name='SystemImporterFileCsvConfig')
        system_importer_file_csv_config_model.csv_column_system = 1
        system_importer_file_csv_config_model.csv_headline = False
        system_importer_file_csv_config_model.csv_import_path = csv_import_path
        system_importer_file_csv_config_model.csv_import_username = test_user
        system_importer_file_csv_config_model.csv_default_systemstatus = systemstatus_1
        system_importer_file_csv_config_model.csv_default_analysisstatus = analysisstatus_1
        system_importer_file_csv_config_model.csv_default_tagfree_systemstatus = systemstatus_2
        system_importer_file_csv_config_model.csv_default_tagfree_analysisstatus = analysisstatus_2
        system_importer_file_csv_config_model.csv_tag_lock_systemstatus = 'LOCK_SYSTEMSTATUS'
        system_importer_file_csv_config_model.csv_tag_lock_analysisstatus = 'LOCK_ANALYSISSTATUS'
        system_importer_file_csv_config_model.csv_remove_tag = 'tag_remove_prefix'
        system_importer_file_csv_config_model.csv_field_delimiter = 'field_comma'
        system_importer_file_csv_config_model.csv_text_quote = 'text_double_quotation_marks'
        system_importer_file_csv_config_model.csv_ip_delimiter = 'ip_semicolon'
        system_importer_file_csv_config_model.csv_tag_delimiter = 'tag_space'
        system_importer_file_csv_config_model.save()

    def test_system_importer_file_csv_messages_cron_single_system_create(self):
        """ test importer view """

        # change config
        set_csv_import_filename('system_importer_file_csv_testfile_11_messages_single_system.csv')
        # change config
        set_csv_skip_existing_system(True)

        # mock timezone.now()
        t_1 = datetime(2021, 3, 7, 10, 45, tzinfo=timezone.utc)
        with patch.object(timezone, 'now', return_value=t_1):

            # execute cron job / scheduled task
            system_cron()

        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_messages', password='a9aZU5mlnXbVv4TTgcMW')
        # get response
        response = self.client.get('/system/')
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare
        self.assertEqual(str(response.context['user']), 'testuser_system_importer_file_csv_messages')
        self.assertEqual(messages[0].message, 'System CSV importer: created: 1 | updated: 0 | skipped: 0 | multiple: 0 [2021-03-07 10:45:00 - 2021-03-07 10:45:00]')
        self.assertEqual(messages[0].level_tag, 'success')
        # switch user context
        self.client.logout()
        self.client.login(username='message_user', password='uNQIBX9woW0M834mJWex')
        # get response
        response = self.client.get('/system/')
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare
        self.assertEqual(str(response.context['user']), 'message_user')
        self.assertEqual(messages[0].message, 'System CSV importer: created: 1 | updated: 0 | skipped: 0 | multiple: 0 [2021-03-07 10:45:00 - 2021-03-07 10:45:00]')
        self.assertEqual(messages[0].level_tag, 'success')

    def test_system_importer_file_csv_messages_cron_single_system_update(self):
        """ test importer view """

        # create system
        create_system('system_csv_11_001')

        # change config
        set_csv_import_filename('system_importer_file_csv_testfile_11_messages_single_system.csv')
        # change config
        set_csv_skip_existing_system(False)

        # mock timezone.now()
        t_2 = datetime(2021, 3, 7, 10, 50, tzinfo=timezone.utc)
        with patch.object(timezone, 'now', return_value=t_2):

            # execute cron job / scheduled task
            system_cron()

        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_messages', password='a9aZU5mlnXbVv4TTgcMW')
        # get response
        response = self.client.get('/system/')
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare
        self.assertEqual(str(response.context['user']), 'testuser_system_importer_file_csv_messages')
        self.assertEqual(messages[0].message, 'System CSV importer: created: 0 | updated: 1 | skipped: 0 | multiple: 0 [2021-03-07 10:50:00 - 2021-03-07 10:50:00]')
        self.assertEqual(messages[0].level_tag, 'success')
        # switch user context
        self.client.logout()
        self.client.login(username='message_user', password='uNQIBX9woW0M834mJWex')
        # get response
        response = self.client.get('/system/')
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare
        self.assertEqual(str(response.context['user']), 'message_user')
        self.assertEqual(messages[0].message, 'System CSV importer: created: 0 | updated: 1 | skipped: 0 | multiple: 0 [2021-03-07 10:50:00 - 2021-03-07 10:50:00]')
        self.assertEqual(messages[0].level_tag, 'success')

    def test_system_importer_file_csv_messages_cron_single_system_skip(self):
        """ test importer view """

        # create system
        create_system('system_csv_11_001')

        # change config
        set_csv_import_filename('system_importer_file_csv_testfile_11_messages_single_system.csv')
        # change config
        set_csv_skip_existing_system(True)

        # mock timezone.now()
        t_3 = datetime(2021, 3, 7, 10, 55, tzinfo=timezone.utc)
        with patch.object(timezone, 'now', return_value=t_3):

            # execute cron job / scheduled task
            system_cron()

        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_messages', password='a9aZU5mlnXbVv4TTgcMW')
        # get response
        response = self.client.get('/system/')
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare
        self.assertEqual(str(response.context['user']), 'testuser_system_importer_file_csv_messages')
        self.assertEqual(messages[0].message, 'System CSV importer: created: 0 | updated: 0 | skipped: 1 | multiple: 0 [2021-03-07 10:55:00 - 2021-03-07 10:55:00]')
        self.assertEqual(messages[0].level_tag, 'success')
        # switch user context
        self.client.logout()
        self.client.login(username='message_user', password='uNQIBX9woW0M834mJWex')
        # get response
        response = self.client.get('/system/')
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare
        self.assertEqual(str(response.context['user']), 'message_user')
        self.assertEqual(messages[0].message, 'System CSV importer: created: 0 | updated: 0 | skipped: 1 | multiple: 0 [2021-03-07 10:55:00 - 2021-03-07 10:55:00]')
        self.assertEqual(messages[0].level_tag, 'success')

    def test_system_importer_file_csv_messages_cron_single_system_multiple(self):
        """ test importer view """

        # create system
        create_system('system_csv_11_001')
        create_system('system_csv_11_001')

        # change config
        set_csv_import_filename('system_importer_file_csv_testfile_11_messages_single_system.csv')
        # change config
        set_csv_skip_existing_system(False)

        # mock timezone.now()
        t_4 = datetime(2021, 3, 7, 11, 00, tzinfo=timezone.utc)
        with patch.object(timezone, 'now', return_value=t_4):

            # execute cron job / scheduled task
            system_cron()

        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_messages', password='a9aZU5mlnXbVv4TTgcMW')
        # get response
        response = self.client.get('/system/')
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare
        self.assertEqual(str(response.context['user']), 'testuser_system_importer_file_csv_messages')
        self.assertEqual(messages[0].message, 'System CSV importer: created: 0 | updated: 0 | skipped: 0 | multiple: 1 [2021-03-07 11:00:00 - 2021-03-07 11:00:00]')
        self.assertEqual(messages[0].level_tag, 'success')
        self.assertEqual(messages[1].message, "1 system was skipped because it existed several times. ['system_csv_11_001']")
        self.assertEqual(messages[1].level_tag, 'warning')
        # switch user context
        self.client.logout()
        self.client.login(username='message_user', password='uNQIBX9woW0M834mJWex')
        # get response
        response = self.client.get('/system/')
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare
        self.assertEqual(str(response.context['user']), 'message_user')
        self.assertEqual(messages[0].message, 'System CSV importer: created: 0 | updated: 0 | skipped: 0 | multiple: 1 [2021-03-07 11:00:00 - 2021-03-07 11:00:00]')
        self.assertEqual(messages[0].level_tag, 'success')
        self.assertEqual(messages[1].message, "1 system was skipped because it existed several times. ['system_csv_11_001']")
        self.assertEqual(messages[1].level_tag, 'warning')

    def test_system_importer_file_csv_messages_instant_single_system_create(self):
        """ test importer view """

        # change config
        set_csv_import_filename('system_importer_file_csv_testfile_11_messages_single_system.csv')
        # change config
        set_csv_skip_existing_system(True)

        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_messages', password='a9aZU5mlnXbVv4TTgcMW')
        # get response
        response = self.client.get('/system/importer/file/csv/instant/', follow=True)
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare
        self.assertEqual(messages[0].message, '1 system was created.')
        self.assertEqual(messages[0].level_tag, 'success')

    def test_system_importer_file_csv_messages_instant_single_system_update(self):
        """ test importer view """

        # create system
        create_system('system_csv_11_001')

        # change config
        set_csv_import_filename('system_importer_file_csv_testfile_11_messages_single_system.csv')
        # change config
        set_csv_skip_existing_system(False)

        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_messages', password='a9aZU5mlnXbVv4TTgcMW')
        # get response
        response = self.client.get('/system/importer/file/csv/instant/', follow=True)
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare
        self.assertEqual(messages[0].message, '1 system was updated.')
        self.assertEqual(messages[0].level_tag, 'success')

    def test_system_importer_file_csv_messages_instant_single_system_skip(self):
        """ test importer view """

        # create system
        create_system('system_csv_11_001')

        # change config
        set_csv_import_filename('system_importer_file_csv_testfile_11_messages_single_system.csv')
        # change config
        set_csv_skip_existing_system(True)

        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_messages', password='a9aZU5mlnXbVv4TTgcMW')
        # get response
        response = self.client.get('/system/importer/file/csv/instant/', follow=True)
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare
        self.assertEqual(messages[0].message, '1 system was skipped.')
        self.assertEqual(messages[0].level_tag, 'success')

    def test_system_importer_file_csv_messages_instant_single_system_multiple(self):
        """ test importer view """

        # create system
        create_system('system_csv_11_001')
        create_system('system_csv_11_001')

        # change config
        set_csv_import_filename('system_importer_file_csv_testfile_11_messages_single_system.csv')
        # change config
        set_csv_skip_existing_system(True)

        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_messages', password='a9aZU5mlnXbVv4TTgcMW')
        # get response
        response = self.client.get('/system/importer/file/csv/instant/', follow=True)
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare
        self.assertEqual(messages[0].message, "1 system was skipped because it existed several times. ['system_csv_11_001']")
        self.assertEqual(messages[0].level_tag, 'warning')

    def test_system_importer_file_csv_messages_upload_post_single_system_create(self):
        """ test importer view """

        # change config
        set_csv_skip_existing_system(True)

        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_messages', password='a9aZU5mlnXbVv4TTgcMW')
        # open upload file
        systemcsv = open(os.path.join(BASE_DIR, 'dfirtrack_main/tests/system_importer/system_importer_file_csv_files/system_importer_file_csv_testfile_11_messages_single_system.csv'), 'r')
        # create post data
        data_dict = {
            'systemcsv': systemcsv,
        }
        # get response
        response = self.client.post('/system/importer/file/csv/upload/', data_dict)
        # close file
        systemcsv.close()
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare
        self.assertEqual(messages[0].message, '1 system was created.')
        self.assertEqual(messages[0].level_tag, 'success')

    def test_system_importer_file_csv_messages_upload_post_single_system_update(self):
        """ test importer view """

        # create system
        create_system('system_csv_11_001')

        # change config
        set_csv_skip_existing_system(False)

        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_messages', password='a9aZU5mlnXbVv4TTgcMW')
        # open upload file
        systemcsv = open(os.path.join(BASE_DIR, 'dfirtrack_main/tests/system_importer/system_importer_file_csv_files/system_importer_file_csv_testfile_11_messages_single_system.csv'), 'r')
        # create post data
        data_dict = {
            'systemcsv': systemcsv,
        }
        # get response
        response = self.client.post('/system/importer/file/csv/upload/', data_dict)
        # close file
        systemcsv.close()
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare
        self.assertEqual(messages[0].message, '1 system was updated.')
        self.assertEqual(messages[0].level_tag, 'success')

    def test_system_importer_file_csv_messages_upload_post_single_system_skip(self):
        """ test importer view """

        # create system
        create_system('system_csv_11_001')

        # change config
        set_csv_skip_existing_system(True)

        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_messages', password='a9aZU5mlnXbVv4TTgcMW')
        # open upload file
        systemcsv = open(os.path.join(BASE_DIR, 'dfirtrack_main/tests/system_importer/system_importer_file_csv_files/system_importer_file_csv_testfile_11_messages_single_system.csv'), 'r')
        # create post data
        data_dict = {
            'systemcsv': systemcsv,
        }
        # get response
        response = self.client.post('/system/importer/file/csv/upload/', data_dict)
        # close file
        systemcsv.close()
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare
        self.assertEqual(messages[0].message, '1 system was skipped.')
        self.assertEqual(messages[0].level_tag, 'success')

    def test_system_importer_file_csv_messages_upload_post_single_system_multiple(self):
        """ test importer view """

        # create system
        create_system('system_csv_11_001')
        create_system('system_csv_11_001')

        # change config
        set_csv_skip_existing_system(True)

        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_messages', password='a9aZU5mlnXbVv4TTgcMW')
        # open upload file
        systemcsv = open(os.path.join(BASE_DIR, 'dfirtrack_main/tests/system_importer/system_importer_file_csv_files/system_importer_file_csv_testfile_11_messages_single_system.csv'), 'r')
        # create post data
        data_dict = {
            'systemcsv': systemcsv,
        }
        # get response
        response = self.client.post('/system/importer/file/csv/upload/', data_dict)
        # close file
        systemcsv.close()
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare
        self.assertEqual(messages[0].message, "1 system was skipped because it existed several times. ['system_csv_11_001']")
        self.assertEqual(messages[0].level_tag, 'warning')

    def test_system_importer_file_csv_messages_cron_many_systems_create(self):
        """ test importer view """

        # change config
        set_csv_import_filename('system_importer_file_csv_testfile_12_messages_many_systems.csv')
        # change config
        set_csv_skip_existing_system(True)

        # mock timezone.now()
        t_5 = datetime(2021, 3, 7, 11, 25, tzinfo=timezone.utc)
        with patch.object(timezone, 'now', return_value=t_5):

            # execute cron job / scheduled task
            system_cron()

        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_messages', password='a9aZU5mlnXbVv4TTgcMW')
        # get response
        response = self.client.get('/system/')
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare
        self.assertEqual(str(response.context['user']), 'testuser_system_importer_file_csv_messages')
        self.assertEqual(messages[0].message, 'System CSV importer: created: 3 | updated: 0 | skipped: 0 | multiple: 0 [2021-03-07 11:25:00 - 2021-03-07 11:25:00]')
        self.assertEqual(messages[0].level_tag, 'success')
        # switch user context
        self.client.logout()
        self.client.login(username='message_user', password='uNQIBX9woW0M834mJWex')
        # get response
        response = self.client.get('/system/')
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare
        self.assertEqual(str(response.context['user']), 'message_user')
        self.assertEqual(messages[0].message, 'System CSV importer: created: 3 | updated: 0 | skipped: 0 | multiple: 0 [2021-03-07 11:25:00 - 2021-03-07 11:25:00]')
        self.assertEqual(messages[0].level_tag, 'success')

    def test_system_importer_file_csv_messages_cron_many_systems_update(self):
        """ test importer view """

        # create systems
        create_system('system_csv_12_001')
        create_system('system_csv_12_002')
        create_system('system_csv_12_003')

        # change config
        set_csv_import_filename('system_importer_file_csv_testfile_12_messages_many_systems.csv')
        # change config
        set_csv_skip_existing_system(False)

        # mock timezone.now()
        t_6 = datetime(2021, 3, 7, 11, 30, tzinfo=timezone.utc)
        with patch.object(timezone, 'now', return_value=t_6):

            # execute cron job / scheduled task
            system_cron()

        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_messages', password='a9aZU5mlnXbVv4TTgcMW')
        # get response
        response = self.client.get('/system/')
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare
        self.assertEqual(str(response.context['user']), 'testuser_system_importer_file_csv_messages')
        self.assertEqual(messages[0].message, 'System CSV importer: created: 0 | updated: 3 | skipped: 0 | multiple: 0 [2021-03-07 11:30:00 - 2021-03-07 11:30:00]')
        self.assertEqual(messages[0].level_tag, 'success')
        # switch user context
        self.client.logout()
        self.client.login(username='message_user', password='uNQIBX9woW0M834mJWex')
        # get response
        response = self.client.get('/system/')
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare
        self.assertEqual(str(response.context['user']), 'message_user')
        self.assertEqual(messages[0].message, 'System CSV importer: created: 0 | updated: 3 | skipped: 0 | multiple: 0 [2021-03-07 11:30:00 - 2021-03-07 11:30:00]')
        self.assertEqual(messages[0].level_tag, 'success')

    def test_system_importer_file_csv_messages_cron_many_systems_skip(self):
        """ test importer view """

        # create systems
        create_system('system_csv_12_001')
        create_system('system_csv_12_002')
        create_system('system_csv_12_003')

        # change config
        set_csv_import_filename('system_importer_file_csv_testfile_12_messages_many_systems.csv')
        # change config
        set_csv_skip_existing_system(True)

        # mock timezone.now()
        t_7 = datetime(2021, 3, 7, 11, 35, tzinfo=timezone.utc)
        with patch.object(timezone, 'now', return_value=t_7):

            # execute cron job / scheduled task
            system_cron()

        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_messages', password='a9aZU5mlnXbVv4TTgcMW')
        # get response
        response = self.client.get('/system/')
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare
        self.assertEqual(str(response.context['user']), 'testuser_system_importer_file_csv_messages')
        self.assertEqual(messages[0].message, 'System CSV importer: created: 0 | updated: 0 | skipped: 3 | multiple: 0 [2021-03-07 11:35:00 - 2021-03-07 11:35:00]')
        self.assertEqual(messages[0].level_tag, 'success')
        # switch user context
        self.client.logout()
        self.client.login(username='message_user', password='uNQIBX9woW0M834mJWex')
        # get response
        response = self.client.get('/system/')
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare
        self.assertEqual(str(response.context['user']), 'message_user')
        self.assertEqual(messages[0].message, 'System CSV importer: created: 0 | updated: 0 | skipped: 3 | multiple: 0 [2021-03-07 11:35:00 - 2021-03-07 11:35:00]')
        self.assertEqual(messages[0].level_tag, 'success')

    def test_system_importer_file_csv_messages_cron_many_systems_multiple(self):
        """ test importer view """

        # create systems
        create_system('system_csv_12_001')
        create_system('system_csv_12_001')
        create_system('system_csv_12_002')
        create_system('system_csv_12_002')
        create_system('system_csv_12_003')
        create_system('system_csv_12_003')

        # change config
        set_csv_import_filename('system_importer_file_csv_testfile_12_messages_many_systems.csv')
        # change config
        set_csv_skip_existing_system(False)

        # mock timezone.now()
        t_8 = datetime(2021, 3, 7, 11, 40, tzinfo=timezone.utc)
        with patch.object(timezone, 'now', return_value=t_8):

            # execute cron job / scheduled task
            system_cron()

        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_messages', password='a9aZU5mlnXbVv4TTgcMW')
        # get response
        response = self.client.get('/system/')
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare
        self.assertEqual(str(response.context['user']), 'testuser_system_importer_file_csv_messages')
        self.assertEqual(messages[0].message, 'System CSV importer: created: 0 | updated: 0 | skipped: 0 | multiple: 3 [2021-03-07 11:40:00 - 2021-03-07 11:40:00]')
        self.assertEqual(messages[0].level_tag, 'success')
        self.assertEqual(messages[1].message, "3 systems were skipped because they existed several times. ['system_csv_12_001', 'system_csv_12_002', 'system_csv_12_003']")
        self.assertEqual(messages[1].level_tag, 'warning')
        # switch user context
        self.client.logout()
        self.client.login(username='message_user', password='uNQIBX9woW0M834mJWex')
        # get response
        response = self.client.get('/system/')
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare
        self.assertEqual(str(response.context['user']), 'message_user')
        self.assertEqual(messages[0].message, 'System CSV importer: created: 0 | updated: 0 | skipped: 0 | multiple: 3 [2021-03-07 11:40:00 - 2021-03-07 11:40:00]')
        self.assertEqual(messages[0].level_tag, 'success')
        self.assertEqual(messages[1].message, "3 systems were skipped because they existed several times. ['system_csv_12_001', 'system_csv_12_002', 'system_csv_12_003']")
        self.assertEqual(messages[1].level_tag, 'warning')

    def test_system_importer_file_csv_messages_instant_many_systems_create(self):
        """ test importer view """

        # change config
        set_csv_import_filename('system_importer_file_csv_testfile_12_messages_many_systems.csv')
        # change config
        set_csv_skip_existing_system(True)

        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_messages', password='a9aZU5mlnXbVv4TTgcMW')
        # get response
        response = self.client.get('/system/importer/file/csv/instant/', follow=True)
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare
        self.assertEqual(messages[0].message, '3 systems were created.')
        self.assertEqual(messages[0].level_tag, 'success')

    def test_system_importer_file_csv_messages_instant_many_systems_update(self):
        """ test importer view """

        # create systems
        create_system('system_csv_12_001')
        create_system('system_csv_12_002')
        create_system('system_csv_12_003')

        # change config
        set_csv_import_filename('system_importer_file_csv_testfile_12_messages_many_systems.csv')
        # change config
        set_csv_skip_existing_system(False)

        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_messages', password='a9aZU5mlnXbVv4TTgcMW')
        # get response
        response = self.client.get('/system/importer/file/csv/instant/', follow=True)
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare
        self.assertEqual(messages[0].message, '3 systems were updated.')
        self.assertEqual(messages[0].level_tag, 'success')

    def test_system_importer_file_csv_messages_instant_many_systems_skip(self):
        """ test importer view """

        # create systems
        create_system('system_csv_12_001')
        create_system('system_csv_12_002')
        create_system('system_csv_12_003')

        # change config
        set_csv_import_filename('system_importer_file_csv_testfile_12_messages_many_systems.csv')
        # change config
        set_csv_skip_existing_system(True)

        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_messages', password='a9aZU5mlnXbVv4TTgcMW')
        # get response
        response = self.client.get('/system/importer/file/csv/instant/', follow=True)
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare
        self.assertEqual(messages[0].message, '3 systems were skipped.')
        self.assertEqual(messages[0].level_tag, 'success')

    def test_system_importer_file_csv_messages_instant_many_systems_multiple(self):
        """ test importer view """

        # create systems
        create_system('system_csv_12_001')
        create_system('system_csv_12_001')
        create_system('system_csv_12_002')
        create_system('system_csv_12_002')
        create_system('system_csv_12_003')
        create_system('system_csv_12_003')

        # change config
        set_csv_import_filename('system_importer_file_csv_testfile_12_messages_many_systems.csv')
        # change config
        set_csv_skip_existing_system(True)

        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_messages', password='a9aZU5mlnXbVv4TTgcMW')
        # get response
        response = self.client.get('/system/importer/file/csv/instant/', follow=True)
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare
        self.assertEqual(messages[0].message, "3 systems were skipped because they existed several times. ['system_csv_12_001', 'system_csv_12_002', 'system_csv_12_003']")
        self.assertEqual(messages[0].level_tag, 'warning')

    def test_system_importer_file_csv_messages_upload_post_many_systems_create(self):
        """ test importer view """

        # change config
        set_csv_skip_existing_system(True)

        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_messages', password='a9aZU5mlnXbVv4TTgcMW')
        # open upload file
        systemcsv = open(os.path.join(BASE_DIR, 'dfirtrack_main/tests/system_importer/system_importer_file_csv_files/system_importer_file_csv_testfile_12_messages_many_systems.csv'), 'r')
        # create post data
        data_dict = {
            'systemcsv': systemcsv,
        }
        # get response
        response = self.client.post('/system/importer/file/csv/upload/', data_dict)
        # close file
        systemcsv.close()
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare
        self.assertEqual(messages[0].message, '3 systems were created.')
        self.assertEqual(messages[0].level_tag, 'success')

    def test_system_importer_file_csv_messages_upload_post_many_systems_update(self):
        """ test importer view """

        # create systems
        create_system('system_csv_12_001')
        create_system('system_csv_12_002')
        create_system('system_csv_12_003')

        # change config
        set_csv_skip_existing_system(False)

        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_messages', password='a9aZU5mlnXbVv4TTgcMW')
        # open upload file
        systemcsv = open(os.path.join(BASE_DIR, 'dfirtrack_main/tests/system_importer/system_importer_file_csv_files/system_importer_file_csv_testfile_12_messages_many_systems.csv'), 'r')
        # create post data
        data_dict = {
            'systemcsv': systemcsv,
        }
        # get response
        response = self.client.post('/system/importer/file/csv/upload/', data_dict)
        # close file
        systemcsv.close()
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare
        self.assertEqual(messages[0].message, '3 systems were updated.')
        self.assertEqual(messages[0].level_tag, 'success')

    def test_system_importer_file_csv_messages_upload_post_many_systems_skip(self):
        """ test importer view """

        # create systems
        create_system('system_csv_12_001')
        create_system('system_csv_12_002')
        create_system('system_csv_12_003')

        # change config
        set_csv_skip_existing_system(True)

        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_messages', password='a9aZU5mlnXbVv4TTgcMW')
        # open upload file
        systemcsv = open(os.path.join(BASE_DIR, 'dfirtrack_main/tests/system_importer/system_importer_file_csv_files/system_importer_file_csv_testfile_12_messages_many_systems.csv'), 'r')
        # create post data
        data_dict = {
            'systemcsv': systemcsv,
        }
        # get response
        response = self.client.post('/system/importer/file/csv/upload/', data_dict)
        # close file
        systemcsv.close()
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare
        self.assertEqual(messages[0].message, '3 systems were skipped.')
        self.assertEqual(messages[0].level_tag, 'success')

    def test_system_importer_file_csv_messages_upload_post_many_systems_multiple(self):
        """ test importer view """

        # create systems
        create_system('system_csv_12_001')
        create_system('system_csv_12_001')
        create_system('system_csv_12_002')
        create_system('system_csv_12_002')
        create_system('system_csv_12_003')
        create_system('system_csv_12_003')

        # change config
        set_csv_skip_existing_system(True)

        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_messages', password='a9aZU5mlnXbVv4TTgcMW')
        # open upload file
        systemcsv = open(os.path.join(BASE_DIR, 'dfirtrack_main/tests/system_importer/system_importer_file_csv_files/system_importer_file_csv_testfile_12_messages_many_systems.csv'), 'r')
        # create post data
        data_dict = {
            'systemcsv': systemcsv,
        }
        # get response
        response = self.client.post('/system/importer/file/csv/upload/', data_dict)
        # close file
        systemcsv.close()
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare
        self.assertEqual(messages[0].message, "3 systems were skipped because they existed several times. ['system_csv_12_001', 'system_csv_12_002', 'system_csv_12_003']")
        self.assertEqual(messages[0].level_tag, 'warning')
