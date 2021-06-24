from datetime import datetime
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.test import TestCase
from django.utils import timezone
from dfirtrack.settings import BASE_DIR
from dfirtrack_config.models import SystemImporterFileCsvConfigModel
from dfirtrack_main.importer.file.csv import system_cron
from dfirtrack_main.models import Analysisstatus, System, Systemstatus, Tag, Tagcolor
from dfirtrack_main.tests.system_importer.config_functions import set_config_tag_remove_all
from dfirtrack_main.tests.system_importer.config_functions import set_config_tag_remove_none
from dfirtrack_main.tests.system_importer.config_functions import set_config_tag_remove_prefix
from dfirtrack_main.tests.system_importer.config_functions import set_csv_import_filename
from dfirtrack_main.tests.system_importer.config_functions import set_csv_import_path
from mock import patch
import os
import urllib.parse


def compare_messages_csv(self, messages):
    """ compare messages """

    # compare - messages
    self.assertEqual(messages[0].message, '3 systems were updated.')
    self.assertEqual(messages[0].level_tag, 'success')

    # return to test function
    return self

def compare_tag_remove_all(self, file_number):
    """ compare tags """

    # compare - old tags (all removed)
    self.assertFalse(System.objects.get(system_name=f'system_csv_{file_number}_001').tag.filter(tag_name='AUTO_tag_96_1').exists())
    self.assertFalse(System.objects.get(system_name=f'system_csv_{file_number}_002').tag.filter(tag_name='AUTO_tag_96_1').exists())
    self.assertFalse(System.objects.get(system_name=f'system_csv_{file_number}_003').tag.filter(tag_name='AUTO_tag_96_1').exists())
    self.assertFalse(System.objects.get(system_name=f'system_csv_{file_number}_001').tag.filter(tag_name='tag_97_1').exists())
    self.assertFalse(System.objects.get(system_name=f'system_csv_{file_number}_002').tag.filter(tag_name='tag_97_1').exists())
    self.assertFalse(System.objects.get(system_name=f'system_csv_{file_number}_003').tag.filter(tag_name='tag_97_1').exists())

    # compare - existence of objects
    self.assertTrue(Tag.objects.filter(tag_name=f'AUTO_tag_{file_number}_1').exists())
    self.assertTrue(Tag.objects.filter(tag_name=f'AUTO_tag_{file_number}_2').exists())
    self.assertTrue(Tag.objects.filter(tag_name=f'AUTO_tag_{file_number}_3').exists())

    # compare - new tags
    self.assertTrue(System.objects.get(system_name=f'system_csv_{file_number}_001').tag.filter(tag_name=f'AUTO_tag_{file_number}_1').exists())
    self.assertTrue(System.objects.get(system_name=f'system_csv_{file_number}_001').tag.filter(tag_name=f'AUTO_tag_{file_number}_2').exists())
    self.assertTrue(System.objects.get(system_name=f'system_csv_{file_number}_001').tag.filter(tag_name=f'AUTO_tag_{file_number}_3').exists())
    self.assertTrue(System.objects.get(system_name=f'system_csv_{file_number}_002').tag.filter(tag_name=f'AUTO_tag_{file_number}_1').exists())
    self.assertTrue(System.objects.get(system_name=f'system_csv_{file_number}_002').tag.filter(tag_name=f'AUTO_tag_{file_number}_2').exists())
    self.assertTrue(System.objects.get(system_name=f'system_csv_{file_number}_002').tag.filter(tag_name=f'AUTO_tag_{file_number}_3').exists())
    self.assertTrue(System.objects.get(system_name=f'system_csv_{file_number}_003').tag.filter(tag_name=f'AUTO_tag_{file_number}_1').exists())
    self.assertTrue(System.objects.get(system_name=f'system_csv_{file_number}_003').tag.filter(tag_name=f'AUTO_tag_{file_number}_2').exists())
    self.assertTrue(System.objects.get(system_name=f'system_csv_{file_number}_003').tag.filter(tag_name=f'AUTO_tag_{file_number}_3').exists())

    # return to test function
    return self

def compare_tag_remove_prefix(self, file_number):
    """ compare tags """

    # compare - old tags (with prefix removed)
    self.assertFalse(System.objects.get(system_name=f'system_csv_{file_number}_001').tag.filter(tag_name='AUTO_tag_96_1').exists())
    self.assertFalse(System.objects.get(system_name=f'system_csv_{file_number}_002').tag.filter(tag_name='AUTO_tag_96_1').exists())
    self.assertFalse(System.objects.get(system_name=f'system_csv_{file_number}_003').tag.filter(tag_name='AUTO_tag_96_1').exists())
    self.assertTrue(System.objects.get(system_name=f'system_csv_{file_number}_001').tag.filter(tag_name='tag_97_1').exists())
    self.assertTrue(System.objects.get(system_name=f'system_csv_{file_number}_002').tag.filter(tag_name='tag_97_1').exists())
    self.assertTrue(System.objects.get(system_name=f'system_csv_{file_number}_003').tag.filter(tag_name='tag_97_1').exists())

    # compare - existence of objects
    self.assertTrue(Tag.objects.filter(tag_name=f'AUTO_tag_{file_number}_1').exists())
    self.assertTrue(Tag.objects.filter(tag_name=f'AUTO_tag_{file_number}_2').exists())
    self.assertTrue(Tag.objects.filter(tag_name=f'AUTO_tag_{file_number}_3').exists())

    # compare - new tags
    self.assertTrue(System.objects.get(system_name=f'system_csv_{file_number}_001').tag.filter(tag_name=f'AUTO_tag_{file_number}_1').exists())
    self.assertTrue(System.objects.get(system_name=f'system_csv_{file_number}_001').tag.filter(tag_name=f'AUTO_tag_{file_number}_2').exists())
    self.assertTrue(System.objects.get(system_name=f'system_csv_{file_number}_001').tag.filter(tag_name=f'AUTO_tag_{file_number}_3').exists())
    self.assertTrue(System.objects.get(system_name=f'system_csv_{file_number}_002').tag.filter(tag_name=f'AUTO_tag_{file_number}_1').exists())
    self.assertTrue(System.objects.get(system_name=f'system_csv_{file_number}_002').tag.filter(tag_name=f'AUTO_tag_{file_number}_2').exists())
    self.assertTrue(System.objects.get(system_name=f'system_csv_{file_number}_002').tag.filter(tag_name=f'AUTO_tag_{file_number}_3').exists())
    self.assertTrue(System.objects.get(system_name=f'system_csv_{file_number}_003').tag.filter(tag_name=f'AUTO_tag_{file_number}_1').exists())
    self.assertTrue(System.objects.get(system_name=f'system_csv_{file_number}_003').tag.filter(tag_name=f'AUTO_tag_{file_number}_2').exists())
    self.assertTrue(System.objects.get(system_name=f'system_csv_{file_number}_003').tag.filter(tag_name=f'AUTO_tag_{file_number}_3').exists())

    # return to test function
    return self

def compare_tag_remove_none(self, file_number):
    """ compare tags """

    # compare - old tags (no tag removed)
    self.assertTrue(System.objects.get(system_name=f'system_csv_{file_number}_001').tag.filter(tag_name='AUTO_tag_96_1').exists())
    self.assertTrue(System.objects.get(system_name=f'system_csv_{file_number}_002').tag.filter(tag_name='AUTO_tag_96_1').exists())
    self.assertTrue(System.objects.get(system_name=f'system_csv_{file_number}_003').tag.filter(tag_name='AUTO_tag_96_1').exists())
    self.assertTrue(System.objects.get(system_name=f'system_csv_{file_number}_001').tag.filter(tag_name='tag_97_1').exists())
    self.assertTrue(System.objects.get(system_name=f'system_csv_{file_number}_002').tag.filter(tag_name='tag_97_1').exists())
    self.assertTrue(System.objects.get(system_name=f'system_csv_{file_number}_003').tag.filter(tag_name='tag_97_1').exists())

    # compare - new tags (no tag created)
    self.assertFalse(Tag.objects.filter(tag_name=f'AUTO_tag_{file_number}_1').exists())
    self.assertFalse(Tag.objects.filter(tag_name=f'AUTO_tag_{file_number}_2').exists())
    self.assertFalse(Tag.objects.filter(tag_name=f'AUTO_tag_{file_number}_3').exists())

    # return to test function
    return self

class SystemImporterFileCsvTagRemovalViewTestCase(TestCase):
    """ system importer file CSV view tests """

    @classmethod
    def setUpTestData(cls):
        """ one-time setup """

        # create user
        test_user = User.objects.create_user(username='testuser_system_importer_file_csv_tag_removal', password='XAavYL75MrC5eVVSuzoL')
        User.objects.create_user(username='message_user', password='8vwuoDthBxFkMQUBG2DM')

        # create objects
        analysisstatus_1 = Analysisstatus.objects.create(analysisstatus_name='analysisstatus_1')
        analysisstatus_2 = Analysisstatus.objects.create(analysisstatus_name='analysisstatus_2')
        systemstatus_1 = Systemstatus.objects.create(systemstatus_name='systemstatus_1')
        systemstatus_2 = Systemstatus.objects.create(systemstatus_name='systemstatus_2')

        # create systems
        system_csv_56_001 = System.objects.create(
            system_name = 'system_csv_56_001',
            systemstatus = systemstatus_1,
            analysisstatus = analysisstatus_1,
            system_modify_time = timezone.now(),
            system_created_by_user_id = test_user,
            system_modified_by_user_id = test_user,
        )
        system_csv_56_002 = System.objects.create(
            system_name = 'system_csv_56_002',
            systemstatus = systemstatus_1,
            analysisstatus = analysisstatus_1,
            system_modify_time = timezone.now(),
            system_created_by_user_id = test_user,
            system_modified_by_user_id = test_user,
        )
        system_csv_56_003 = System.objects.create(
            system_name = 'system_csv_56_003',
            systemstatus = systemstatus_1,
            analysisstatus = analysisstatus_1,
            system_modify_time = timezone.now(),
            system_created_by_user_id = test_user,
            system_modified_by_user_id = test_user,
        )

        tagcolor_1 = Tagcolor.objects.create(tagcolor_name='tagcolor_1')
        AUTO_tag_96_1 = Tag.objects.create(
            tag_name='AUTO_tag_96_1',
            tagcolor=tagcolor_1,
        )
        tag_97_1 = Tag.objects.create(
            tag_name='tag_97_1',
            tagcolor=tagcolor_1,
        )

        system_csv_56_001.tag.add(AUTO_tag_96_1)
        system_csv_56_002.tag.add(AUTO_tag_96_1)
        system_csv_56_003.tag.add(AUTO_tag_96_1)
        system_csv_56_001.tag.add(tag_97_1)
        system_csv_56_002.tag.add(tag_97_1)
        system_csv_56_003.tag.add(tag_97_1)

        # set config
        set_csv_import_path(os.path.join(BASE_DIR, 'dfirtrack_main/tests/system_importer/system_importer_file_csv_files/'))

        # set config
        set_csv_import_filename('system_importer_file_csv_testfile_56_tag_delimiter_space.csv')

        # set config
        system_importer_file_csv_config_model = SystemImporterFileCsvConfigModel.objects.get(system_importer_file_csv_config_name='SystemImporterFileCsvConfig')
        system_importer_file_csv_config_model.csv_column_system = 1
        system_importer_file_csv_config_model.csv_skip_existing_system = False
        system_importer_file_csv_config_model.csv_headline = False
        system_importer_file_csv_config_model.csv_import_username = test_user
        system_importer_file_csv_config_model.csv_default_systemstatus = systemstatus_1
        system_importer_file_csv_config_model.csv_default_analysisstatus = analysisstatus_1
        system_importer_file_csv_config_model.csv_default_tagfree_systemstatus = systemstatus_2
        system_importer_file_csv_config_model.csv_default_tagfree_analysisstatus = analysisstatus_2
        system_importer_file_csv_config_model.csv_tag_lock_systemstatus = 'LOCK_SYSTEMSTATUS'
        system_importer_file_csv_config_model.csv_tag_lock_analysisstatus = 'LOCK_ANALYSISSTATUS'
        system_importer_file_csv_config_model.csv_field_delimiter = 'field_comma'
        system_importer_file_csv_config_model.csv_text_quote = 'text_double_quotation_marks'
        system_importer_file_csv_config_model.csv_ip_delimiter = 'ip_semicolon'
        system_importer_file_csv_config_model.csv_tag_delimiter = 'tag_space'
        system_importer_file_csv_config_model.csv_tag_prefix = 'AUTO'
        system_importer_file_csv_config_model.csv_tag_prefix_delimiter = 'tag_prefix_underscore'
        system_importer_file_csv_config_model.csv_choice_tag = True
        system_importer_file_csv_config_model.csv_column_tag = 2
        system_importer_file_csv_config_model.save()

    """ remove all tags """

    def test_system_importer_file_csv_cron_tag_remove_all(self):
        """ test importer view """

        # change config
        set_config_tag_remove_all()

        # mock timezone.now()
        t_1 = datetime(2021, 3, 26, 18, 35, tzinfo=timezone.utc)
        with patch.object(timezone, 'now', return_value=t_1):

            # execute cron job / scheduled task
            system_cron()

        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_tag_removal', password='XAavYL75MrC5eVVSuzoL')
        # get response
        response = self.client.get('/system/')
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare - user 1
        self.assertEqual(str(response.context['user']), 'testuser_system_importer_file_csv_tag_removal')
        self.assertEqual(messages[0].message, 'System CSV importer: created: 0 | updated: 3 | skipped: 0 | multiple: 0 [2021-03-26 18:35:00 - 2021-03-26 18:35:00]')
        self.assertEqual(messages[0].level_tag, 'success')
        # switch user context
        self.client.logout()
        self.client.login(username='message_user', password='8vwuoDthBxFkMQUBG2DM')
        # get response
        response = self.client.get('/system/')
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare - user 2
        self.assertEqual(str(response.context['user']), 'message_user')
        self.assertEqual(messages[0].message, 'System CSV importer: created: 0 | updated: 3 | skipped: 0 | multiple: 0 [2021-03-26 18:35:00 - 2021-03-26 18:35:00]')
        self.assertEqual(messages[0].level_tag, 'success')
        # compare - tags
        compare_tag_remove_all(self, '56')

    def test_system_importer_file_csv_instant_tag_remove_all(self):
        """ test importer view """

        # change config
        set_config_tag_remove_all()

        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_tag_removal', password='XAavYL75MrC5eVVSuzoL')
        # create url
        destination = urllib.parse.quote('/system/', safe='/')
        # get response
        response = self.client.get('/system/importer/file/csv/instant/', follow=True)
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare - meta
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)
        # compare - messages
        compare_messages_csv(self, messages)
        # compare - tags
        compare_tag_remove_all(self, '56')

    def test_system_importer_file_csv_upload_post_tag_remove_all(self):
        """ test importer view """

        # change config
        set_config_tag_remove_all()

        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_tag_removal', password='XAavYL75MrC5eVVSuzoL')
        # open upload file
        systemcsv = open(os.path.join(BASE_DIR, 'dfirtrack_main/tests/system_importer/system_importer_file_csv_files/system_importer_file_csv_testfile_56_tag_delimiter_space.csv'), 'r')
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
        # close file
        systemcsv.close()
        # compare - meta
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)
        # compare - messages
        compare_messages_csv(self, messages)
        # compare - tags
        compare_tag_remove_all(self, '56')

    """ remove prefix tags """

    def test_system_importer_file_csv_cron_tag_remove_prefix(self):
        """ test importer view """

        # change config
        set_config_tag_remove_prefix()

        # mock timezone.now()
        t_2 = datetime(2021, 3, 26, 18, 40, tzinfo=timezone.utc)
        with patch.object(timezone, 'now', return_value=t_2):

            # execute cron job / scheduled task
            system_cron()

        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_tag_removal', password='XAavYL75MrC5eVVSuzoL')
        # get response
        response = self.client.get('/system/')
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare - user 1
        self.assertEqual(str(response.context['user']), 'testuser_system_importer_file_csv_tag_removal')
        self.assertEqual(messages[0].message, 'System CSV importer: created: 0 | updated: 3 | skipped: 0 | multiple: 0 [2021-03-26 18:40:00 - 2021-03-26 18:40:00]')
        self.assertEqual(messages[0].level_tag, 'success')
        # switch user context
        self.client.logout()
        self.client.login(username='message_user', password='8vwuoDthBxFkMQUBG2DM')
        # get response
        response = self.client.get('/system/')
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare - user 2
        self.assertEqual(str(response.context['user']), 'message_user')
        self.assertEqual(messages[0].message, 'System CSV importer: created: 0 | updated: 3 | skipped: 0 | multiple: 0 [2021-03-26 18:40:00 - 2021-03-26 18:40:00]')
        self.assertEqual(messages[0].level_tag, 'success')
        # compare - tags
        compare_tag_remove_prefix(self, '56')

    def test_system_importer_file_csv_instant_tag_remove_prefix(self):
        """ test importer view """

        # change config
        set_config_tag_remove_prefix()

        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_tag_removal', password='XAavYL75MrC5eVVSuzoL')
        # create url
        destination = urllib.parse.quote('/system/', safe='/')
        # get response
        response = self.client.get('/system/importer/file/csv/instant/', follow=True)
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare - meta
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)
        # compare - messages
        compare_messages_csv(self, messages)
        # compare - tags
        compare_tag_remove_prefix(self, '56')

    def test_system_importer_file_csv_upload_post_tag_remove_prefix(self):
        """ test importer view """

        # change config
        set_config_tag_remove_prefix()

        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_tag_removal', password='XAavYL75MrC5eVVSuzoL')
        # open upload file
        systemcsv = open(os.path.join(BASE_DIR, 'dfirtrack_main/tests/system_importer/system_importer_file_csv_files/system_importer_file_csv_testfile_56_tag_delimiter_space.csv'), 'r')
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
        # close file
        systemcsv.close()
        # compare - meta
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)
        # compare - messages
        compare_messages_csv(self, messages)
        # compare - tags
        compare_tag_remove_prefix(self, '56')

    """ remove no tags """

    def test_system_importer_file_csv_cron_tag_remove_none(self):
        """ test importer view """

        # change config
        set_config_tag_remove_none()

        # mock timezone.now()
        t_3 = datetime(2021, 3, 26, 18, 45, tzinfo=timezone.utc)
        with patch.object(timezone, 'now', return_value=t_3):

            # execute cron job / scheduled task
            system_cron()

        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_tag_removal', password='XAavYL75MrC5eVVSuzoL')
        # get response
        response = self.client.get('/system/')
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare - user 1
        self.assertEqual(str(response.context['user']), 'testuser_system_importer_file_csv_tag_removal')
        self.assertEqual(messages[0].message, 'System CSV importer: created: 0 | updated: 3 | skipped: 0 | multiple: 0 [2021-03-26 18:45:00 - 2021-03-26 18:45:00]')
        self.assertEqual(messages[0].level_tag, 'success')
        # switch user context
        self.client.logout()
        self.client.login(username='message_user', password='8vwuoDthBxFkMQUBG2DM')
        # get response
        response = self.client.get('/system/')
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare - user 2
        self.assertEqual(str(response.context['user']), 'message_user')
        self.assertEqual(messages[0].message, 'System CSV importer: created: 0 | updated: 3 | skipped: 0 | multiple: 0 [2021-03-26 18:45:00 - 2021-03-26 18:45:00]')
        self.assertEqual(messages[0].level_tag, 'success')
        # compare - tags
        compare_tag_remove_none(self, '56')

    def test_system_importer_file_csv_instant_tag_remove_none(self):
        """ test importer view """

        # change config
        set_config_tag_remove_none()

        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_tag_removal', password='XAavYL75MrC5eVVSuzoL')
        # create url
        destination = urllib.parse.quote('/system/', safe='/')
        # get response
        response = self.client.get('/system/importer/file/csv/instant/', follow=True)
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare - meta
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)
        # compare - messages
        compare_messages_csv(self, messages)
        # compare - tags
        compare_tag_remove_none(self, '56')

    def test_system_importer_file_csv_upload_post_tag_remove_none(self):
        """ test importer view """

        # change config
        set_config_tag_remove_none()

        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_tag_removal', password='XAavYL75MrC5eVVSuzoL')
        # open upload file
        systemcsv = open(os.path.join(BASE_DIR, 'dfirtrack_main/tests/system_importer/system_importer_file_csv_files/system_importer_file_csv_testfile_56_tag_delimiter_space.csv'), 'r')
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
        # close file
        systemcsv.close()
        # compare - meta
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)
        # compare - messages
        compare_messages_csv(self, messages)
        # compare - tags
        compare_tag_remove_none(self, '56')
