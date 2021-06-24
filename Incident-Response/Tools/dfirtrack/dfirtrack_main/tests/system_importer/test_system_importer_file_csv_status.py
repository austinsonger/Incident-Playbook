from datetime import datetime
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.test import TestCase
from django.utils import timezone
from dfirtrack.settings import BASE_DIR
from dfirtrack_config.models import SystemImporterFileCsvConfigModel
from dfirtrack_main.importer.file.csv import system_cron
from dfirtrack_main.models import Analysisstatus, System, Systemstatus, Tag, Tagcolor
from dfirtrack_main.tests.system_importer.config_functions import set_config_tagfree_status, set_csv_import_filename
from mock import patch
import os
import urllib.parse


def compare_messages_lock_status(self, messages):
    """ compare messages """

    # set counter
    message_counter = 0

    # compare - messages
    self.assertEqual(messages[message_counter].message, '1 system was created.')
    self.assertEqual(messages[message_counter].level_tag, 'success')
    message_counter += 1
    self.assertEqual(messages[message_counter].message, '2 systems were updated.')
    self.assertEqual(messages[message_counter].level_tag, 'success')
    message_counter += 1

    # return to test function
    return self

def compare_system_and_attributes_lock_status(self):
    """ compare systems and associated attributes """

    # compare - systems / attributes
    self.assertTrue(System.objects.filter(system_name='system_csv_34_001').exists())
    self.assertTrue(System.objects.filter(system_name='system_csv_34_002').exists())
    self.assertTrue(System.objects.filter(system_name='system_csv_34_003').exists())
    # status of existing system w/o lock tags gets updated according to config
    self.assertEqual(System.objects.get(system_name='system_csv_34_001').analysisstatus, Analysisstatus.objects.get(analysisstatus_name='analysisstatus_2'))
    self.assertEqual(System.objects.get(system_name='system_csv_34_001').systemstatus, Systemstatus.objects.get(systemstatus_name='systemstatus_2'))
    # status of existing system w/ lock tags preserved
    self.assertEqual(System.objects.get(system_name='system_csv_34_002').analysisstatus, Analysisstatus.objects.get(analysisstatus_name='analysisstatus_1'))
    self.assertEqual(System.objects.get(system_name='system_csv_34_002').systemstatus, Systemstatus.objects.get(systemstatus_name='systemstatus_1'))
    # status of new system is set according to config
    self.assertEqual(System.objects.get(system_name='system_csv_34_003').analysisstatus, Analysisstatus.objects.get(analysisstatus_name='analysisstatus_2'))
    self.assertEqual(System.objects.get(system_name='system_csv_34_003').systemstatus, Systemstatus.objects.get(systemstatus_name='systemstatus_2'))

    # return to test function
    return self

def compare_messages_tagfree_status(self, messages):
    """ compare messages """

    pass

    # set counter
    message_counter = 0

    # compare - messages
    self.assertEqual(messages[message_counter].message, '2 systems were created.')
    self.assertEqual(messages[message_counter].level_tag, 'success')
    message_counter += 1
    self.assertEqual(messages[message_counter].message, '4 systems were updated.')
    self.assertEqual(messages[message_counter].level_tag, 'success')
    message_counter += 1

    # return to test function
    return self

def compare_system_and_attributes_tagfree_status(self):
    """ compare systems and associated attributes """

    pass

    # compare - systems / attributes
    self.assertTrue(System.objects.filter(system_name='system_csv_35_001').exists())
    self.assertTrue(System.objects.filter(system_name='system_csv_35_002').exists())
    self.assertTrue(System.objects.filter(system_name='system_csv_35_003').exists())
    self.assertTrue(System.objects.filter(system_name='system_csv_35_004').exists())
    self.assertTrue(System.objects.filter(system_name='system_csv_35_005').exists())
    self.assertTrue(System.objects.filter(system_name='system_csv_35_006').exists())
    # existing system - gets status 2 (because of tag)
    self.assertEqual(System.objects.get(system_name='system_csv_35_001').analysisstatus, Analysisstatus.objects.get(analysisstatus_name='analysisstatus_2'))
    self.assertEqual(System.objects.get(system_name='system_csv_35_001').systemstatus, Systemstatus.objects.get(systemstatus_name='systemstatus_2'))
    # existing system - gets status 3 (because tagfree)
    self.assertEqual(System.objects.get(system_name='system_csv_35_002').analysisstatus, Analysisstatus.objects.get(analysisstatus_name='analysisstatus_3'))
    self.assertEqual(System.objects.get(system_name='system_csv_35_002').systemstatus, Systemstatus.objects.get(systemstatus_name='systemstatus_3'))
    # existing system - keeps status 1 (because lock tag)
    self.assertEqual(System.objects.get(system_name='system_csv_35_003').analysisstatus, Analysisstatus.objects.get(analysisstatus_name='analysisstatus_1'))
    self.assertEqual(System.objects.get(system_name='system_csv_35_003').systemstatus, Systemstatus.objects.get(systemstatus_name='systemstatus_1'))
    # existing system - keeps status 1 (because lock tag)
    self.assertEqual(System.objects.get(system_name='system_csv_35_004').analysisstatus, Analysisstatus.objects.get(analysisstatus_name='analysisstatus_1'))
    self.assertEqual(System.objects.get(system_name='system_csv_35_004').systemstatus, Systemstatus.objects.get(systemstatus_name='systemstatus_1'))
    # new system - gets status 2 (because of tag)
    self.assertEqual(System.objects.get(system_name='system_csv_35_005').analysisstatus, Analysisstatus.objects.get(analysisstatus_name='analysisstatus_2'))
    self.assertEqual(System.objects.get(system_name='system_csv_35_005').systemstatus, Systemstatus.objects.get(systemstatus_name='systemstatus_2'))
    # new system - gets status 3 (because tagfree)
    self.assertEqual(System.objects.get(system_name='system_csv_35_006').analysisstatus, Analysisstatus.objects.get(analysisstatus_name='analysisstatus_3'))
    self.assertEqual(System.objects.get(system_name='system_csv_35_006').systemstatus, Systemstatus.objects.get(systemstatus_name='systemstatus_3'))

    # return to test function
    return self

class SystemImporterFileCsvStatusViewTestCase(TestCase):
    """ system importer file CSV view tests """

    @classmethod
    def setUpTestData(cls):
        """ one-time setup """

        """ create objects """

        # create users
        test_user = User.objects.create_user(username='testuser_system_importer_file_csv_status', password='Tsu0Q6SDhuxMH2APXMBT')
        User.objects.create_user(username='message_user', password='cwfOLfHnI33Y0g90gcN9')

        # create objects
        analysisstatus_1 = Analysisstatus.objects.create(analysisstatus_name='analysisstatus_1')
        analysisstatus_2 = Analysisstatus.objects.create(analysisstatus_name='analysisstatus_2')
        analysisstatus_3 = Analysisstatus.objects.create(analysisstatus_name='analysisstatus_3')
        systemstatus_1 = Systemstatus.objects.create(systemstatus_name='systemstatus_1')
        systemstatus_2 = Systemstatus.objects.create(systemstatus_name='systemstatus_2')
        systemstatus_3 = Systemstatus.objects.create(systemstatus_name='systemstatus_3')

        # create system (systemstatus and analysisstatus will be updated)
        System.objects.create(
            system_name = 'system_csv_34_001',
            systemstatus = systemstatus_1,
            analysisstatus = analysisstatus_1,
            system_modify_time = timezone.now(),
            system_created_by_user_id = test_user,
            system_modified_by_user_id = test_user,
        )
        # create system (systemstatus and analysisstatus won't be updated)
        system_34_2 = System.objects.create(
            system_name = 'system_csv_34_002',
            systemstatus = systemstatus_1,
            analysisstatus = analysisstatus_1,
            system_modify_time = timezone.now(),
            system_created_by_user_id = test_user,
            system_modified_by_user_id = test_user,
        )
        # create system (existing system - gets status 2 (because of tag))
        System.objects.create(
            system_name = 'system_csv_35_001',
            systemstatus = systemstatus_1,
            analysisstatus = analysisstatus_1,
            system_modify_time = timezone.now(),
            system_created_by_user_id = test_user,
            system_modified_by_user_id = test_user,
        )
        # create system (existing system - gets status 3 (because tagfree))
        System.objects.create(
            system_name = 'system_csv_35_002',
            systemstatus = systemstatus_1,
            analysisstatus = analysisstatus_1,
            system_modify_time = timezone.now(),
            system_created_by_user_id = test_user,
            system_modified_by_user_id = test_user,
        )
        # create system (existing system - keeps status 1 (because lock tag))
        system_35_3 = System.objects.create(
            system_name = 'system_csv_35_003',
            systemstatus = systemstatus_1,
            analysisstatus = analysisstatus_1,
            system_modify_time = timezone.now(),
            system_created_by_user_id = test_user,
            system_modified_by_user_id = test_user,
        )
        # create system (existing system - keeps status 1 (because lock tag))
        system_35_4 = System.objects.create(
            system_name = 'system_csv_35_004',
            systemstatus = systemstatus_1,
            analysisstatus = analysisstatus_1,
            system_modify_time = timezone.now(),
            system_created_by_user_id = test_user,
            system_modified_by_user_id = test_user,
        )

        # create lock tags
        tagcolor_1 = Tagcolor.objects.create(tagcolor_name='tagcolor_1')
        tag_lock_systemstatus = Tag.objects.create(
            tag_name = 'TEST_LOCK_SYSTEMSTATUS',
            tagcolor = tagcolor_1,
        )
        tag_lock_analysisstatus = Tag.objects.create(
            tag_name = 'TEST_LOCK_ANALYSISSTATUS',
            tagcolor = tagcolor_1,
        )

        # add lock tags to systems to prevent systemstatus and analysisstatus from updating
        system_34_2.tag.add(tag_lock_systemstatus)
        system_34_2.tag.add(tag_lock_analysisstatus)
        system_35_3.tag.add(tag_lock_systemstatus)
        system_35_3.tag.add(tag_lock_analysisstatus)
        system_35_4.tag.add(tag_lock_systemstatus)
        system_35_4.tag.add(tag_lock_analysisstatus)

        """ set config with fixed values """

        # build local path with test files
        csv_import_path = os.path.join(BASE_DIR, 'dfirtrack_main/tests/system_importer/system_importer_file_csv_files/')

        # set fixed config values
        system_importer_file_csv_config_model = SystemImporterFileCsvConfigModel.objects.get(system_importer_file_csv_config_name='SystemImporterFileCsvConfig')
        system_importer_file_csv_config_model.csv_column_system = 1
        system_importer_file_csv_config_model.csv_skip_existing_systems = False
        system_importer_file_csv_config_model.csv_headline = False
        system_importer_file_csv_config_model.csv_import_path = csv_import_path
        system_importer_file_csv_config_model.csv_import_username = test_user
        system_importer_file_csv_config_model.csv_default_systemstatus = systemstatus_2
        system_importer_file_csv_config_model.csv_remove_systemstatus = True
        system_importer_file_csv_config_model.csv_default_analysisstatus = analysisstatus_2
        system_importer_file_csv_config_model.csv_remove_analysisstatus = True
        system_importer_file_csv_config_model.csv_default_tagfree_systemstatus = systemstatus_3
        system_importer_file_csv_config_model.csv_default_tagfree_analysisstatus = analysisstatus_3
        system_importer_file_csv_config_model.csv_tag_lock_systemstatus = 'TEST_LOCK_SYSTEMSTATUS'
        system_importer_file_csv_config_model.csv_tag_lock_analysisstatus = 'TEST_LOCK_ANALYSISSTATUS'
        system_importer_file_csv_config_model.csv_field_delimiter = 'field_comma'
        system_importer_file_csv_config_model.csv_text_quote = 'text_double_quotation_marks'
        system_importer_file_csv_config_model.csv_ip_delimiter = 'ip_semicolon'
        system_importer_file_csv_config_model.csv_tag_delimiter = 'tag_space'

        # save config
        system_importer_file_csv_config_model.save()

    @classmethod
    def setUp(cls):
        """ setup in advance of every test """

        # get objects
        analysisstatus_1 = Analysisstatus.objects.get(analysisstatus_name='analysisstatus_1')
        systemstatus_1 = Systemstatus.objects.get(systemstatus_name='systemstatus_1')

        # reset systems
        system_34_1 = System.objects.get(system_name = 'system_csv_34_001')
        system_34_1.systemstatus = systemstatus_1
        system_34_1.analysisstatus = analysisstatus_1
        system_34_1.save()
        system_34_2 = System.objects.get(system_name = 'system_csv_34_002')
        system_34_2.systemstatus = systemstatus_1
        system_34_2.analysisstatus = analysisstatus_1
        system_34_2.save()
        system_35_1 = System.objects.get(system_name = 'system_csv_35_001')
        system_35_1.systemstatus = systemstatus_1
        system_35_1.analysisstatus = analysisstatus_1
        system_35_1.save()
        system_35_2 = System.objects.get(system_name = 'system_csv_35_002')
        system_35_2.systemstatus = systemstatus_1
        system_35_2.analysisstatus = analysisstatus_1
        system_35_2.save()
        system_35_3 = System.objects.get(system_name = 'system_csv_35_003')
        system_35_3.systemstatus = systemstatus_1
        system_35_3.analysisstatus = analysisstatus_1
        system_35_3.save()
        system_35_4 = System.objects.get(system_name = 'system_csv_35_004')
        system_35_4.systemstatus = systemstatus_1
        system_35_4.analysisstatus = analysisstatus_1
        system_35_4.save()

    """ lock status """

    def test_system_importer_file_csv_status_cron_lock_status(self):
        """ test importer view """

        # change config
        set_csv_import_filename('system_importer_file_csv_testfile_34_lock_status.csv')

        # mock timezone.now()
        t_1 = datetime(2021, 3, 11, 19, 5, tzinfo=timezone.utc)
        with patch.object(timezone, 'now', return_value=t_1):

            # execute cron job / scheduled task
            system_cron()

        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_status', password='Tsu0Q6SDhuxMH2APXMBT')
        # get response
        response = self.client.get('/system/')
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare - user 1
        self.assertEqual(str(response.context['user']), 'testuser_system_importer_file_csv_status')
        self.assertEqual(messages[0].message, 'System CSV importer: created: 1 | updated: 2 | skipped: 0 | multiple: 0 [2021-03-11 19:05:00 - 2021-03-11 19:05:00]')
        self.assertEqual(messages[0].level_tag, 'success')
        # switch user context
        self.client.logout()
        self.client.login(username='message_user', password='cwfOLfHnI33Y0g90gcN9')
        # get response
        response = self.client.get('/system/')
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare - user 2
        self.assertEqual(str(response.context['user']), 'message_user')
        self.assertEqual(messages[0].message, 'System CSV importer: created: 1 | updated: 2 | skipped: 0 | multiple: 0 [2021-03-11 19:05:00 - 2021-03-11 19:05:00]')
        self.assertEqual(messages[0].level_tag, 'success')
        # compare - systems / attributes
        self = compare_system_and_attributes_lock_status(self)

    def test_system_importer_file_csv_status_instant_lock_status(self):
        """ test importer view """

        # change config
        set_csv_import_filename('system_importer_file_csv_testfile_34_lock_status.csv')

        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_status', password='Tsu0Q6SDhuxMH2APXMBT')
        # create url
        destination = urllib.parse.quote('/system/', safe='/')
        # get response
        response = self.client.get('/system/importer/file/csv/instant/', follow=True)
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare - meta
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)
        # compare - messages
        self = compare_messages_lock_status(self, messages)
        # compare - systems / attributes
        self = compare_system_and_attributes_lock_status(self)

    def test_system_importer_file_csv_status_upload_post_lock_status(self):
        """ test importer view """

        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_status', password='Tsu0Q6SDhuxMH2APXMBT')
        # open upload file
        systemcsv = open(os.path.join(BASE_DIR, 'dfirtrack_main/tests/system_importer/system_importer_file_csv_files/system_importer_file_csv_testfile_34_lock_status.csv'), 'r')
        # create post data
        data_dict = {
            'systemcsv': systemcsv,
        }
        # create url
        destination = urllib.parse.quote('/system/', safe='/')
        # get response
        response = self.client.post('/system/importer/file/csv/upload/', data_dict)
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare - meta
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)
        # compare - messages
        self = compare_messages_lock_status(self, messages)
        # compare - systems / attributes
        self = compare_system_and_attributes_lock_status(self)
        # close file
        systemcsv.close()

    """ tagfree status """

    def test_system_importer_file_csv_status_cron_tagfree_status(self):
        """ test importer view """

        # change config
        set_csv_import_filename('system_importer_file_csv_testfile_35_tagfree_status.csv')
        # change config
        set_config_tagfree_status()

        # mock timezone.now()
        t_2 = datetime(2021, 3, 11, 19, 10, tzinfo=timezone.utc)
        with patch.object(timezone, 'now', return_value=t_2):

            # execute cron job / scheduled task
            system_cron()

        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_status', password='Tsu0Q6SDhuxMH2APXMBT')
        # get response
        response = self.client.get('/system/')
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare - user 1
        self.assertEqual(str(response.context['user']), 'testuser_system_importer_file_csv_status')
        self.assertEqual(messages[0].message, 'System CSV importer: created: 2 | updated: 4 | skipped: 0 | multiple: 0 [2021-03-11 19:10:00 - 2021-03-11 19:10:00]')
        self.assertEqual(messages[0].level_tag, 'success')
        # switch user context
        self.client.logout()
        self.client.login(username='message_user', password='cwfOLfHnI33Y0g90gcN9')
        # get response
        response = self.client.get('/system/')
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare - user 2
        self.assertEqual(str(response.context['user']), 'message_user')
        self.assertEqual(messages[0].message, 'System CSV importer: created: 2 | updated: 4 | skipped: 0 | multiple: 0 [2021-03-11 19:10:00 - 2021-03-11 19:10:00]')
        self.assertEqual(messages[0].level_tag, 'success')
        # compare - systems / attributes
        self = compare_system_and_attributes_tagfree_status(self)

    def test_system_importer_file_csv_status_instant_tagfree_status(self):
        """ test importer view """

        # change config
        set_csv_import_filename('system_importer_file_csv_testfile_35_tagfree_status.csv')
        # change config
        set_config_tagfree_status()

        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_status', password='Tsu0Q6SDhuxMH2APXMBT')
        # create url
        destination = urllib.parse.quote('/system/', safe='/')
        # get response
        response = self.client.get('/system/importer/file/csv/instant/', follow=True)
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare - meta
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)
        # compare - messages
        self = compare_messages_tagfree_status(self, messages)
        # compare - systems / attributes
        self = compare_system_and_attributes_tagfree_status(self)

    def test_system_importer_file_csv_status_upload_post_tagfree_status(self):
        """ test importer view """

        # change config
        set_config_tagfree_status()

        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_status', password='Tsu0Q6SDhuxMH2APXMBT')
        # open upload file
        systemcsv = open(os.path.join(BASE_DIR, 'dfirtrack_main/tests/system_importer/system_importer_file_csv_files/system_importer_file_csv_testfile_35_tagfree_status.csv'), 'r')
        # create post data
        data_dict = {
            'systemcsv': systemcsv,
        }
        # create url
        destination = urllib.parse.quote('/system/', safe='/')
        # get response
        response = self.client.post('/system/importer/file/csv/upload/', data_dict)
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare - meta
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)
        # compare - messages
        self = compare_messages_tagfree_status(self, messages)
        # compare - systems / attributes
        self = compare_system_and_attributes_tagfree_status(self)
        # close file
        systemcsv.close()
