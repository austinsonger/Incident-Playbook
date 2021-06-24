from datetime import datetime
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.test import TestCase
from django.utils import timezone
from dfirtrack.settings import BASE_DIR
from dfirtrack_config.models import SystemImporterFileCsvConfigModel
from dfirtrack_main.importer.file.csv import system_cron
from dfirtrack_main.models import Analysisstatus, Case, Company, Dnsname, Domain, Ip, Location, Os, Reason, Recommendation, Serviceprovider, System, Systemstatus, Systemtype, Tag
from dfirtrack_main.tests.system_importer.config_functions import set_config_check_attributes_csv
from dfirtrack_main.tests.system_importer.config_functions import set_config_check_attributes_domain_name
from dfirtrack_main.tests.system_importer.config_functions import set_config_column_system
from dfirtrack_main.tests.system_importer.config_functions import set_csv_import_filename
from mock import patch
import os
import urllib.parse


def compare_messages_faulty_systems(self, messages):
    """ compare messages """

    # compare - messages
    self.assertEqual(messages[0].message, 'Value for system in row 2 was too long. System not created.')
    self.assertEqual(messages[0].level_tag, 'warning')
    self.assertEqual(messages[1].message, 'Value for system in row 4 was an empty string. System not created.')
    self.assertEqual(messages[1].level_tag, 'warning')
    self.assertEqual(messages[2].message, 'Index for system in row 5 was out of range. System not created.')
    self.assertEqual(messages[2].level_tag, 'warning')
    self.assertEqual(messages[3].message, '3 systems were created.')
    self.assertEqual(messages[3].level_tag, 'success')
    self.assertEqual(messages[4].message, '3 systems were skipped.')
    self.assertEqual(messages[4].level_tag, 'success')

    # return to test function
    return self

def compare_messages_csv(self, messages):
    """ compare messages """

    # set counter
    message_counter = 0

    # compare - messages
    self.assertEqual(messages[message_counter].message, 'Value for DNS name in row 2 was not a valid value.')
    self.assertEqual(messages[message_counter].level_tag, 'warning')
    message_counter += 1
    self.assertEqual(messages[message_counter].message, 'Value for domain in row 2 was not a valid value.')
    self.assertEqual(messages[message_counter].level_tag, 'warning')
    message_counter += 1
    self.assertEqual(messages[message_counter].message, 'Value for location in row 2 was not a valid value.')
    self.assertEqual(messages[message_counter].level_tag, 'warning')
    message_counter += 1
    self.assertEqual(messages[message_counter].message, 'Value for OS in row 2 was not a valid value.')
    self.assertEqual(messages[message_counter].level_tag, 'warning')
    message_counter += 1
    self.assertEqual(messages[message_counter].message, 'Value for reason in row 2 was not a valid value.')
    self.assertEqual(messages[message_counter].level_tag, 'warning')
    message_counter += 1
    self.assertEqual(messages[message_counter].message, 'Value for recommendation in row 2 was not a valid value.')
    self.assertEqual(messages[message_counter].level_tag, 'warning')
    message_counter += 1
    self.assertEqual(messages[message_counter].message, 'Value for serviceprovider in row 2 was not a valid value.')
    self.assertEqual(messages[message_counter].level_tag, 'warning')
    message_counter += 1
    self.assertEqual(messages[message_counter].message, 'Value for systemtype in row 2 was not a valid value.')
    self.assertEqual(messages[message_counter].level_tag, 'warning')
    message_counter += 1
    self.assertEqual(messages[message_counter].message, 'Value for IP address in row 2 was not a valid IP address.')
    self.assertEqual(messages[message_counter].level_tag, 'warning')
    message_counter += 1
    self.assertEqual(messages[message_counter].message, 'Value for case in row 2 was not a valid value.')
    self.assertEqual(messages[message_counter].level_tag, 'warning')
    message_counter += 1
    self.assertEqual(messages[message_counter].message, 'Value for company in row 2 was not a valid value.')
    self.assertEqual(messages[message_counter].level_tag, 'warning')
    message_counter += 1
    self.assertEqual(messages[message_counter].message, 'Value for tag in row 2 was not a valid value.')
    self.assertEqual(messages[message_counter].level_tag, 'warning')
    message_counter += 1
    self.assertEqual(messages[message_counter].message, 'Index for DNS name in row 3 was out of range.')
    self.assertEqual(messages[message_counter].level_tag, 'warning')
    message_counter += 1
    self.assertEqual(messages[message_counter].message, 'Index for domain in row 3 was out of range.')
    self.assertEqual(messages[message_counter].level_tag, 'warning')
    message_counter += 1
    self.assertEqual(messages[message_counter].message, 'Index for location in row 3 was out of range.')
    self.assertEqual(messages[message_counter].level_tag, 'warning')
    message_counter += 1
    self.assertEqual(messages[message_counter].message, 'Index for OS in row 3 was out of range.')
    self.assertEqual(messages[message_counter].level_tag, 'warning')
    message_counter += 1
    self.assertEqual(messages[message_counter].message, 'Index for reason in row 3 was out of range.')
    self.assertEqual(messages[message_counter].level_tag, 'warning')
    message_counter += 1
    self.assertEqual(messages[message_counter].message, 'Index for recommendation in row 3 was out of range.')
    self.assertEqual(messages[message_counter].level_tag, 'warning')
    message_counter += 1
    self.assertEqual(messages[message_counter].message, 'Index for serviceprovider in row 3 was out of range.')
    self.assertEqual(messages[message_counter].level_tag, 'warning')
    message_counter += 1
    self.assertEqual(messages[message_counter].message, 'Index for systemtype in row 3 was out of range.')
    self.assertEqual(messages[message_counter].level_tag, 'warning')
    message_counter += 1
    self.assertEqual(messages[message_counter].message, 'Index for IP in row 3 was out of range.')
    self.assertEqual(messages[message_counter].level_tag, 'warning')
    message_counter += 1
    self.assertEqual(messages[message_counter].message, 'Index for case in row 3 was out of range.')
    self.assertEqual(messages[message_counter].level_tag, 'warning')
    message_counter += 1
    self.assertEqual(messages[message_counter].message, 'Index for company in row 3 was out of range.')
    self.assertEqual(messages[message_counter].level_tag, 'warning')
    message_counter += 1
    self.assertEqual(messages[message_counter].message, 'Index for tag in row 3 was out of range.')
    self.assertEqual(messages[message_counter].level_tag, 'warning')
    message_counter += 1
    self.assertEqual(messages[message_counter].message, '4 systems were created.')
    self.assertEqual(messages[message_counter].level_tag, 'success')
    message_counter += 1

    # return to test function
    return self

def compare_messages_domain_name(self, messages):
    """ compare messages """

    # compare - messages
    self.assertEqual(messages[0].message, '3 systems were created.')
    self.assertEqual(messages[0].level_tag, 'success')

    # return to test function
    return self

def compare_system_and_attributes_faulty_systems(self):
    """ compare systems and associated attributes """

    # compare - systems / attributes
    self.assertTrue(System.objects.filter(system_name='system_csv_31_001').exists())
    self.assertTrue(System.objects.filter(system_name='system_csv_31_003').exists())
    self.assertTrue(System.objects.filter(system_name='system_csv_31_006').exists())
    # compare - systems / attributes
    self.assertEqual(System.objects.get(system_name='system_csv_31_001').analysisstatus, Analysisstatus.objects.get(analysisstatus_name='analysisstatus_1'))
    self.assertEqual(System.objects.get(system_name='system_csv_31_003').analysisstatus, Analysisstatus.objects.get(analysisstatus_name='analysisstatus_1'))
    self.assertEqual(System.objects.get(system_name='system_csv_31_006').analysisstatus, Analysisstatus.objects.get(analysisstatus_name='analysisstatus_1'))
    self.assertEqual(System.objects.get(system_name='system_csv_31_001').systemstatus, Systemstatus.objects.get(systemstatus_name='systemstatus_1'))
    self.assertEqual(System.objects.get(system_name='system_csv_31_003').systemstatus, Systemstatus.objects.get(systemstatus_name='systemstatus_1'))
    self.assertEqual(System.objects.get(system_name='system_csv_31_006').systemstatus, Systemstatus.objects.get(systemstatus_name='systemstatus_1'))

    # return to test function
    return self

def compare_system_and_attributes_csv(self):
    """ compare systems and associated attributes """

    # compare - systems / attributes
    self.assertTrue(System.objects.filter(system_name='system_csv_32_001').exists())
    self.assertTrue(System.objects.filter(system_name='system_csv_32_002').exists())
    self.assertTrue(System.objects.filter(system_name='system_csv_32_003').exists())
    self.assertTrue(System.objects.filter(system_name='system_csv_32_004').exists())
    self.assertTrue(Ip.objects.filter(ip_ip='127.32.1.1').exists())
    self.assertTrue(Ip.objects.filter(ip_ip='127.32.1.2').exists())
    self.assertTrue(Domain.objects.filter(domain_name='domain_1').exists())
    self.assertTrue(Dnsname.objects.filter(dnsname_name='dnsname_1').exists())
    self.assertTrue(Location.objects.filter(location_name='location_1').exists())
    self.assertTrue(Os.objects.filter(os_name='os_1').exists())
    self.assertTrue(Reason.objects.filter(reason_name='reason_1').exists())
    self.assertTrue(Recommendation.objects.filter(recommendation_name='recommendation_1').exists())
    self.assertTrue(Serviceprovider.objects.filter(serviceprovider_name='serviceprovider_1').exists())
    self.assertTrue(Systemtype.objects.filter(systemtype_name='systemtype_1').exists())
    self.assertTrue(Case.objects.filter(case_name='case_1').exists())
    self.assertTrue(Company.objects.filter(company_name='company_1').exists())
    self.assertTrue(Tag.objects.filter(tag_name='AUTO_tag_1').exists())
    # compare - systems / attributes
    self.assertTrue(System.objects.get(system_name='system_csv_32_001').ip.filter(ip_ip='127.32.1.1').exists())
    self.assertTrue(System.objects.get(system_name='system_csv_32_001').ip.filter(ip_ip='127.32.1.2').exists())
    self.assertEqual(System.objects.get(system_name='system_csv_32_001').dnsname, Dnsname.objects.get(dnsname_name='dnsname_1'))
    self.assertEqual(System.objects.get(system_name='system_csv_32_001').domain, Domain.objects.get(domain_name='domain_1'))
    self.assertEqual(System.objects.get(system_name='system_csv_32_001').location, Location.objects.get(location_name='location_1'))
    self.assertEqual(System.objects.get(system_name='system_csv_32_001').os, Os.objects.get(os_name='os_1'))
    self.assertEqual(System.objects.get(system_name='system_csv_32_001').reason, Reason.objects.get(reason_name='reason_1'))
    self.assertEqual(System.objects.get(system_name='system_csv_32_001').recommendation, Recommendation.objects.get(recommendation_name='recommendation_1'))
    self.assertEqual(System.objects.get(system_name='system_csv_32_001').serviceprovider, Serviceprovider.objects.get(serviceprovider_name='serviceprovider_1'))
    self.assertEqual(System.objects.get(system_name='system_csv_32_001').systemtype, Systemtype.objects.get(systemtype_name='systemtype_1'))
    self.assertTrue(System.objects.get(system_name='system_csv_32_001').case.filter(case_name='case_1').exists())
    self.assertTrue(System.objects.get(system_name='system_csv_32_001').company.filter(company_name='company_1').exists())
    self.assertTrue(System.objects.get(system_name='system_csv_32_001').tag.filter(tag_name='AUTO_tag_1').exists())

    # return to test function
    return self

def compare_system_and_attributes_domain_name(self):
    """ compare systems and associated attributes """

    # compare - systems / attributes
    self.assertTrue(System.objects.filter(system_name='system_csv_33_001').exists())
    self.assertTrue(System.objects.filter(system_name='system_csv_33_002').exists())
    self.assertTrue(System.objects.filter(system_name='system_csv_33_003').exists())
    self.assertTrue(Domain.objects.filter(domain_name='domain_33_1').exists())
    self.assertFalse(Domain.objects.filter(domain_name='system_csv_33_002').exists())
    self.assertTrue(Domain.objects.filter(domain_name='domain_33_3').exists())
    self.assertEqual(System.objects.get(system_name='system_csv_33_001').domain, Domain.objects.get(domain_name='domain_33_1'))
    self.assertEqual(System.objects.get(system_name='system_csv_33_002').domain, None)
    self.assertEqual(System.objects.get(system_name='system_csv_33_003').domain, Domain.objects.get(domain_name='domain_33_3'))

    # return to test function
    return self

class SystemImporterFileCsvCheckAttributesViewTestCase(TestCase):
    """ system importer file CSV view tests """

    @classmethod
    def setUpTestData(cls):
        """ one-time setup """

        """ create objects """

        # create users
        test_user = User.objects.create_user(username='testuser_system_importer_file_csv_check_attributes', password='vlQnN2tg9HVGyyyIvezt')
        User.objects.create_user(username='message_user', password='POPKkir2A2biti52AYJG')

        # create objects
        analysisstatus_1 = Analysisstatus.objects.create(analysisstatus_name='analysisstatus_1')
        systemstatus_1 = Systemstatus.objects.create(systemstatus_name='systemstatus_1')

        """ set config with fixed values """

        # build local path with test files
        csv_import_path = os.path.join(BASE_DIR, 'dfirtrack_main/tests/system_importer/system_importer_file_csv_files/')

        # set fixed config values
        system_importer_file_csv_config_model = SystemImporterFileCsvConfigModel.objects.get(system_importer_file_csv_config_name='SystemImporterFileCsvConfig')
        system_importer_file_csv_config_model.csv_headline = False
        system_importer_file_csv_config_model.csv_import_path = csv_import_path
        system_importer_file_csv_config_model.csv_import_username = test_user
        system_importer_file_csv_config_model.csv_default_systemstatus = systemstatus_1
        system_importer_file_csv_config_model.csv_default_analysisstatus = analysisstatus_1
        system_importer_file_csv_config_model.csv_default_tagfree_systemstatus = systemstatus_1
        system_importer_file_csv_config_model.csv_default_tagfree_analysisstatus = analysisstatus_1
        system_importer_file_csv_config_model.csv_tag_lock_systemstatus = 'LOCK_SYSTEMSTATUS'
        system_importer_file_csv_config_model.csv_tag_lock_analysisstatus = 'LOCK_ANALYSISSTATUS'
        system_importer_file_csv_config_model.csv_field_delimiter = 'field_comma'
        system_importer_file_csv_config_model.csv_text_quote = 'text_double_quotation_marks'
        system_importer_file_csv_config_model.csv_ip_delimiter = 'ip_semicolon'
        system_importer_file_csv_config_model.csv_tag_delimiter = 'tag_space'

        # save config
        system_importer_file_csv_config_model.save()

    """ faulty system (system_name) """

    def test_system_importer_file_csv_check_attributes_cron_faulty_systems(self):
        """ test importer view """

        # change config
        set_config_column_system(2)
        # change config
        set_csv_import_filename('system_importer_file_csv_testfile_31_faulty_system.csv')

        # mock timezone.now()
        t_1 = datetime(2021, 3, 8, 18, 5, tzinfo=timezone.utc)
        with patch.object(timezone, 'now', return_value=t_1):

            # execute cron job / scheduled task
            system_cron()

        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_check_attributes', password='vlQnN2tg9HVGyyyIvezt')
        # get response
        response = self.client.get('/system/')
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare - user 1
        self.assertEqual(str(response.context['user']), 'testuser_system_importer_file_csv_check_attributes')
        self.assertEqual(messages[0].message, 'System CSV importer: created: 3 | updated: 0 | skipped: 3 | multiple: 0 [2021-03-08 18:05:00 - 2021-03-08 18:05:00]')
        self.assertEqual(messages[0].level_tag, 'success')
        # switch user context
        self.client.logout()
        self.client.login(username='message_user', password='POPKkir2A2biti52AYJG')
        # get response
        response = self.client.get('/system/')
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare - user 2
        self.assertEqual(str(response.context['user']), 'message_user')
        self.assertEqual(messages[0].message, 'System CSV importer: created: 3 | updated: 0 | skipped: 3 | multiple: 0 [2021-03-08 18:05:00 - 2021-03-08 18:05:00]')
        self.assertEqual(messages[0].level_tag, 'success')
        # compare - systems / attributes
        self = compare_system_and_attributes_faulty_systems(self)

    def test_system_importer_file_csv_check_attributes_instant_faulty_systems(self):
        """ test importer view """

        # change config
        set_config_column_system(2)
        # change config
        set_csv_import_filename('system_importer_file_csv_testfile_31_faulty_system.csv')

        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_check_attributes', password='vlQnN2tg9HVGyyyIvezt')
        # create url
        destination = urllib.parse.quote('/system/', safe='/')
        # get response
        response = self.client.get('/system/importer/file/csv/instant/', follow=True)
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare - meta
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)
        # compare - messages
        self = compare_messages_faulty_systems(self, messages)
        # compare - systems / attributes
        self = compare_system_and_attributes_faulty_systems(self)

    def test_system_importer_file_csv_check_attributes_upload_post_faulty_systems(self):
        """ test importer view """

        # change config
        set_config_column_system(2)
        # change config
        set_csv_import_filename('system_importer_file_csv_testfile_31_faulty_system.csv')

        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_check_attributes', password='vlQnN2tg9HVGyyyIvezt')
        # open upload file
        systemcsv = open(os.path.join(BASE_DIR, 'dfirtrack_main/tests/system_importer/system_importer_file_csv_files/system_importer_file_csv_testfile_31_faulty_system.csv'), 'r')
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
        self = compare_messages_faulty_systems(self, messages)
        # compare - systems / attributes
        self = compare_system_and_attributes_faulty_systems(self)
        # close file
        systemcsv.close()

    """ faulty attributes (faulty values in CSV) """

    def test_system_importer_file_csv_check_attributes_cron_faulty_attributes(self):
        """ test importer view """

        # change config
        set_config_check_attributes_csv()
        # change config
        set_csv_import_filename('system_importer_file_csv_testfile_32_faulty_attributes.csv')

        # mock timezone.now()
        t_2 = datetime(2021, 3, 8, 18, 10, tzinfo=timezone.utc)
        with patch.object(timezone, 'now', return_value=t_2):

            # execute cron job / scheduled task
            system_cron()

        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_check_attributes', password='vlQnN2tg9HVGyyyIvezt')
        # get response
        response = self.client.get('/system/')
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare - user 1
        self.assertEqual(str(response.context['user']), 'testuser_system_importer_file_csv_check_attributes')
        self.assertEqual(messages[0].message, 'System CSV importer: created: 4 | updated: 0 | skipped: 0 | multiple: 0 [2021-03-08 18:10:00 - 2021-03-08 18:10:00]')
        self.assertEqual(messages[0].level_tag, 'success')
        # switch user context
        self.client.logout()
        self.client.login(username='message_user', password='POPKkir2A2biti52AYJG')
        # get response
        response = self.client.get('/system/')
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare - user 2
        self.assertEqual(str(response.context['user']), 'message_user')
        self.assertEqual(messages[0].message, 'System CSV importer: created: 4 | updated: 0 | skipped: 0 | multiple: 0 [2021-03-08 18:10:00 - 2021-03-08 18:10:00]')
        self.assertEqual(messages[0].level_tag, 'success')
        # compare - systems / attributes
        self = compare_system_and_attributes_csv(self)

    def test_system_importer_file_csv_check_attributes_instant_faulty_attributes(self):
        """ test importer view """

        # change config
        set_config_check_attributes_csv()
        # change config
        set_csv_import_filename('system_importer_file_csv_testfile_32_faulty_attributes.csv')

        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_check_attributes', password='vlQnN2tg9HVGyyyIvezt')
        # create url
        destination = urllib.parse.quote('/system/', safe='/')
        # get response
        response = self.client.get('/system/importer/file/csv/instant/', follow=True)
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare - meta
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)
        # compare - messages
        self = compare_messages_csv(self, messages)
        # compare - systems / attributes
        self = compare_system_and_attributes_csv(self)

    def test_system_importer_file_csv_check_attributes_upload_post_faulty_attributes(self):
        """ test importer view """

        # change config
        set_config_check_attributes_csv()

        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_check_attributes', password='vlQnN2tg9HVGyyyIvezt')
        # open upload file
        systemcsv = open(os.path.join(BASE_DIR, 'dfirtrack_main/tests/system_importer/system_importer_file_csv_files/system_importer_file_csv_testfile_32_faulty_attributes.csv'), 'r')
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
        self = compare_messages_csv(self, messages)
        # compare - systems / attributes
        self = compare_system_and_attributes_csv(self)
        # close file
        systemcsv.close()

    """ domain name (same as hostname) """

    def test_system_importer_file_csv_check_attributes_cron_domain_name(self):
        """ test importer view """

        # change config
        set_config_check_attributes_domain_name()
        # change config
        set_csv_import_filename('system_importer_file_csv_testfile_33_domain_name.csv')

        # mock timezone.now()
        t_4 = datetime(2021, 3, 8, 18, 20, tzinfo=timezone.utc)
        with patch.object(timezone, 'now', return_value=t_4):

            # execute cron job / scheduled task
            system_cron()

        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_check_attributes', password='vlQnN2tg9HVGyyyIvezt')
        # get response
        response = self.client.get('/system/')
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare - user 1
        self.assertEqual(str(response.context['user']), 'testuser_system_importer_file_csv_check_attributes')
        self.assertEqual(messages[0].message, 'System CSV importer: created: 3 | updated: 0 | skipped: 0 | multiple: 0 [2021-03-08 18:20:00 - 2021-03-08 18:20:00]')
        self.assertEqual(messages[0].level_tag, 'success')
        # switch user context
        self.client.logout()
        self.client.login(username='message_user', password='POPKkir2A2biti52AYJG')
        # get response
        response = self.client.get('/system/')
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare - user 2
        self.assertEqual(str(response.context['user']), 'message_user')
        self.assertEqual(messages[0].message, 'System CSV importer: created: 3 | updated: 0 | skipped: 0 | multiple: 0 [2021-03-08 18:20:00 - 2021-03-08 18:20:00]')
        self.assertEqual(messages[0].level_tag, 'success')
        # compare - systems / attributes
        self = compare_system_and_attributes_domain_name(self)

    def test_system_importer_file_csv_check_attributes_instant_domain_name(self):
        """ test importer view """

        # change config
        set_config_check_attributes_domain_name()
        # change config
        set_csv_import_filename('system_importer_file_csv_testfile_33_domain_name.csv')

        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_check_attributes', password='vlQnN2tg9HVGyyyIvezt')
        # create url
        destination = urllib.parse.quote('/system/', safe='/')
        # get response
        response = self.client.get('/system/importer/file/csv/instant/', follow=True)
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare - meta
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)
        # compare - messages
        self = compare_messages_domain_name(self, messages)
        # compare - systems / attributes
        self = compare_system_and_attributes_domain_name(self)

    def test_system_importer_file_csv_check_attributes_upload_post_domain_name(self):
        """ test importer view """

        # change config
        set_config_check_attributes_domain_name()

        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_check_attributes', password='vlQnN2tg9HVGyyyIvezt')
        # open upload file
        systemcsv = open(os.path.join(BASE_DIR, 'dfirtrack_main/tests/system_importer/system_importer_file_csv_files/system_importer_file_csv_testfile_33_domain_name.csv'), 'r')
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
        self = compare_messages_domain_name(self, messages)
        # compare - systems / attributes
        self = compare_system_and_attributes_domain_name(self)
        # close file
        systemcsv.close()
