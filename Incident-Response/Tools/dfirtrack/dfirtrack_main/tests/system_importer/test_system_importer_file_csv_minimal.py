from datetime import datetime
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.test import TestCase
from django.utils import timezone
from dfirtrack.settings import BASE_DIR
from dfirtrack_config.models import SystemImporterFileCsvConfigModel
from dfirtrack_main.importer.file.csv import system_cron
from dfirtrack_main.models import Analysisstatus, Domain, Ip, System, Systemstatus, Tag
from dfirtrack_main.tests.system_importer.config_functions import set_config_field_delimiter_comma
from dfirtrack_main.tests.system_importer.config_functions import set_config_field_delimiter_semicolon
from dfirtrack_main.tests.system_importer.config_functions import set_config_headline
from dfirtrack_main.tests.system_importer.config_functions import set_config_ip_delimiter_comma
from dfirtrack_main.tests.system_importer.config_functions import set_config_ip_delimiter_semicolon
from dfirtrack_main.tests.system_importer.config_functions import set_config_ip_delimiter_space
from dfirtrack_main.tests.system_importer.config_functions import set_config_single_quotation
from dfirtrack_main.tests.system_importer.config_functions import set_config_tag_delimiter_comma
from dfirtrack_main.tests.system_importer.config_functions import set_config_tag_delimiter_semicolon
from dfirtrack_main.tests.system_importer.config_functions import set_config_tag_delimiter_space
from dfirtrack_main.tests.system_importer.config_functions import set_config_tag_prefix_delimiter_hyphen
from dfirtrack_main.tests.system_importer.config_functions import set_config_tag_prefix_delimiter_period
from dfirtrack_main.tests.system_importer.config_functions import set_config_tag_prefix_delimiter_underscore
from dfirtrack_main.tests.system_importer.config_functions import set_csv_import_filename
from dfirtrack_main.tests.system_importer.config_functions import set_csv_import_path
from mock import patch
import os
import urllib.parse


def compare_messages_csv(self, messages):
    """ compare messages """

    # compare - messages
    self.assertEqual(messages[0].message, '3 systems were created.')
    self.assertEqual(messages[0].level_tag, 'success')

    # return to test function
    return self

def compare_system_and_attributes_csv(self, file_number):
    """ compare systems and associated attributes """

    # get objects
    analysisstatus_1 = Analysisstatus.objects.get(analysisstatus_name='analysisstatus_1')
    systemstatus_1 = Systemstatus.objects.get(systemstatus_name='systemstatus_1')

    # compare - existence of objects
    self.assertTrue(System.objects.filter(system_name=f'system_csv_{file_number}_001').exists())
    self.assertTrue(System.objects.filter(system_name=f'system_csv_{file_number}_002').exists())
    self.assertTrue(System.objects.filter(system_name=f'system_csv_{file_number}_003').exists())
    self.assertEqual(System.objects.get(system_name=f'system_csv_{file_number}_001').analysisstatus, analysisstatus_1)
    self.assertEqual(System.objects.get(system_name=f'system_csv_{file_number}_002').analysisstatus, analysisstatus_1)
    self.assertEqual(System.objects.get(system_name=f'system_csv_{file_number}_003').analysisstatus, analysisstatus_1)
    self.assertEqual(System.objects.get(system_name=f'system_csv_{file_number}_001').systemstatus, systemstatus_1)
    self.assertEqual(System.objects.get(system_name=f'system_csv_{file_number}_002').systemstatus, systemstatus_1)
    self.assertEqual(System.objects.get(system_name=f'system_csv_{file_number}_003').systemstatus, systemstatus_1)

    # return to test function
    return self

def compare_delimiter_specific(self, file_number):
    """ compare delimiter specific results  """

    # compare domain (delimiter specific)
    self.assertTrue(Domain.objects.filter(domain_name=f'domain_{file_number}_1').exists())
    domain_1 = Domain.objects.get(domain_name=f'domain_{file_number}_1')
    self.assertEqual(System.objects.get(system_name=f'system_csv_{file_number}_001').domain, domain_1)
    self.assertEqual(System.objects.get(system_name=f'system_csv_{file_number}_002').domain, domain_1)
    self.assertEqual(System.objects.get(system_name=f'system_csv_{file_number}_003').domain, domain_1)

    # return to test function
    return self

def compare_ips(self, file_number):
    """ compare systems and associated attributes """

    # compare - existence of objects
    self.assertTrue(Ip.objects.filter(ip_ip=f'127.{file_number}.1.1').exists())
    self.assertTrue(Ip.objects.filter(ip_ip=f'127.{file_number}.1.2').exists())
    self.assertTrue(Ip.objects.filter(ip_ip=f'127.{file_number}.1.3').exists())
    self.assertTrue(Ip.objects.filter(ip_ip=f'127.{file_number}.2.1').exists())
    self.assertTrue(Ip.objects.filter(ip_ip=f'127.{file_number}.2.2').exists())
    self.assertTrue(Ip.objects.filter(ip_ip=f'127.{file_number}.2.3').exists())
    self.assertTrue(Ip.objects.filter(ip_ip=f'127.{file_number}.3.1').exists())
    self.assertTrue(Ip.objects.filter(ip_ip=f'127.{file_number}.3.2').exists())
    self.assertTrue(Ip.objects.filter(ip_ip=f'127.{file_number}.3.3').exists())

    # compare - existence of objects
    self.assertTrue(System.objects.get(system_name=f'system_csv_{file_number}_001').ip.filter(ip_ip=f'127.{file_number}.1.1').exists())
    self.assertTrue(System.objects.get(system_name=f'system_csv_{file_number}_001').ip.filter(ip_ip=f'127.{file_number}.1.2').exists())
    self.assertTrue(System.objects.get(system_name=f'system_csv_{file_number}_001').ip.filter(ip_ip=f'127.{file_number}.1.3').exists())
    self.assertTrue(System.objects.get(system_name=f'system_csv_{file_number}_002').ip.filter(ip_ip=f'127.{file_number}.2.1').exists())
    self.assertTrue(System.objects.get(system_name=f'system_csv_{file_number}_002').ip.filter(ip_ip=f'127.{file_number}.2.2').exists())
    self.assertTrue(System.objects.get(system_name=f'system_csv_{file_number}_002').ip.filter(ip_ip=f'127.{file_number}.2.3').exists())
    self.assertTrue(System.objects.get(system_name=f'system_csv_{file_number}_003').ip.filter(ip_ip=f'127.{file_number}.3.1').exists())
    self.assertTrue(System.objects.get(system_name=f'system_csv_{file_number}_003').ip.filter(ip_ip=f'127.{file_number}.3.2').exists())
    self.assertTrue(System.objects.get(system_name=f'system_csv_{file_number}_003').ip.filter(ip_ip=f'127.{file_number}.3.3').exists())

    # return to test function
    return self

def compare_tags(self, file_number, delimiter):
    """ compare systems and associated attributes """

    # compare - existence of objects
    self.assertTrue(Tag.objects.filter(tag_name=f'AUTO{delimiter}tag_{file_number}_1').exists())
    self.assertTrue(Tag.objects.filter(tag_name=f'AUTO{delimiter}tag_{file_number}_2').exists())
    self.assertTrue(Tag.objects.filter(tag_name=f'AUTO{delimiter}tag_{file_number}_3').exists())

    # compare - existence of objects
    self.assertTrue(System.objects.get(system_name=f'system_csv_{file_number}_001').tag.filter(tag_name=f'AUTO{delimiter}tag_{file_number}_1').exists())
    self.assertTrue(System.objects.get(system_name=f'system_csv_{file_number}_001').tag.filter(tag_name=f'AUTO{delimiter}tag_{file_number}_2').exists())
    self.assertTrue(System.objects.get(system_name=f'system_csv_{file_number}_001').tag.filter(tag_name=f'AUTO{delimiter}tag_{file_number}_3').exists())
    self.assertTrue(System.objects.get(system_name=f'system_csv_{file_number}_002').tag.filter(tag_name=f'AUTO{delimiter}tag_{file_number}_1').exists())
    self.assertTrue(System.objects.get(system_name=f'system_csv_{file_number}_002').tag.filter(tag_name=f'AUTO{delimiter}tag_{file_number}_2').exists())
    self.assertTrue(System.objects.get(system_name=f'system_csv_{file_number}_002').tag.filter(tag_name=f'AUTO{delimiter}tag_{file_number}_3').exists())
    self.assertTrue(System.objects.get(system_name=f'system_csv_{file_number}_003').tag.filter(tag_name=f'AUTO{delimiter}tag_{file_number}_1').exists())
    self.assertTrue(System.objects.get(system_name=f'system_csv_{file_number}_003').tag.filter(tag_name=f'AUTO{delimiter}tag_{file_number}_2').exists())
    self.assertTrue(System.objects.get(system_name=f'system_csv_{file_number}_003').tag.filter(tag_name=f'AUTO{delimiter}tag_{file_number}_3').exists())

    # return to test function
    return self

class SystemImporterFileCsvMinimalViewTestCase(TestCase):
    """ system importer file CSV view tests """

    @classmethod
    def setUpTestData(cls):
        """ one-time setup """

        # create user
        test_user = User.objects.create_user(username='testuser_system_importer_file_csv_minimal', password='H6mM7kq9sEZLvm6CyOaW')
        User.objects.create_user(username='message_user', password='UFPntl9kU9vYkXwAo9SS')

        # create objects
        analysisstatus_1 = Analysisstatus.objects.create(analysisstatus_name='analysisstatus_1')
        analysisstatus_2 = Analysisstatus.objects.create(analysisstatus_name='analysisstatus_2')
        systemstatus_1 = Systemstatus.objects.create(systemstatus_name='systemstatus_1')
        systemstatus_2 = Systemstatus.objects.create(systemstatus_name='systemstatus_2')

        # build local path with test files
        set_csv_import_path(os.path.join(BASE_DIR, 'dfirtrack_main/tests/system_importer/system_importer_file_csv_files/'))

        # change config
        system_importer_file_csv_config_model = SystemImporterFileCsvConfigModel.objects.get(system_importer_file_csv_config_name='SystemImporterFileCsvConfig')
        system_importer_file_csv_config_model.csv_column_system = 1
        system_importer_file_csv_config_model.csv_skip_existing_system = True
        system_importer_file_csv_config_model.csv_headline = False
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

    """ text quote - double quotation """

    def test_system_importer_file_csv_cron_minimal_double_quotation(self):
        """ test importer view """

        # change config
        set_csv_import_filename('system_importer_file_csv_testfile_01_minimal_double_quotation.csv')

        # mock timezone.now()
        t_1 = datetime(2021, 3, 6, 17, 28, tzinfo=timezone.utc)
        with patch.object(timezone, 'now', return_value=t_1):

            # execute cron job / scheduled task
            system_cron()

        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_minimal', password='H6mM7kq9sEZLvm6CyOaW')
        # get response
        response = self.client.get('/system/')
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare - user 1
        self.assertEqual(str(response.context['user']), 'testuser_system_importer_file_csv_minimal')
        self.assertEqual(messages[0].message, 'System CSV importer: created: 3 | updated: 0 | skipped: 0 | multiple: 0 [2021-03-06 17:28:00 - 2021-03-06 17:28:00]')
        self.assertEqual(messages[0].level_tag, 'success')
        # switch user context
        self.client.logout()
        self.client.login(username='message_user', password='UFPntl9kU9vYkXwAo9SS')
        # get response
        response = self.client.get('/system/')
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare - user 2
        self.assertEqual(str(response.context['user']), 'message_user')
        self.assertEqual(messages[0].message, 'System CSV importer: created: 3 | updated: 0 | skipped: 0 | multiple: 0 [2021-03-06 17:28:00 - 2021-03-06 17:28:00]')
        self.assertEqual(messages[0].level_tag, 'success')
        # compare - systems / attributes
        compare_system_and_attributes_csv(self, '01')

    def test_system_importer_file_csv_instant_minimal_double_quotation(self):
        """ test importer view """

        # change config
        set_csv_import_filename('system_importer_file_csv_testfile_01_minimal_double_quotation.csv')

        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_minimal', password='H6mM7kq9sEZLvm6CyOaW')
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
        # compare - systems / attributes
        compare_system_and_attributes_csv(self, '01')

    def test_system_importer_file_csv_upload_post_minimal_double_quotation(self):
        """ test importer view """

        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_minimal', password='H6mM7kq9sEZLvm6CyOaW')
        # open upload file
        systemcsv = open(os.path.join(BASE_DIR, 'dfirtrack_main/tests/system_importer/system_importer_file_csv_files/system_importer_file_csv_testfile_01_minimal_double_quotation.csv'), 'r')
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
        # compare - systems / attributes
        compare_system_and_attributes_csv(self, '01')

    """ text quote - single quotation """

    def test_system_importer_file_csv_cron_minimal_single_quotation(self):
        """ test importer view """

        # change config
        set_csv_import_filename('system_importer_file_csv_testfile_02_minimal_single_quotation.csv')
        # change config
        set_config_single_quotation()

        # mock timezone.now()
        t_2 = datetime(2021, 3, 6, 17, 55, tzinfo=timezone.utc)
        with patch.object(timezone, 'now', return_value=t_2):

            # execute cron job / scheduled task
            system_cron()

        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_minimal', password='H6mM7kq9sEZLvm6CyOaW')
        # get response
        response = self.client.get('/system/')
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare - user 1
        self.assertEqual(str(response.context['user']), 'testuser_system_importer_file_csv_minimal')
        self.assertEqual(messages[0].message, 'System CSV importer: created: 3 | updated: 0 | skipped: 0 | multiple: 0 [2021-03-06 17:55:00 - 2021-03-06 17:55:00]')
        self.assertEqual(messages[0].level_tag, 'success')
        # switch user context
        self.client.logout()
        self.client.login(username='message_user', password='UFPntl9kU9vYkXwAo9SS')
        # get response
        response = self.client.get('/system/')
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare - user 2
        self.assertEqual(str(response.context['user']), 'message_user')
        self.assertEqual(messages[0].message, 'System CSV importer: created: 3 | updated: 0 | skipped: 0 | multiple: 0 [2021-03-06 17:55:00 - 2021-03-06 17:55:00]')
        self.assertEqual(messages[0].level_tag, 'success')
        # compare - systems / attributes
        compare_system_and_attributes_csv(self, '02')

    def test_system_importer_file_csv_instant_minimal_single_quotation(self):
        """ test importer view """

        # change config
        set_csv_import_filename('system_importer_file_csv_testfile_02_minimal_single_quotation.csv')
        # change config
        set_config_single_quotation()

        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_minimal', password='H6mM7kq9sEZLvm6CyOaW')
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
        # compare - systems / attributes
        compare_system_and_attributes_csv(self, '02')

    def test_system_importer_file_csv_upload_post_minimal_single_quotation(self):
        """ test importer view """

        # change config
        set_config_single_quotation()

        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_minimal', password='H6mM7kq9sEZLvm6CyOaW')
        # open upload file
        systemcsv = open(os.path.join(BASE_DIR, 'dfirtrack_main/tests/system_importer/system_importer_file_csv_files/system_importer_file_csv_testfile_02_minimal_single_quotation.csv'), 'r')
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
        # compare - systems / attributes
        compare_system_and_attributes_csv(self, '02')

    """ headline """

    def test_system_importer_file_csv_cron_minimal_headline(self):
        """ test importer view """

        # change config
        set_csv_import_filename('system_importer_file_csv_testfile_03_minimal_headline.csv')
        # change config
        set_config_headline()

        # mock timezone.now()
        t_3 = datetime(2021, 3, 6, 18, 7, tzinfo=timezone.utc)
        with patch.object(timezone, 'now', return_value=t_3):

            # execute cron job / scheduled task
            system_cron()

        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_minimal', password='H6mM7kq9sEZLvm6CyOaW')
        # get response
        response = self.client.get('/system/')
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare - user 1
        self.assertEqual(str(response.context['user']), 'testuser_system_importer_file_csv_minimal')
        self.assertEqual(messages[0].message, 'System CSV importer: created: 3 | updated: 0 | skipped: 0 | multiple: 0 [2021-03-06 18:07:00 - 2021-03-06 18:07:00]')
        self.assertEqual(messages[0].level_tag, 'success')
        # switch user context
        self.client.logout()
        self.client.login(username='message_user', password='UFPntl9kU9vYkXwAo9SS')
        # get response
        response = self.client.get('/system/')
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare - user 2
        self.assertEqual(str(response.context['user']), 'message_user')
        self.assertEqual(messages[0].message, 'System CSV importer: created: 3 | updated: 0 | skipped: 0 | multiple: 0 [2021-03-06 18:07:00 - 2021-03-06 18:07:00]')
        self.assertEqual(messages[0].level_tag, 'success')
        # compare - systems / attributes
        compare_system_and_attributes_csv(self, '03')

    def test_system_importer_file_csv_instant_minimal_headline(self):
        """ test importer view """

        # change config
        set_csv_import_filename('system_importer_file_csv_testfile_03_minimal_headline.csv')
        # change config
        set_config_headline()

        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_minimal', password='H6mM7kq9sEZLvm6CyOaW')
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
        # compare - systems / attributes
        compare_system_and_attributes_csv(self, '03')

    def test_system_importer_file_csv_upload_post_minimal_headline(self):
        """ test importer view """

        # change config
        set_config_headline()

        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_minimal', password='H6mM7kq9sEZLvm6CyOaW')
        # open upload file
        systemcsv = open(os.path.join(BASE_DIR, 'dfirtrack_main/tests/system_importer/system_importer_file_csv_files/system_importer_file_csv_testfile_03_minimal_headline.csv'), 'r')
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
        # compare - systems / attributes
        compare_system_and_attributes_csv(self, '03')

    """ field delimiter - comma """

    def test_system_importer_file_csv_cron_minimal_comma(self):
        """ test importer view """

        # change config
        set_csv_import_filename('system_importer_file_csv_testfile_21_minimal_comma.csv')
        # change config
        set_config_field_delimiter_comma()

        # mock timezone.now()
        t_5 = datetime(2021, 3, 7, 21, 12, tzinfo=timezone.utc)
        with patch.object(timezone, 'now', return_value=t_5):

            # execute cron job / scheduled task
            system_cron()

        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_minimal', password='H6mM7kq9sEZLvm6CyOaW')
        # get response
        response = self.client.get('/system/')
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare - user 1
        self.assertEqual(str(response.context['user']), 'testuser_system_importer_file_csv_minimal')
        self.assertEqual(messages[0].message, 'System CSV importer: created: 3 | updated: 0 | skipped: 0 | multiple: 0 [2021-03-07 21:12:00 - 2021-03-07 21:12:00]')
        self.assertEqual(messages[0].level_tag, 'success')
        # switch user context
        self.client.logout()
        self.client.login(username='message_user', password='UFPntl9kU9vYkXwAo9SS')
        # get response
        response = self.client.get('/system/')
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare - user 2
        self.assertEqual(str(response.context['user']), 'message_user')
        self.assertEqual(messages[0].message, 'System CSV importer: created: 3 | updated: 0 | skipped: 0 | multiple: 0 [2021-03-07 21:12:00 - 2021-03-07 21:12:00]')
        self.assertEqual(messages[0].level_tag, 'success')
        # compare - systems / attributes
        compare_system_and_attributes_csv(self, '21')
        # compare domain (delimiter specific)
        compare_delimiter_specific(self, '21')

    def test_system_importer_file_csv_instant_minimal_comma(self):
        """ test importer view """

        # change config
        set_csv_import_filename('system_importer_file_csv_testfile_21_minimal_comma.csv')
        # change config
        set_config_field_delimiter_comma()

        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_minimal', password='H6mM7kq9sEZLvm6CyOaW')
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
        # compare - systems / attributes
        compare_system_and_attributes_csv(self, '21')
        # compare domain (delimiter specific)
        compare_delimiter_specific(self, '21')

    def test_system_importer_file_csv_upload_post_minimal_comma(self):
        """ test importer view """

        # change config
        set_config_field_delimiter_comma()

        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_minimal', password='H6mM7kq9sEZLvm6CyOaW')
        # open upload file
        systemcsv = open(os.path.join(BASE_DIR, 'dfirtrack_main/tests/system_importer/system_importer_file_csv_files/system_importer_file_csv_testfile_21_minimal_comma.csv'), 'r')
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
        # compare - systems / attributes
        compare_system_and_attributes_csv(self, '21')
        # compare domain (delimiter specific)
        compare_delimiter_specific(self, '21')

    """ field delimiter - semicolon """

    def test_system_importer_file_csv_cron_minimal_semicolon(self):
        """ test importer view """

        # change config
        set_csv_import_filename('system_importer_file_csv_testfile_22_minimal_semicolon.csv')
        # change config
        set_config_field_delimiter_semicolon()

        # mock timezone.now()
        t_6 = datetime(2021, 3, 7, 21, 17, tzinfo=timezone.utc)
        with patch.object(timezone, 'now', return_value=t_6):

            # execute cron job / scheduled task
            system_cron()

        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_minimal', password='H6mM7kq9sEZLvm6CyOaW')
        # get response
        response = self.client.get('/system/')
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare - user 1
        self.assertEqual(str(response.context['user']), 'testuser_system_importer_file_csv_minimal')
        self.assertEqual(messages[0].message, 'System CSV importer: created: 3 | updated: 0 | skipped: 0 | multiple: 0 [2021-03-07 21:17:00 - 2021-03-07 21:17:00]')
        self.assertEqual(messages[0].level_tag, 'success')
        # switch user context
        self.client.logout()
        self.client.login(username='message_user', password='UFPntl9kU9vYkXwAo9SS')
        # get response
        response = self.client.get('/system/')
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare - user 2
        self.assertEqual(str(response.context['user']), 'message_user')
        self.assertEqual(messages[0].message, 'System CSV importer: created: 3 | updated: 0 | skipped: 0 | multiple: 0 [2021-03-07 21:17:00 - 2021-03-07 21:17:00]')
        self.assertEqual(messages[0].level_tag, 'success')
        # compare - systems / attributes
        compare_system_and_attributes_csv(self, '22')
        # compare domain (delimiter specific)
        compare_delimiter_specific(self, '22')

    def test_system_importer_file_csv_instant_minimal_semicolon(self):
        """ test importer view """

        # change config
        set_csv_import_filename('system_importer_file_csv_testfile_22_minimal_semicolon.csv')
        # change config
        set_config_field_delimiter_semicolon()

        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_minimal', password='H6mM7kq9sEZLvm6CyOaW')
        # create url
        destination = urllib.parse.quote('/system/', safe='/')
        # get response
        response = self.client.get('/system/importer/file/csv/instant/', follow=True)
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)
        # compare - messages
        compare_messages_csv(self, messages)
        # compare - systems / attributes
        compare_system_and_attributes_csv(self, '22')
        # compare domain (delimiter specific)
        compare_delimiter_specific(self, '22')

    def test_system_importer_file_csv_upload_post_minimal_semicolon(self):
        """ test importer view """

        # change config
        set_config_field_delimiter_semicolon()

        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_minimal', password='H6mM7kq9sEZLvm6CyOaW')
        # open upload file
        systemcsv = open(os.path.join(BASE_DIR, 'dfirtrack_main/tests/system_importer/system_importer_file_csv_files/system_importer_file_csv_testfile_22_minimal_semicolon.csv'), 'r')
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
        # compare - systems / attributes
        compare_system_and_attributes_csv(self, '22')
        # compare domain (delimiter specific)
        compare_delimiter_specific(self, '22')

    """ ip delimiter - comma """

    def test_system_importer_file_csv_cron_ip_delimiter_comma(self):
        """ test importer view """

        # change config
        set_csv_import_filename('system_importer_file_csv_testfile_51_ip_delimiter_comma.csv')
        # change config
        set_config_ip_delimiter_comma()

        # mock timezone.now()
        t_7 = datetime(2021, 3, 21, 19, 35, tzinfo=timezone.utc)
        with patch.object(timezone, 'now', return_value=t_7):

            # execute cron job / scheduled task
            system_cron()

        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_minimal', password='H6mM7kq9sEZLvm6CyOaW')
        # get response
        response = self.client.get('/system/')
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare - user 1
        self.assertEqual(str(response.context['user']), 'testuser_system_importer_file_csv_minimal')
        self.assertEqual(messages[0].message, 'System CSV importer: created: 3 | updated: 0 | skipped: 0 | multiple: 0 [2021-03-21 19:35:00 - 2021-03-21 19:35:00]')
        self.assertEqual(messages[0].level_tag, 'success')
        # switch user context
        self.client.logout()
        self.client.login(username='message_user', password='UFPntl9kU9vYkXwAo9SS')
        # get response
        response = self.client.get('/system/')
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare - user 2
        self.assertEqual(str(response.context['user']), 'message_user')
        self.assertEqual(messages[0].message, 'System CSV importer: created: 3 | updated: 0 | skipped: 0 | multiple: 0 [2021-03-21 19:35:00 - 2021-03-21 19:35:00]')
        self.assertEqual(messages[0].level_tag, 'success')
        # compare - systems / attributes
        compare_system_and_attributes_csv(self, '51')
        # compare - IPs
        compare_ips(self, '51')

    def test_system_importer_file_csv_instant_ip_delimiter_comma(self):
        """ test importer view """

        # change config
        set_csv_import_filename('system_importer_file_csv_testfile_51_ip_delimiter_comma.csv')
        # change config
        set_config_ip_delimiter_comma()

        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_minimal', password='H6mM7kq9sEZLvm6CyOaW')
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
        # compare - systems / attributes
        compare_system_and_attributes_csv(self, '51')
        # compare - IPs
        compare_ips(self, '51')

    def test_system_importer_file_csv_upload_post_ip_delimiter_comma(self):
        """ test importer view """

        # change config
        set_config_ip_delimiter_comma()

        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_minimal', password='H6mM7kq9sEZLvm6CyOaW')
        # open upload file
        systemcsv = open(os.path.join(BASE_DIR, 'dfirtrack_main/tests/system_importer/system_importer_file_csv_files/system_importer_file_csv_testfile_51_ip_delimiter_comma.csv'), 'r')
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
        # compare - systems / attributes
        compare_system_and_attributes_csv(self, '51')
        # compare - IPs
        compare_ips(self, '51')

    """ ip delimiter - semicolon """

    def test_system_importer_file_csv_cron_ip_delimiter_semicolon(self):
        """ test importer view """

        # change config
        set_csv_import_filename('system_importer_file_csv_testfile_52_ip_delimiter_semicolon.csv')
        # change config
        set_config_ip_delimiter_semicolon()

        # mock timezone.now()
        t_8 = datetime(2021, 3, 21, 19, 40, tzinfo=timezone.utc)
        with patch.object(timezone, 'now', return_value=t_8):

            # execute cron job / scheduled task
            system_cron()

        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_minimal', password='H6mM7kq9sEZLvm6CyOaW')
        # get response
        response = self.client.get('/system/')
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare - user 1
        self.assertEqual(str(response.context['user']), 'testuser_system_importer_file_csv_minimal')
        self.assertEqual(messages[0].message, 'System CSV importer: created: 3 | updated: 0 | skipped: 0 | multiple: 0 [2021-03-21 19:40:00 - 2021-03-21 19:40:00]')
        self.assertEqual(messages[0].level_tag, 'success')
        # switch user context
        self.client.logout()
        self.client.login(username='message_user', password='UFPntl9kU9vYkXwAo9SS')
        # get response
        response = self.client.get('/system/')
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare - user 2
        self.assertEqual(str(response.context['user']), 'message_user')
        self.assertEqual(messages[0].message, 'System CSV importer: created: 3 | updated: 0 | skipped: 0 | multiple: 0 [2021-03-21 19:40:00 - 2021-03-21 19:40:00]')
        self.assertEqual(messages[0].level_tag, 'success')
        # compare - systems / attributes
        compare_system_and_attributes_csv(self, '52')
        # compare - IPs
        compare_ips(self, '52')

    def test_system_importer_file_csv_instant_ip_delimiter_semicolon(self):
        """ test importer view """

        # change config
        set_csv_import_filename('system_importer_file_csv_testfile_52_ip_delimiter_semicolon.csv')
        # change config
        set_config_ip_delimiter_semicolon()

        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_minimal', password='H6mM7kq9sEZLvm6CyOaW')
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
        # compare - systems / attributes
        compare_system_and_attributes_csv(self, '52')
        # compare - IPs
        compare_ips(self, '52')

    def test_system_importer_file_csv_upload_post_ip_delimiter_semicolon(self):
        """ test importer view """

        # change config
        set_config_ip_delimiter_semicolon()

        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_minimal', password='H6mM7kq9sEZLvm6CyOaW')
        # open upload file
        systemcsv = open(os.path.join(BASE_DIR, 'dfirtrack_main/tests/system_importer/system_importer_file_csv_files/system_importer_file_csv_testfile_52_ip_delimiter_semicolon.csv'), 'r')
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
        # compare - systems / attributes
        compare_system_and_attributes_csv(self, '52')
        # compare - IPs
        compare_ips(self, '52')

    """ ip delimiter - space """

    def test_system_importer_file_csv_cron_ip_delimiter_space(self):
        """ test importer view """

        # change config
        set_csv_import_filename('system_importer_file_csv_testfile_53_ip_delimiter_space.csv')
        # change config
        set_config_ip_delimiter_space()

        # mock timezone.now()
        t_9 = datetime(2021, 3, 21, 19, 45, tzinfo=timezone.utc)
        with patch.object(timezone, 'now', return_value=t_9):

            # execute cron job / scheduled task
            system_cron()

        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_minimal', password='H6mM7kq9sEZLvm6CyOaW')
        # get response
        response = self.client.get('/system/')
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare - user 1
        self.assertEqual(str(response.context['user']), 'testuser_system_importer_file_csv_minimal')
        self.assertEqual(messages[0].message, 'System CSV importer: created: 3 | updated: 0 | skipped: 0 | multiple: 0 [2021-03-21 19:45:00 - 2021-03-21 19:45:00]')
        self.assertEqual(messages[0].level_tag, 'success')
        # switch user context
        self.client.logout()
        self.client.login(username='message_user', password='UFPntl9kU9vYkXwAo9SS')
        # get response
        response = self.client.get('/system/')
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare - user 2
        self.assertEqual(str(response.context['user']), 'message_user')
        self.assertEqual(messages[0].message, 'System CSV importer: created: 3 | updated: 0 | skipped: 0 | multiple: 0 [2021-03-21 19:45:00 - 2021-03-21 19:45:00]')
        self.assertEqual(messages[0].level_tag, 'success')
        # compare - systems / attributes
        compare_system_and_attributes_csv(self, '53')
        # compare - IPs
        compare_ips(self, '53')

    def test_system_importer_file_csv_instant_ip_delimiter_space(self):
        """ test importer view """

        # change config
        set_csv_import_filename('system_importer_file_csv_testfile_53_ip_delimiter_space.csv')
        # change config
        set_config_ip_delimiter_space()

        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_minimal', password='H6mM7kq9sEZLvm6CyOaW')
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
        # compare - systems / attributes
        compare_system_and_attributes_csv(self, '53')
        # compare - IPs
        compare_ips(self, '53')

    def test_system_importer_file_csv_upload_post_ip_delimiter_space(self):
        """ test importer view """

        # change config
        set_config_ip_delimiter_space()

        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_minimal', password='H6mM7kq9sEZLvm6CyOaW')
        # open upload file
        systemcsv = open(os.path.join(BASE_DIR, 'dfirtrack_main/tests/system_importer/system_importer_file_csv_files/system_importer_file_csv_testfile_53_ip_delimiter_space.csv'), 'r')
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
        # compare - systems / attributes
        compare_system_and_attributes_csv(self, '53')
        # compare - IPs
        compare_ips(self, '53')

    """ tag delimiter - comma """

    def test_system_importer_file_csv_cron_tag_delimiter_comma(self):
        """ test importer view """

        # change config
        set_csv_import_filename('system_importer_file_csv_testfile_54_tag_delimiter_comma.csv')
        # change config
        set_config_tag_delimiter_comma()

        # mock timezone.now()
        t_10 = datetime(2021, 3, 22, 18, 35, tzinfo=timezone.utc)
        with patch.object(timezone, 'now', return_value=t_10):

            # execute cron job / scheduled task
            system_cron()

        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_minimal', password='H6mM7kq9sEZLvm6CyOaW')
        # get response
        response = self.client.get('/system/')
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare - user 1
        self.assertEqual(str(response.context['user']), 'testuser_system_importer_file_csv_minimal')
        self.assertEqual(messages[0].message, 'System CSV importer: created: 3 | updated: 0 | skipped: 0 | multiple: 0 [2021-03-22 18:35:00 - 2021-03-22 18:35:00]')
        self.assertEqual(messages[0].level_tag, 'success')
        # switch user context
        self.client.logout()
        self.client.login(username='message_user', password='UFPntl9kU9vYkXwAo9SS')
        # get response
        response = self.client.get('/system/')
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare - user 2
        self.assertEqual(str(response.context['user']), 'message_user')
        self.assertEqual(messages[0].message, 'System CSV importer: created: 3 | updated: 0 | skipped: 0 | multiple: 0 [2021-03-22 18:35:00 - 2021-03-22 18:35:00]')
        self.assertEqual(messages[0].level_tag, 'success')
        # compare - systems / attributes
        compare_system_and_attributes_csv(self, '54')
        # compare - tags
        compare_tags(self, '54', '_')

    def test_system_importer_file_csv_instant_tag_delimiter_comma(self):
        """ test importer view """

        # change config
        set_csv_import_filename('system_importer_file_csv_testfile_54_tag_delimiter_comma.csv')
        # change config
        set_config_tag_delimiter_comma()

        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_minimal', password='H6mM7kq9sEZLvm6CyOaW')
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
        # compare - systems / attributes
        compare_system_and_attributes_csv(self, '54')
        # compare - tags
        compare_tags(self, '54', '_')

    def test_system_importer_file_csv_upload_post_tag_delimiter_comma(self):
        """ test importer view """

        # change config
        set_config_tag_delimiter_comma()

        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_minimal', password='H6mM7kq9sEZLvm6CyOaW')
        # open upload file
        systemcsv = open(os.path.join(BASE_DIR, 'dfirtrack_main/tests/system_importer/system_importer_file_csv_files/system_importer_file_csv_testfile_54_tag_delimiter_comma.csv'), 'r')
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
        # compare - systems / attributes
        compare_system_and_attributes_csv(self, '54')
        # compare - tags
        compare_tags(self, '54', '_')

    """ tag delimiter - semicolon """

    def test_system_importer_file_csv_cron_tag_delimiter_semicolon(self):
        """ test importer view """

        # change config
        set_csv_import_filename('system_importer_file_csv_testfile_55_tag_delimiter_semicolon.csv')
        # change config
        set_config_tag_delimiter_semicolon()

        # mock timezone.now()
        t_8 = datetime(2021, 3, 22, 18, 40, tzinfo=timezone.utc)
        with patch.object(timezone, 'now', return_value=t_8):

            # execute cron job / scheduled task
            system_cron()

        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_minimal', password='H6mM7kq9sEZLvm6CyOaW')
        # get response
        response = self.client.get('/system/')
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare - user 1
        self.assertEqual(str(response.context['user']), 'testuser_system_importer_file_csv_minimal')
        self.assertEqual(messages[0].message, 'System CSV importer: created: 3 | updated: 0 | skipped: 0 | multiple: 0 [2021-03-22 18:40:00 - 2021-03-22 18:40:00]')
        self.assertEqual(messages[0].level_tag, 'success')
        # switch user context
        self.client.logout()
        self.client.login(username='message_user', password='UFPntl9kU9vYkXwAo9SS')
        # get response
        response = self.client.get('/system/')
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare - user 2
        self.assertEqual(str(response.context['user']), 'message_user')
        self.assertEqual(messages[0].message, 'System CSV importer: created: 3 | updated: 0 | skipped: 0 | multiple: 0 [2021-03-22 18:40:00 - 2021-03-22 18:40:00]')
        self.assertEqual(messages[0].level_tag, 'success')
        # compare - systems / attributes
        compare_system_and_attributes_csv(self, '55')
        # compare - tags
        compare_tags(self, '55', '_')

    def test_system_importer_file_csv_instant_tag_delimiter_semicolon(self):
        """ test importer view """

        # change config
        set_csv_import_filename('system_importer_file_csv_testfile_55_tag_delimiter_semicolon.csv')
        # change config
        set_config_tag_delimiter_semicolon()

        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_minimal', password='H6mM7kq9sEZLvm6CyOaW')
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
        # compare - systems / attributes
        compare_system_and_attributes_csv(self, '55')
        # compare - tags
        compare_tags(self, '55', '_')

    def test_system_importer_file_csv_upload_post_tag_delimiter_semicolon(self):
        """ test importer view """

        # change config
        set_config_tag_delimiter_semicolon()

        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_minimal', password='H6mM7kq9sEZLvm6CyOaW')
        # open upload file
        systemcsv = open(os.path.join(BASE_DIR, 'dfirtrack_main/tests/system_importer/system_importer_file_csv_files/system_importer_file_csv_testfile_55_tag_delimiter_semicolon.csv'), 'r')
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
        # compare - systems / attributes
        compare_system_and_attributes_csv(self, '55')
        # compare - tags
        compare_tags(self, '55', '_')

    """ tag delimiter - space """

    def test_system_importer_file_csv_cron_tag_delimiter_space(self):
        """ test importer view """

        # change config
        set_csv_import_filename('system_importer_file_csv_testfile_56_tag_delimiter_space.csv')
        # change config
        set_config_tag_delimiter_space()

        # mock timezone.now()
        t_9 = datetime(2021, 3, 22, 18, 45, tzinfo=timezone.utc)
        with patch.object(timezone, 'now', return_value=t_9):

            # execute cron job / scheduled task
            system_cron()

        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_minimal', password='H6mM7kq9sEZLvm6CyOaW')
        # get response
        response = self.client.get('/system/')
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare - user 1
        self.assertEqual(str(response.context['user']), 'testuser_system_importer_file_csv_minimal')
        self.assertEqual(messages[0].message, 'System CSV importer: created: 3 | updated: 0 | skipped: 0 | multiple: 0 [2021-03-22 18:45:00 - 2021-03-22 18:45:00]')
        self.assertEqual(messages[0].level_tag, 'success')
        # switch user context
        self.client.logout()
        self.client.login(username='message_user', password='UFPntl9kU9vYkXwAo9SS')
        # get response
        response = self.client.get('/system/')
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare - user 2
        self.assertEqual(str(response.context['user']), 'message_user')
        self.assertEqual(messages[0].message, 'System CSV importer: created: 3 | updated: 0 | skipped: 0 | multiple: 0 [2021-03-22 18:45:00 - 2021-03-22 18:45:00]')
        self.assertEqual(messages[0].level_tag, 'success')
        # compare - systems / attributes
        compare_system_and_attributes_csv(self, '56')
        # compare - tags
        compare_tags(self, '56', '_')

    def test_system_importer_file_csv_instant_tag_delimiter_space(self):
        """ test importer view """

        # change config
        set_csv_import_filename('system_importer_file_csv_testfile_56_tag_delimiter_space.csv')
        # change config
        set_config_tag_delimiter_space()

        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_minimal', password='H6mM7kq9sEZLvm6CyOaW')
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
        # compare - systems / attributes
        compare_system_and_attributes_csv(self, '56')
        # compare - tags
        compare_tags(self, '56', '_')

    def test_system_importer_file_csv_upload_post_tag_delimiter_space(self):
        """ test importer view """

        # change config
        set_config_tag_delimiter_space()

        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_minimal', password='H6mM7kq9sEZLvm6CyOaW')
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
        # compare - systems / attributes
        compare_system_and_attributes_csv(self, '56')
        # compare - tags
        compare_tags(self, '56', '_')

    """ tag prefix delimiter - underscore """

    def test_system_importer_file_csv_cron_tag_prefix_delimiter_underscore(self):
        """ test importer view """

        # change config
        set_csv_import_filename('system_importer_file_csv_testfile_56_tag_delimiter_space.csv')
        # change config
        set_config_tag_prefix_delimiter_underscore()

        # mock timezone.now()
        t_10 = datetime(2021, 3, 22, 19, 10, tzinfo=timezone.utc)
        with patch.object(timezone, 'now', return_value=t_10):

            # execute cron job / scheduled task
            system_cron()

        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_minimal', password='H6mM7kq9sEZLvm6CyOaW')
        # get response
        response = self.client.get('/system/')
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare - user 1
        self.assertEqual(str(response.context['user']), 'testuser_system_importer_file_csv_minimal')
        self.assertEqual(messages[0].message, 'System CSV importer: created: 3 | updated: 0 | skipped: 0 | multiple: 0 [2021-03-22 19:10:00 - 2021-03-22 19:10:00]')
        self.assertEqual(messages[0].level_tag, 'success')
        # switch user context
        self.client.logout()
        self.client.login(username='message_user', password='UFPntl9kU9vYkXwAo9SS')
        # get response
        response = self.client.get('/system/')
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare - user 2
        self.assertEqual(str(response.context['user']), 'message_user')
        self.assertEqual(messages[0].message, 'System CSV importer: created: 3 | updated: 0 | skipped: 0 | multiple: 0 [2021-03-22 19:10:00 - 2021-03-22 19:10:00]')
        self.assertEqual(messages[0].level_tag, 'success')
        # compare - systems / attributes
        compare_system_and_attributes_csv(self, '56')
        # compare - tags
        compare_tags(self, '56', '_')

    def test_system_importer_file_csv_instant_tag_prefix_delimiter_underscore(self):
        """ test importer view """

        # change config
        set_csv_import_filename('system_importer_file_csv_testfile_56_tag_delimiter_space.csv')
        # change config
        set_config_tag_prefix_delimiter_underscore()

        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_minimal', password='H6mM7kq9sEZLvm6CyOaW')
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
        # compare - systems / attributes
        compare_system_and_attributes_csv(self, '56')
        # compare - tags
        compare_tags(self, '56', '_')

    def test_system_importer_file_csv_upload_post_tag_prefix_delimiter_underscore(self):
        """ test importer view """

        # change config
        set_config_tag_prefix_delimiter_underscore()

        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_minimal', password='H6mM7kq9sEZLvm6CyOaW')
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
        # compare - systems / attributes
        compare_system_and_attributes_csv(self, '56')
        # compare - tags
        compare_tags(self, '56', '_')

    """ tag prefix delimiter - hyphen """

    def test_system_importer_file_csv_cron_tag_prefix_delimiter_hyphen(self):
        """ test importer view """

        # change config
        set_csv_import_filename('system_importer_file_csv_testfile_56_tag_delimiter_space.csv')
        # change config
        set_config_tag_prefix_delimiter_hyphen()

        # mock timezone.now()
        t_8 = datetime(2021, 3, 22, 19, 15, tzinfo=timezone.utc)
        with patch.object(timezone, 'now', return_value=t_8):

            # execute cron job / scheduled task
            system_cron()

        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_minimal', password='H6mM7kq9sEZLvm6CyOaW')
        # get response
        response = self.client.get('/system/')
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare - user 1
        self.assertEqual(str(response.context['user']), 'testuser_system_importer_file_csv_minimal')
        self.assertEqual(messages[0].message, 'System CSV importer: created: 3 | updated: 0 | skipped: 0 | multiple: 0 [2021-03-22 19:15:00 - 2021-03-22 19:15:00]')
        self.assertEqual(messages[0].level_tag, 'success')
        # switch user context
        self.client.logout()
        self.client.login(username='message_user', password='UFPntl9kU9vYkXwAo9SS')
        # get response
        response = self.client.get('/system/')
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare - user 2
        self.assertEqual(str(response.context['user']), 'message_user')
        self.assertEqual(messages[0].message, 'System CSV importer: created: 3 | updated: 0 | skipped: 0 | multiple: 0 [2021-03-22 19:15:00 - 2021-03-22 19:15:00]')
        self.assertEqual(messages[0].level_tag, 'success')
        # compare - systems / attributes
        compare_system_and_attributes_csv(self, '56')
        # compare - tags
        compare_tags(self, '56', '-')

    def test_system_importer_file_csv_instant_tag_prefix_delimiter_hyphen(self):
        """ test importer view """

        # change config
        set_csv_import_filename('system_importer_file_csv_testfile_56_tag_delimiter_space.csv')
        # change config
        set_config_tag_prefix_delimiter_hyphen()

        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_minimal', password='H6mM7kq9sEZLvm6CyOaW')
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
        # compare - systems / attributes
        compare_system_and_attributes_csv(self, '56')
        # compare - tags
        compare_tags(self, '56', '-')

    def test_system_importer_file_csv_upload_post_tag_prefix_delimiter_hyphen(self):
        """ test importer view """

        # change config
        set_config_tag_prefix_delimiter_hyphen()

        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_minimal', password='H6mM7kq9sEZLvm6CyOaW')
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
        # compare - systems / attributes
        compare_system_and_attributes_csv(self, '56')
        # compare - tags
        compare_tags(self, '56', '-')

    """ tag prefix delimiter - period """

    def test_system_importer_file_csv_cron_tag_prefix_delimiter_period(self):
        """ test importer view """

        # change config
        set_csv_import_filename('system_importer_file_csv_testfile_56_tag_delimiter_space.csv')
        # change config
        set_config_tag_prefix_delimiter_period()

        # mock timezone.now()
        t_9 = datetime(2021, 3, 22, 19, 20, tzinfo=timezone.utc)
        with patch.object(timezone, 'now', return_value=t_9):

            # execute cron job / scheduled task
            system_cron()

        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_minimal', password='H6mM7kq9sEZLvm6CyOaW')
        # get response
        response = self.client.get('/system/')
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare - user 1
        self.assertEqual(str(response.context['user']), 'testuser_system_importer_file_csv_minimal')
        self.assertEqual(messages[0].message, 'System CSV importer: created: 3 | updated: 0 | skipped: 0 | multiple: 0 [2021-03-22 19:20:00 - 2021-03-22 19:20:00]')
        self.assertEqual(messages[0].level_tag, 'success')
        # switch user context
        self.client.logout()
        self.client.login(username='message_user', password='UFPntl9kU9vYkXwAo9SS')
        # get response
        response = self.client.get('/system/')
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare - user 2
        self.assertEqual(str(response.context['user']), 'message_user')
        self.assertEqual(messages[0].message, 'System CSV importer: created: 3 | updated: 0 | skipped: 0 | multiple: 0 [2021-03-22 19:20:00 - 2021-03-22 19:20:00]')
        self.assertEqual(messages[0].level_tag, 'success')
        # compare - systems / attributes
        compare_system_and_attributes_csv(self, '56')
        # compare - tags
        compare_tags(self, '56', '.')

    def test_system_importer_file_csv_instant_tag_prefix_delimiter_period(self):
        """ test importer view """

        # change config
        set_csv_import_filename('system_importer_file_csv_testfile_56_tag_delimiter_space.csv')
        # change config
        set_config_tag_prefix_delimiter_period()

        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_minimal', password='H6mM7kq9sEZLvm6CyOaW')
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
        # compare - systems / attributes
        compare_system_and_attributes_csv(self, '56')
        # compare - tags
        compare_tags(self, '56', '.')

    def test_system_importer_file_csv_upload_post_tag_prefix_delimiter_period(self):
        """ test importer view """

        # change config
        set_config_tag_prefix_delimiter_period()

        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_minimal', password='H6mM7kq9sEZLvm6CyOaW')
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
        # compare - systems / attributes
        compare_system_and_attributes_csv(self, '56')
        # compare - tags
        compare_tags(self, '56', '.')
