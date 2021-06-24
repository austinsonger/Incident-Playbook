from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.test import TestCase
from dfirtrack.settings import BASE_DIR
from dfirtrack_config.models import SystemImporterFileCsvConfigModel
from dfirtrack_main.importer.file.csv import system_cron
from dfirtrack_main.models import Analysisstatus, Case, Company, Dnsname, Domain, Location, Os, Reason, Recommendation, Serviceprovider, Systemstatus, Systemtype, Tag, Tagcolor
from dfirtrack_main.tests.system_importer.config_functions import set_config_check_config_attributes_column_fields_numeric_values
from dfirtrack_main.tests.system_importer.config_functions import set_config_check_config_attributes_column_choice_vs_default_single_error
from dfirtrack_main.tests.system_importer.config_functions import set_config_check_config_attributes_column_choice_vs_default_multiple_errors_1
from dfirtrack_main.tests.system_importer.config_functions import set_config_check_config_attributes_column_choice_vs_default_multiple_errors_2
from dfirtrack_main.tests.system_importer.config_functions import set_config_check_config_attributes_tagfree_choices
from dfirtrack_main.tests.system_importer.config_functions import set_config_check_config_attributes_column_fields_equal_values
from dfirtrack_main.tests.system_importer.config_functions import set_config_check_config_attributes_remove_choices
import os
import urllib.parse


def compare_messages_column_fields_numeric_values(self, messages):
    """ compare messages """

    # set counter
    message_counter = 0

    # compare - message
    self.assertEqual(messages[message_counter].message, '`CSV_COLUMN_SYSTEM` is outside the allowed range. Check config!')
    self.assertEqual(messages[message_counter].level_tag, 'error')
    message_counter += 1
    self.assertEqual(messages[message_counter].message, '`CSV_COLUMN_IP` is outside the allowed range. Check config!')
    self.assertEqual(messages[message_counter].level_tag, 'error')
    message_counter += 1
    self.assertEqual(messages[message_counter].message, '`CSV_COLUMN_DNSNAME` is outside the allowed range. Check config!')
    self.assertEqual(messages[message_counter].level_tag, 'error')
    message_counter += 1
    self.assertEqual(messages[message_counter].message, '`CSV_COLUMN_DOMAIN` is outside the allowed range. Check config!')
    self.assertEqual(messages[message_counter].level_tag, 'error')
    message_counter += 1
    self.assertEqual(messages[message_counter].message, '`CSV_COLUMN_LOCATION` is outside the allowed range. Check config!')
    self.assertEqual(messages[message_counter].level_tag, 'error')
    message_counter += 1
    self.assertEqual(messages[message_counter].message, '`CSV_COLUMN_OS` is outside the allowed range. Check config!')
    self.assertEqual(messages[message_counter].level_tag, 'error')
    message_counter += 1
    self.assertEqual(messages[message_counter].message, '`CSV_COLUMN_REASON` is outside the allowed range. Check config!')
    self.assertEqual(messages[message_counter].level_tag, 'error')
    message_counter += 1
    self.assertEqual(messages[message_counter].message, '`CSV_COLUMN_RECOMMENDATION` is outside the allowed range. Check config!')
    self.assertEqual(messages[message_counter].level_tag, 'error')
    message_counter += 1
    self.assertEqual(messages[message_counter].message, '`CSV_COLUMN_SERVICEPROVIDER` is outside the allowed range. Check config!')
    self.assertEqual(messages[message_counter].level_tag, 'error')
    message_counter += 1
    self.assertEqual(messages[message_counter].message, '`CSV_COLUMN_SYSTEMTYPE` is outside the allowed range. Check config!')
    self.assertEqual(messages[message_counter].level_tag, 'error')
    message_counter += 1
    self.assertEqual(messages[message_counter].message, '`CSV_COLUMN_CASE` is outside the allowed range. Check config!')
    self.assertEqual(messages[message_counter].level_tag, 'error')
    message_counter += 1
    self.assertEqual(messages[message_counter].message, '`CSV_COLUMN_COMPANY` is outside the allowed range. Check config!')
    self.assertEqual(messages[message_counter].level_tag, 'error')
    message_counter += 1
    self.assertEqual(messages[message_counter].message, '`CSV_COLUMN_TAG` is outside the allowed range. Check config!')
    self.assertEqual(messages[message_counter].level_tag, 'error')
    message_counter += 1

    # return to test function
    return self

class SystemImporterFileCsvCheckConfigAttributesViewTestCase(TestCase):
    """ system importer file CSV view tests """

    @classmethod
    def setUpTestData(cls):
        """ one-time setup """

        """ create objects """

        # create users
        test_user = User.objects.create_user(username='testuser_system_importer_file_csv_check_config_attributes', password='VgnTh4qkYZH61F5YArC7')
        User.objects.create_user(username='message_user', password='POPKkir2A2biti52AYJG')

        # create objects
        analysisstatus_1 = Analysisstatus.objects.create(analysisstatus_name='analysisstatus_1')
        Case.objects.create(
            case_name='case_1',
            case_is_incident=True,
            case_created_by_user_id=test_user,
        )
        Company.objects.create(company_name='company_1')
        Dnsname.objects.create(dnsname_name='dnsname_1')
        Domain.objects.create(domain_name='domain_1')
        Location.objects.create(location_name='location_1')
        Os.objects.create(os_name='os_1')
        Reason.objects.create(reason_name='reason_1')
        Recommendation.objects.create(recommendation_name='recommendation_1')
        Serviceprovider.objects.create(serviceprovider_name='serviceprovider_1')
        systemstatus_1 = Systemstatus.objects.create(systemstatus_name='systemstatus_1')
        Systemtype.objects.create(systemtype_name='systemtype_1')
        tagcolor_1 = Tagcolor.objects.create(tagcolor_name='tagcolor_1')
        Tag.objects.create(
            tag_name='tag_1',
            tagcolor=tagcolor_1,
        )

        """ set config with fixed values """

        # build local path with test files
        csv_import_path = os.path.join(BASE_DIR, 'dfirtrack_main/tests/system_importer/system_importer_file_csv_files/')
        csv_import_filename = 'system_importer_file_csv_testfile_01_minimal_double_quotation.csv'

        # set fixed config values
        system_importer_file_csv_config_model = SystemImporterFileCsvConfigModel.objects.get(system_importer_file_csv_config_name='SystemImporterFileCsvConfig')
        system_importer_file_csv_config_model.csv_headline = False
        system_importer_file_csv_config_model.csv_import_path = csv_import_path
        system_importer_file_csv_config_model.csv_import_filename = csv_import_filename
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

    @classmethod
    def setUp(cls):
        """ setup in advance of every test """

        """ clean non-mandatory values which may set by other tests """

        # get config
        system_importer_file_csv_config_model = SystemImporterFileCsvConfigModel.objects.get(system_importer_file_csv_config_name='SystemImporterFileCsvConfig')

        # (re)set config values
        system_importer_file_csv_config_model.csv_column_system = 1
        system_importer_file_csv_config_model.csv_skip_existing_system = False
        system_importer_file_csv_config_model.csv_remove_systemstatus = False
        system_importer_file_csv_config_model.csv_remove_analysisstatus = False
        system_importer_file_csv_config_model.csv_choice_tagfree_systemstatus = False
        system_importer_file_csv_config_model.csv_choice_tagfree_analysisstatus = False
        system_importer_file_csv_config_model.csv_choice_ip = False
        system_importer_file_csv_config_model.csv_column_ip = None
        system_importer_file_csv_config_model.csv_remove_ip = False
        system_importer_file_csv_config_model.csv_choice_dnsname = False
        system_importer_file_csv_config_model.csv_column_dnsname = None
        system_importer_file_csv_config_model.csv_default_dnsname = None
        system_importer_file_csv_config_model.csv_remove_dnsname = False
        system_importer_file_csv_config_model.csv_choice_domain = False
        system_importer_file_csv_config_model.csv_column_domain = None
        system_importer_file_csv_config_model.csv_default_domain = None
        system_importer_file_csv_config_model.csv_remove_domain = False
        system_importer_file_csv_config_model.csv_choice_location = False
        system_importer_file_csv_config_model.csv_column_location = None
        system_importer_file_csv_config_model.csv_default_location = None
        system_importer_file_csv_config_model.csv_remove_location = False
        system_importer_file_csv_config_model.csv_choice_os = False
        system_importer_file_csv_config_model.csv_column_os = None
        system_importer_file_csv_config_model.csv_default_os = None
        system_importer_file_csv_config_model.csv_remove_os = False
        system_importer_file_csv_config_model.csv_choice_reason = False
        system_importer_file_csv_config_model.csv_column_reason = None
        system_importer_file_csv_config_model.csv_default_reason = None
        system_importer_file_csv_config_model.csv_remove_reason = False
        system_importer_file_csv_config_model.csv_choice_recommendation = False
        system_importer_file_csv_config_model.csv_column_recommendation = None
        system_importer_file_csv_config_model.csv_default_recommendation = None
        system_importer_file_csv_config_model.csv_remove_recommendation = False
        system_importer_file_csv_config_model.csv_choice_serviceprovider = False
        system_importer_file_csv_config_model.csv_column_serviceprovider = None
        system_importer_file_csv_config_model.csv_default_serviceprovider = None
        system_importer_file_csv_config_model.csv_remove_serviceprovider = False
        system_importer_file_csv_config_model.csv_choice_systemtype = False
        system_importer_file_csv_config_model.csv_column_systemtype = None
        system_importer_file_csv_config_model.csv_default_systemtype = None
        system_importer_file_csv_config_model.csv_remove_systemtype = False
        system_importer_file_csv_config_model.csv_choice_case = False
        system_importer_file_csv_config_model.csv_column_case = None
        system_importer_file_csv_config_model.csv_default_case.clear()
        system_importer_file_csv_config_model.csv_remove_case = False
        system_importer_file_csv_config_model.csv_choice_company = False
        system_importer_file_csv_config_model.csv_column_company = None
        system_importer_file_csv_config_model.csv_default_company.clear()
        system_importer_file_csv_config_model.csv_remove_company = False
        system_importer_file_csv_config_model.csv_choice_tag = False
        system_importer_file_csv_config_model.csv_column_tag = None
        system_importer_file_csv_config_model.csv_default_tag.clear()
        system_importer_file_csv_config_model.csv_remove_tag = 'tag_remove_prefix'
        system_importer_file_csv_config_model.csv_tag_prefix = 'AUTO'
        system_importer_file_csv_config_model.csv_tag_prefix_delimiter = 'tag_prefix_underscore'

        # save config
        system_importer_file_csv_config_model.save()

    """ check numeric values of column fields for range """

    def test_system_importer_file_csv_check_config_attributes_create_cron_column_fields_numeric_values(self):
        """ test importer view """

        # change config
        set_config_check_config_attributes_column_fields_numeric_values()

        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_check_config_attributes', password='VgnTh4qkYZH61F5YArC7')
        # create url
        destination = urllib.parse.quote('/system/', safe='/')
        # get response
        response = self.client.get('/system/importer/file/csv/cron/', follow=True)
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare - meta
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)
        # compare - message
        self = compare_messages_column_fields_numeric_values(self, messages)

    def test_system_importer_file_csv_check_config_attributes_cron_column_fields_numeric_values(self):
        """ test importer view """

        # change config
        set_config_check_config_attributes_column_fields_numeric_values()

        # execute cron job / scheduled task
        system_cron()
        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_check_config_attributes', password='VgnTh4qkYZH61F5YArC7')
        # get response
        response = self.client.get('/system/')
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare
        self.assertEqual(str(response.context['user']), 'testuser_system_importer_file_csv_check_config_attributes')
        self.assertEqual(messages[0].message, '[Scheduled task CSV system importer] There was an error within the configuration. Check config!')
        self.assertEqual(messages[0].level_tag, 'error')
        # switch user context
        self.client.logout()
        self.client.login(username='message_user', password='POPKkir2A2biti52AYJG')
        # get response
        response = self.client.get('/system/')
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare
        self.assertEqual(str(response.context['user']), 'message_user')
        self.assertEqual(messages[0].message, '[Scheduled task CSV system importer] There was an error within the configuration. Check config!')
        self.assertEqual(messages[0].level_tag, 'error')

    def test_system_importer_file_csv_check_config_attributes_instant_column_fields_numeric_values(self):
        """ test importer view """

        # change config
        set_config_check_config_attributes_column_fields_numeric_values()

        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_check_config_attributes', password='VgnTh4qkYZH61F5YArC7')
        # create url
        destination = urllib.parse.quote('/system/', safe='/')
        # get response
        response = self.client.get('/system/importer/file/csv/instant/', follow=True)
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare - meta
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)
        # compare - message
        self = compare_messages_column_fields_numeric_values(self, messages)

    def test_system_importer_file_csv_check_config_attributes_upload_get_column_fields_numeric_values(self):
        """ test importer view """

        # change config
        set_config_check_config_attributes_column_fields_numeric_values()

        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_check_config_attributes', password='VgnTh4qkYZH61F5YArC7')
        # create url
        destination = urllib.parse.quote('/system/', safe='/')
        # get response
        response = self.client.get('/system/importer/file/csv/upload/', follow=True)
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare - meta
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)
        # compare - message
        self = compare_messages_column_fields_numeric_values(self, messages)

    def test_system_importer_file_csv_check_config_attributes_upload_post_column_fields_numeric_values(self):
        """ test importer view """

        # change config
        set_config_check_config_attributes_column_fields_numeric_values()

        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_check_config_attributes', password='VgnTh4qkYZH61F5YArC7')
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
        # compare - meta
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)
        # compare - message
        self = compare_messages_column_fields_numeric_values(self, messages)
        # close file
        systemcsv.close()

    """ check choice and column vs. default (single error) """

    def test_system_importer_file_csv_check_config_attributes_create_cron_column_choive_vs_default_single_error(self):
        """ test importer view """

        # change config
        set_config_check_config_attributes_column_choice_vs_default_single_error()

        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_check_config_attributes', password='VgnTh4qkYZH61F5YArC7')
        # create url
        destination = urllib.parse.quote('/system/', safe='/')
        # get response
        response = self.client.get('/system/importer/file/csv/cron/', follow=True)
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)
        self.assertEqual(messages[0].message, 'There was 1 error regarding attributes. Check config!')
        self.assertEqual(messages[0].level_tag, 'error')

    def test_system_importer_file_csv_check_config_attributes_cron_column_choive_vs_default_single_error(self):
        """ test importer view """

        # change config
        set_config_check_config_attributes_column_choice_vs_default_single_error()

        # execute cron job / scheduled task
        system_cron()
        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_check_config_attributes', password='VgnTh4qkYZH61F5YArC7')
        # get response
        response = self.client.get('/system/')
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare
        self.assertEqual(str(response.context['user']), 'testuser_system_importer_file_csv_check_config_attributes')
        self.assertEqual(messages[0].message, '[Scheduled task CSV system importer] There was an error within the configuration. Check config!')
        self.assertEqual(messages[0].level_tag, 'error')
        # switch user context
        self.client.logout()
        self.client.login(username='message_user', password='POPKkir2A2biti52AYJG')
        # get response
        response = self.client.get('/system/')
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare
        self.assertEqual(str(response.context['user']), 'message_user')
        self.assertEqual(messages[0].message, '[Scheduled task CSV system importer] There was an error within the configuration. Check config!')
        self.assertEqual(messages[0].level_tag, 'error')

    def test_system_importer_file_csv_check_config_attributes_instant_column_choive_vs_default_single_error(self):
        """ test importer view """

        # change config
        set_config_check_config_attributes_column_choice_vs_default_single_error()

        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_check_config_attributes', password='VgnTh4qkYZH61F5YArC7')
        # create url
        destination = urllib.parse.quote('/system/', safe='/')
        # get response
        response = self.client.get('/system/importer/file/csv/instant/', follow=True)
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)
        self.assertEqual(messages[0].message, 'There was 1 error regarding attributes. Check config!')
        self.assertEqual(messages[0].level_tag, 'error')

    def test_system_importer_file_csv_check_config_attributes_upload_get_column_choive_vs_default_single_error(self):
        """ test importer view """

        # change config
        set_config_check_config_attributes_column_choice_vs_default_single_error()

        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_check_config_attributes', password='VgnTh4qkYZH61F5YArC7')
        # create url
        destination = urllib.parse.quote('/system/', safe='/')
        # get response
        response = self.client.get('/system/importer/file/csv/upload/', follow=True)
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)
        self.assertEqual(messages[0].message, 'There was 1 error regarding attributes. Check config!')
        self.assertEqual(messages[0].level_tag, 'error')

    def test_system_importer_file_csv_check_config_attributes_upload_post_column_choive_vs_default_single_error(self):
        """ test importer view """

        # change config
        set_config_check_config_attributes_column_choice_vs_default_single_error()

        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_check_config_attributes', password='VgnTh4qkYZH61F5YArC7')
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
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)
        self.assertEqual(messages[0].message, 'There was 1 error regarding attributes. Check config!')
        self.assertEqual(messages[0].level_tag, 'error')
        # close file
        systemcsv.close()

    """ check choice and column vs. default (multiple errors 1) """

    def test_system_importer_file_csv_check_config_attributes_create_cron_column_choive_vs_default_multiple_errors_1(self):
        """ test importer view """

        # change config
        set_config_check_config_attributes_column_choice_vs_default_multiple_errors_1()

        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_check_config_attributes', password='VgnTh4qkYZH61F5YArC7')
        # create url
        destination = urllib.parse.quote('/system/', safe='/')
        # get response
        response = self.client.get('/system/importer/file/csv/cron/', follow=True)
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)
        self.assertEqual(messages[0].message, 'There were 23 errors regarding attributes. Check config!')
        self.assertEqual(messages[0].level_tag, 'error')

    def test_system_importer_file_csv_check_config_attributes_cron_column_choive_vs_default_multiple_errors_1(self):
        """ test importer view """

        # change config
        set_config_check_config_attributes_column_choice_vs_default_multiple_errors_1()

        # execute cron job / scheduled task
        system_cron()
        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_check_config_attributes', password='VgnTh4qkYZH61F5YArC7')
        # get response
        response = self.client.get('/system/')
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare
        self.assertEqual(str(response.context['user']), 'testuser_system_importer_file_csv_check_config_attributes')
        self.assertEqual(messages[0].message, '[Scheduled task CSV system importer] There was an error within the configuration. Check config!')
        self.assertEqual(messages[0].level_tag, 'error')
        # switch user context
        self.client.logout()
        self.client.login(username='message_user', password='POPKkir2A2biti52AYJG')
        # get response
        response = self.client.get('/system/')
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare
        self.assertEqual(str(response.context['user']), 'message_user')
        self.assertEqual(messages[0].message, '[Scheduled task CSV system importer] There was an error within the configuration. Check config!')
        self.assertEqual(messages[0].level_tag, 'error')

    def test_system_importer_file_csv_check_config_attributes_instant_column_choive_vs_default_multiple_errors_1(self):
        """ test importer view """

        # change config
        set_config_check_config_attributes_column_choice_vs_default_multiple_errors_1()

        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_check_config_attributes', password='VgnTh4qkYZH61F5YArC7')
        # create url
        destination = urllib.parse.quote('/system/', safe='/')
        # get response
        response = self.client.get('/system/importer/file/csv/instant/', follow=True)
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)
        self.assertEqual(messages[0].message, 'There were 23 errors regarding attributes. Check config!')
        self.assertEqual(messages[0].level_tag, 'error')

    def test_system_importer_file_csv_check_config_attributes_upload_get_column_choive_vs_default_multiple_errors_1(self):
        """ test importer view """

        # change config
        set_config_check_config_attributes_column_choice_vs_default_multiple_errors_1()

        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_check_config_attributes', password='VgnTh4qkYZH61F5YArC7')
        # create url
        destination = urllib.parse.quote('/system/', safe='/')
        # get response
        response = self.client.get('/system/importer/file/csv/upload/', follow=True)
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)
        self.assertEqual(messages[0].message, 'There were 23 errors regarding attributes. Check config!')
        self.assertEqual(messages[0].level_tag, 'error')

    def test_system_importer_file_csv_check_config_attributes_upload_post_column_choive_vs_default_multiple_errors_1(self):
        """ test importer view """

        # change config
        set_config_check_config_attributes_column_choice_vs_default_multiple_errors_1()

        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_check_config_attributes', password='VgnTh4qkYZH61F5YArC7')
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
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)
        self.assertEqual(messages[0].message, 'There were 23 errors regarding attributes. Check config!')
        self.assertEqual(messages[0].level_tag, 'error')
        # close file
        systemcsv.close()

    """ check choice and column vs. default (multiple errors 2) """

    def test_system_importer_file_csv_check_config_attributes_create_cron_column_choive_vs_default_multiple_errors_2(self):
        """ test importer view """

        # change config
        set_config_check_config_attributes_column_choice_vs_default_multiple_errors_2()

        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_check_config_attributes', password='VgnTh4qkYZH61F5YArC7')
        # create url
        destination = urllib.parse.quote('/system/', safe='/')
        # get response
        response = self.client.get('/system/importer/file/csv/cron/', follow=True)
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)
        self.assertEqual(messages[0].message, 'There were 23 errors regarding attributes. Check config!')
        self.assertEqual(messages[0].level_tag, 'error')

    def test_system_importer_file_csv_check_config_attributes_cron_column_choive_vs_default_multiple_errors_2(self):
        """ test importer view """

        # change config
        set_config_check_config_attributes_column_choice_vs_default_multiple_errors_2()

        # execute cron job / scheduled task
        system_cron()
        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_check_config_attributes', password='VgnTh4qkYZH61F5YArC7')
        # get response
        response = self.client.get('/system/')
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare
        self.assertEqual(str(response.context['user']), 'testuser_system_importer_file_csv_check_config_attributes')
        self.assertEqual(messages[0].message, '[Scheduled task CSV system importer] There was an error within the configuration. Check config!')
        self.assertEqual(messages[0].level_tag, 'error')
        # switch user context
        self.client.logout()
        self.client.login(username='message_user', password='POPKkir2A2biti52AYJG')
        # get response
        response = self.client.get('/system/')
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare
        self.assertEqual(str(response.context['user']), 'message_user')
        self.assertEqual(messages[0].message, '[Scheduled task CSV system importer] There was an error within the configuration. Check config!')
        self.assertEqual(messages[0].level_tag, 'error')

    def test_system_importer_file_csv_check_config_attributes_instant_column_choive_vs_default_multiple_errors_2(self):
        """ test importer view """

        # change config
        set_config_check_config_attributes_column_choice_vs_default_multiple_errors_2()

        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_check_config_attributes', password='VgnTh4qkYZH61F5YArC7')
        # create url
        destination = urllib.parse.quote('/system/', safe='/')
        # get response
        response = self.client.get('/system/importer/file/csv/instant/', follow=True)
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)
        self.assertEqual(messages[0].message, 'There were 23 errors regarding attributes. Check config!')
        self.assertEqual(messages[0].level_tag, 'error')

    def test_system_importer_file_csv_check_config_attributes_upload_get_column_choive_vs_default_multiple_errors_2(self):
        """ test importer view """

        # change config
        set_config_check_config_attributes_column_choice_vs_default_multiple_errors_2()

        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_check_config_attributes', password='VgnTh4qkYZH61F5YArC7')
        # create url
        destination = urllib.parse.quote('/system/', safe='/')
        # get response
        response = self.client.get('/system/importer/file/csv/upload/', follow=True)
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)
        self.assertEqual(messages[0].message, 'There were 23 errors regarding attributes. Check config!')
        self.assertEqual(messages[0].level_tag, 'error')

    def test_system_importer_file_csv_check_config_attributes_upload_post_column_choive_vs_default_multiple_errors_2(self):
        """ test importer view """

        # change config
        set_config_check_config_attributes_column_choice_vs_default_multiple_errors_2()

        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_check_config_attributes', password='VgnTh4qkYZH61F5YArC7')
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
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)
        self.assertEqual(messages[0].message, 'There were 23 errors regarding attributes. Check config!')
        self.assertEqual(messages[0].level_tag, 'error')
        # close file
        systemcsv.close()

    """ check tag prefix and delimiter in combination with choice, column and default """

    def test_system_importer_file_csv_check_config_attributes_create_cron_tag_prefix_and_delimiter(self):
        """ test importer view """

        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_check_config_attributes', password='VgnTh4qkYZH61F5YArC7')
        # create url
        destination = urllib.parse.quote('/system/', safe='/')

        """ CSV chosen and prefix and / or prefix delimiter not set """

        # change config
        system_importer_file_csv_config_model = SystemImporterFileCsvConfigModel.objects.get(system_importer_file_csv_config_name='SystemImporterFileCsvConfig')
        system_importer_file_csv_config_model.csv_choice_tag = True
        system_importer_file_csv_config_model.csv_column_tag = 2
        system_importer_file_csv_config_model.csv_tag_prefix = None
        system_importer_file_csv_config_model.csv_tag_prefix_delimiter = 'tag_prefix_underscore'
        system_importer_file_csv_config_model.csv_remove_tag = 'tag_remove_none'
        system_importer_file_csv_config_model.save()
        system_importer_file_csv_config_model.csv_default_tag.clear()
        # get response
        response = self.client.get('/system/importer/file/csv/cron/', follow=True)
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)
        self.assertEqual(messages[0].message, 'Choose prefix and delimiter for tag import from CSV to distinguish between manual set tags.')
        self.assertEqual(messages[0].level_tag, 'error')
        # change config
        system_importer_file_csv_config_model = SystemImporterFileCsvConfigModel.objects.get(system_importer_file_csv_config_name='SystemImporterFileCsvConfig')
        system_importer_file_csv_config_model.csv_choice_tag = True
        system_importer_file_csv_config_model.csv_column_tag = 2
        system_importer_file_csv_config_model.csv_tag_prefix = 'AUTO'
        system_importer_file_csv_config_model.csv_tag_prefix_delimiter = None
        system_importer_file_csv_config_model.csv_remove_tag = 'tag_remove_none'
        system_importer_file_csv_config_model.save()
        system_importer_file_csv_config_model.csv_default_tag.clear()
        # get response
        response = self.client.get('/system/importer/file/csv/cron/', follow=True)
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)
        self.assertEqual(messages[0].message, 'Choose prefix and delimiter for tag import from CSV to distinguish between manual set tags.')
        self.assertEqual(messages[0].level_tag, 'error')

        """ DB chosen and prefix and / or prefix delimiter chosen """

        # get object
        tag_1 = Tag.objects.get(tag_name='tag_1')
        # change config
        system_importer_file_csv_config_model = SystemImporterFileCsvConfigModel.objects.get(system_importer_file_csv_config_name='SystemImporterFileCsvConfig')
        system_importer_file_csv_config_model.csv_choice_tag = False
        system_importer_file_csv_config_model.csv_column_tag = None
        system_importer_file_csv_config_model.csv_tag_prefix = None
        system_importer_file_csv_config_model.csv_tag_prefix_delimiter = 'tag_prefix_underscore'
        system_importer_file_csv_config_model.csv_remove_tag = 'tag_remove_none'
        system_importer_file_csv_config_model.save()
        system_importer_file_csv_config_model.csv_default_tag.add(tag_1)
        # get response
        response = self.client.get('/system/importer/file/csv/cron/', follow=True)
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)
        self.assertEqual(messages[0].message, 'Prefix and delimiter are not available when setting tags from database.')
        self.assertEqual(messages[0].level_tag, 'error')
        # change config
        system_importer_file_csv_config_model = SystemImporterFileCsvConfigModel.objects.get(system_importer_file_csv_config_name='SystemImporterFileCsvConfig')
        system_importer_file_csv_config_model.csv_choice_tag = False
        system_importer_file_csv_config_model.csv_column_tag = None
        system_importer_file_csv_config_model.csv_tag_prefix = 'AUTO'
        system_importer_file_csv_config_model.csv_tag_prefix_delimiter = None
        system_importer_file_csv_config_model.csv_remove_tag = 'tag_remove_none'
        system_importer_file_csv_config_model.save()
        system_importer_file_csv_config_model.csv_default_tag.add(tag_1)
        # get response
        response = self.client.get('/system/importer/file/csv/cron/', follow=True)
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)
        self.assertEqual(messages[0].message, 'Prefix and delimiter are not available when setting tags from database.')
        self.assertEqual(messages[0].level_tag, 'error')

        """ DB chosen but special option 'tag_remove_prefix' set """

        # get object
        tag_1 = Tag.objects.get(tag_name='tag_1')
        # change config
        system_importer_file_csv_config_model = SystemImporterFileCsvConfigModel.objects.get(system_importer_file_csv_config_name='SystemImporterFileCsvConfig')
        system_importer_file_csv_config_model.csv_choice_tag = False
        system_importer_file_csv_config_model.csv_column_tag = None
        system_importer_file_csv_config_model.csv_tag_prefix = None
        system_importer_file_csv_config_model.csv_tag_prefix_delimiter = None
        system_importer_file_csv_config_model.csv_remove_tag = 'tag_remove_prefix'
        system_importer_file_csv_config_model.save()
        system_importer_file_csv_config_model.csv_default_tag.add(tag_1)
        # get response
        response = self.client.get('/system/importer/file/csv/cron/', follow=True)
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)
        self.assertEqual(messages[0].message, 'Removing tags with prefix is only available when setting tags from CSV.')
        self.assertEqual(messages[0].level_tag, 'error')
        # change config
        system_importer_file_csv_config_model = SystemImporterFileCsvConfigModel.objects.get(system_importer_file_csv_config_name='SystemImporterFileCsvConfig')
        system_importer_file_csv_config_model.csv_choice_tag = False
        system_importer_file_csv_config_model.csv_column_tag = None
        system_importer_file_csv_config_model.csv_tag_prefix = None
        system_importer_file_csv_config_model.csv_tag_prefix_delimiter = None
        system_importer_file_csv_config_model.csv_remove_tag = 'tag_remove_prefix'
        system_importer_file_csv_config_model.save()
        system_importer_file_csv_config_model.csv_default_tag.add(tag_1)
        # get response
        response = self.client.get('/system/importer/file/csv/cron/', follow=True)
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)
        self.assertEqual(messages[0].message, 'Removing tags with prefix is only available when setting tags from CSV.')
        self.assertEqual(messages[0].level_tag, 'error')

    def test_system_importer_file_csv_check_config_attributes_cron_tag_prefix_and_delimiter(self):
        """ test importer view """

        """ CSV chosen and prefix and / or prefix delimiter not set """

        # change config
        system_importer_file_csv_config_model = SystemImporterFileCsvConfigModel.objects.get(system_importer_file_csv_config_name='SystemImporterFileCsvConfig')
        system_importer_file_csv_config_model.csv_choice_tag = True
        system_importer_file_csv_config_model.csv_column_tag = 2
        system_importer_file_csv_config_model.csv_tag_prefix = None
        system_importer_file_csv_config_model.csv_tag_prefix_delimiter = 'tag_prefix_underscore'
        system_importer_file_csv_config_model.csv_remove_tag = 'tag_remove_none'
        system_importer_file_csv_config_model.save()
        system_importer_file_csv_config_model.csv_default_tag.clear()
        # execute cron job / scheduled task
        system_cron()
        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_check_config_attributes', password='VgnTh4qkYZH61F5YArC7')
        # get response
        response = self.client.get('/system/')
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare
        self.assertEqual(str(response.context['user']), 'testuser_system_importer_file_csv_check_config_attributes')
        self.assertEqual(messages[0].message, '[Scheduled task CSV system importer] There was an error within the configuration. Check config!')
        self.assertEqual(messages[0].level_tag, 'error')
        # switch user context
        self.client.logout()
        self.client.login(username='message_user', password='POPKkir2A2biti52AYJG')
        # get response
        response = self.client.get('/system/')
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare
        self.assertEqual(str(response.context['user']), 'message_user')
        self.assertEqual(messages[0].message, '[Scheduled task CSV system importer] There was an error within the configuration. Check config!')
        self.assertEqual(messages[0].level_tag, 'error')
        # change config
        system_importer_file_csv_config_model = SystemImporterFileCsvConfigModel.objects.get(system_importer_file_csv_config_name='SystemImporterFileCsvConfig')
        system_importer_file_csv_config_model.csv_choice_tag = True
        system_importer_file_csv_config_model.csv_column_tag = 2
        system_importer_file_csv_config_model.csv_tag_prefix = 'AUTO'
        system_importer_file_csv_config_model.csv_tag_prefix_delimiter = None
        system_importer_file_csv_config_model.csv_remove_tag = 'tag_remove_none'
        system_importer_file_csv_config_model.save()
        system_importer_file_csv_config_model.csv_default_tag.clear()
        # execute cron job / scheduled task
        system_cron()
        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_check_config_attributes', password='VgnTh4qkYZH61F5YArC7')
        # get response
        response = self.client.get('/system/')
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare
        self.assertEqual(str(response.context['user']), 'testuser_system_importer_file_csv_check_config_attributes')
        self.assertEqual(messages[0].message, '[Scheduled task CSV system importer] There was an error within the configuration. Check config!')
        self.assertEqual(messages[0].level_tag, 'error')
        # switch user context
        self.client.logout()
        self.client.login(username='message_user', password='POPKkir2A2biti52AYJG')
        # get response
        response = self.client.get('/system/')
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare
        self.assertEqual(str(response.context['user']), 'message_user')
        self.assertEqual(messages[0].message, '[Scheduled task CSV system importer] There was an error within the configuration. Check config!')
        self.assertEqual(messages[0].level_tag, 'error')

        """ DB chosen and prefix and / or prefix delimiter chosen """

        # get object
        tag_1 = Tag.objects.get(tag_name='tag_1')
        # change config
        system_importer_file_csv_config_model = SystemImporterFileCsvConfigModel.objects.get(system_importer_file_csv_config_name='SystemImporterFileCsvConfig')
        system_importer_file_csv_config_model.csv_choice_tag = False
        system_importer_file_csv_config_model.csv_column_tag = None
        system_importer_file_csv_config_model.csv_tag_prefix = None
        system_importer_file_csv_config_model.csv_tag_prefix_delimiter = 'tag_prefix_underscore'
        system_importer_file_csv_config_model.csv_remove_tag = 'tag_remove_none'
        system_importer_file_csv_config_model.save()
        system_importer_file_csv_config_model.csv_default_tag.add(tag_1)
        # execute cron job / scheduled task
        system_cron()
        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_check_config_attributes', password='VgnTh4qkYZH61F5YArC7')
        # get response
        response = self.client.get('/system/')
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare
        self.assertEqual(str(response.context['user']), 'testuser_system_importer_file_csv_check_config_attributes')
        self.assertEqual(messages[0].message, '[Scheduled task CSV system importer] There was an error within the configuration. Check config!')
        self.assertEqual(messages[0].level_tag, 'error')
        # switch user context
        self.client.logout()
        self.client.login(username='message_user', password='POPKkir2A2biti52AYJG')
        # get response
        response = self.client.get('/system/')
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare
        self.assertEqual(str(response.context['user']), 'message_user')
        self.assertEqual(messages[0].message, '[Scheduled task CSV system importer] There was an error within the configuration. Check config!')
        self.assertEqual(messages[0].level_tag, 'error')
        # change config
        system_importer_file_csv_config_model = SystemImporterFileCsvConfigModel.objects.get(system_importer_file_csv_config_name='SystemImporterFileCsvConfig')
        system_importer_file_csv_config_model.csv_choice_tag = False
        system_importer_file_csv_config_model.csv_column_tag = None
        system_importer_file_csv_config_model.csv_tag_prefix = 'AUTO'
        system_importer_file_csv_config_model.csv_tag_prefix_delimiter = None
        system_importer_file_csv_config_model.csv_remove_tag = 'tag_remove_none'
        system_importer_file_csv_config_model.save()
        system_importer_file_csv_config_model.csv_default_tag.add(tag_1)
        # execute cron job / scheduled task
        system_cron()
        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_check_config_attributes', password='VgnTh4qkYZH61F5YArC7')
        # get response
        response = self.client.get('/system/')
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare
        self.assertEqual(str(response.context['user']), 'testuser_system_importer_file_csv_check_config_attributes')
        self.assertEqual(messages[0].message, '[Scheduled task CSV system importer] There was an error within the configuration. Check config!')
        self.assertEqual(messages[0].level_tag, 'error')
        # switch user context
        self.client.logout()
        self.client.login(username='message_user', password='POPKkir2A2biti52AYJG')
        # get response
        response = self.client.get('/system/')
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare
        self.assertEqual(str(response.context['user']), 'message_user')
        self.assertEqual(messages[0].message, '[Scheduled task CSV system importer] There was an error within the configuration. Check config!')
        self.assertEqual(messages[0].level_tag, 'error')

        """ DB chosen but special option 'tag_remove_prefix' set """

        # get object
        tag_1 = Tag.objects.get(tag_name='tag_1')
        # change config
        system_importer_file_csv_config_model = SystemImporterFileCsvConfigModel.objects.get(system_importer_file_csv_config_name='SystemImporterFileCsvConfig')
        system_importer_file_csv_config_model.csv_choice_tag = False
        system_importer_file_csv_config_model.csv_column_tag = None
        system_importer_file_csv_config_model.csv_tag_prefix = None
        system_importer_file_csv_config_model.csv_tag_prefix_delimiter = None
        system_importer_file_csv_config_model.csv_remove_tag = 'tag_remove_prefix'
        system_importer_file_csv_config_model.save()
        system_importer_file_csv_config_model.csv_default_tag.add(tag_1)
        # execute cron job / scheduled task
        system_cron()
        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_check_config_attributes', password='VgnTh4qkYZH61F5YArC7')
        # get response
        response = self.client.get('/system/')
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare
        self.assertEqual(str(response.context['user']), 'testuser_system_importer_file_csv_check_config_attributes')
        self.assertEqual(messages[0].message, '[Scheduled task CSV system importer] There was an error within the configuration. Check config!')
        self.assertEqual(messages[0].level_tag, 'error')
        # switch user context
        self.client.logout()
        self.client.login(username='message_user', password='POPKkir2A2biti52AYJG')
        # get response
        response = self.client.get('/system/')
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare
        self.assertEqual(str(response.context['user']), 'message_user')
        self.assertEqual(messages[0].message, '[Scheduled task CSV system importer] There was an error within the configuration. Check config!')
        self.assertEqual(messages[0].level_tag, 'error')
        # change config
        system_importer_file_csv_config_model = SystemImporterFileCsvConfigModel.objects.get(system_importer_file_csv_config_name='SystemImporterFileCsvConfig')
        system_importer_file_csv_config_model.csv_choice_tag = False
        system_importer_file_csv_config_model.csv_column_tag = None
        system_importer_file_csv_config_model.csv_tag_prefix = None
        system_importer_file_csv_config_model.csv_tag_prefix_delimiter = None
        system_importer_file_csv_config_model.csv_remove_tag = 'tag_remove_prefix'
        system_importer_file_csv_config_model.save()
        system_importer_file_csv_config_model.csv_default_tag.add(tag_1)
        # execute cron job / scheduled task
        system_cron()
        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_check_config_attributes', password='VgnTh4qkYZH61F5YArC7')
        # get response
        response = self.client.get('/system/')
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare
        self.assertEqual(str(response.context['user']), 'testuser_system_importer_file_csv_check_config_attributes')
        self.assertEqual(messages[0].message, '[Scheduled task CSV system importer] There was an error within the configuration. Check config!')
        self.assertEqual(messages[0].level_tag, 'error')
        # switch user context
        self.client.logout()
        self.client.login(username='message_user', password='POPKkir2A2biti52AYJG')
        # get response
        response = self.client.get('/system/')
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare
        self.assertEqual(str(response.context['user']), 'message_user')
        self.assertEqual(messages[0].message, '[Scheduled task CSV system importer] There was an error within the configuration. Check config!')
        self.assertEqual(messages[0].level_tag, 'error')

    def test_system_importer_file_csv_check_config_attributes_instant_tag_prefix_and_delimiter(self):
        """ test importer view """

        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_check_config_attributes', password='VgnTh4qkYZH61F5YArC7')
        # create url
        destination = urllib.parse.quote('/system/', safe='/')

        """ CSV chosen and prefix and / or prefix delimiter not set """

        # change config
        system_importer_file_csv_config_model = SystemImporterFileCsvConfigModel.objects.get(system_importer_file_csv_config_name='SystemImporterFileCsvConfig')
        system_importer_file_csv_config_model.csv_choice_tag = True
        system_importer_file_csv_config_model.csv_column_tag = 2
        system_importer_file_csv_config_model.csv_tag_prefix = None
        system_importer_file_csv_config_model.csv_tag_prefix_delimiter = 'tag_prefix_underscore'
        system_importer_file_csv_config_model.csv_remove_tag = 'tag_remove_none'
        system_importer_file_csv_config_model.save()
        system_importer_file_csv_config_model.csv_default_tag.clear()
        # get response
        response = self.client.get('/system/importer/file/csv/instant/', follow=True)
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)
        self.assertEqual(messages[0].message, 'Choose prefix and delimiter for tag import from CSV to distinguish between manual set tags.')
        self.assertEqual(messages[0].level_tag, 'error')
        # change config
        system_importer_file_csv_config_model = SystemImporterFileCsvConfigModel.objects.get(system_importer_file_csv_config_name='SystemImporterFileCsvConfig')
        system_importer_file_csv_config_model.csv_choice_tag = True
        system_importer_file_csv_config_model.csv_column_tag = 2
        system_importer_file_csv_config_model.csv_tag_prefix = 'AUTO'
        system_importer_file_csv_config_model.csv_tag_prefix_delimiter = None
        system_importer_file_csv_config_model.csv_remove_tag = 'tag_remove_none'
        system_importer_file_csv_config_model.save()
        system_importer_file_csv_config_model.csv_default_tag.clear()
        # get response
        response = self.client.get('/system/importer/file/csv/instant/', follow=True)
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)
        self.assertEqual(messages[0].message, 'Choose prefix and delimiter for tag import from CSV to distinguish between manual set tags.')
        self.assertEqual(messages[0].level_tag, 'error')

        """ DB chosen and prefix and / or prefix delimiter chosen """

        # get object
        tag_1 = Tag.objects.get(tag_name='tag_1')
        # change config
        system_importer_file_csv_config_model = SystemImporterFileCsvConfigModel.objects.get(system_importer_file_csv_config_name='SystemImporterFileCsvConfig')
        system_importer_file_csv_config_model.csv_choice_tag = False
        system_importer_file_csv_config_model.csv_column_tag = None
        system_importer_file_csv_config_model.csv_tag_prefix = None
        system_importer_file_csv_config_model.csv_tag_prefix_delimiter = 'tag_prefix_underscore'
        system_importer_file_csv_config_model.csv_remove_tag = 'tag_remove_none'
        system_importer_file_csv_config_model.save()
        system_importer_file_csv_config_model.csv_default_tag.add(tag_1)
        # get response
        response = self.client.get('/system/importer/file/csv/instant/', follow=True)
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)
        self.assertEqual(messages[0].message, 'Prefix and delimiter are not available when setting tags from database.')
        self.assertEqual(messages[0].level_tag, 'error')
        # change config
        system_importer_file_csv_config_model = SystemImporterFileCsvConfigModel.objects.get(system_importer_file_csv_config_name='SystemImporterFileCsvConfig')
        system_importer_file_csv_config_model.csv_choice_tag = False
        system_importer_file_csv_config_model.csv_column_tag = None
        system_importer_file_csv_config_model.csv_tag_prefix = 'AUTO'
        system_importer_file_csv_config_model.csv_tag_prefix_delimiter = None
        system_importer_file_csv_config_model.csv_remove_tag = 'tag_remove_none'
        system_importer_file_csv_config_model.save()
        system_importer_file_csv_config_model.csv_default_tag.add(tag_1)
        # get response
        response = self.client.get('/system/importer/file/csv/instant/', follow=True)
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)
        self.assertEqual(messages[0].message, 'Prefix and delimiter are not available when setting tags from database.')
        self.assertEqual(messages[0].level_tag, 'error')

        """ DB chosen but special option 'tag_remove_prefix' set """

        # get object
        tag_1 = Tag.objects.get(tag_name='tag_1')
        # change config
        system_importer_file_csv_config_model = SystemImporterFileCsvConfigModel.objects.get(system_importer_file_csv_config_name='SystemImporterFileCsvConfig')
        system_importer_file_csv_config_model.csv_choice_tag = False
        system_importer_file_csv_config_model.csv_column_tag = None
        system_importer_file_csv_config_model.csv_tag_prefix = None
        system_importer_file_csv_config_model.csv_tag_prefix_delimiter = None
        system_importer_file_csv_config_model.csv_remove_tag = 'tag_remove_prefix'
        system_importer_file_csv_config_model.save()
        system_importer_file_csv_config_model.csv_default_tag.add(tag_1)
        # get response
        response = self.client.get('/system/importer/file/csv/instant/', follow=True)
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)
        self.assertEqual(messages[0].message, 'Removing tags with prefix is only available when setting tags from CSV.')
        self.assertEqual(messages[0].level_tag, 'error')
        # change config
        system_importer_file_csv_config_model = SystemImporterFileCsvConfigModel.objects.get(system_importer_file_csv_config_name='SystemImporterFileCsvConfig')
        system_importer_file_csv_config_model.csv_choice_tag = False
        system_importer_file_csv_config_model.csv_column_tag = None
        system_importer_file_csv_config_model.csv_tag_prefix = None
        system_importer_file_csv_config_model.csv_tag_prefix_delimiter = None
        system_importer_file_csv_config_model.csv_remove_tag = 'tag_remove_prefix'
        system_importer_file_csv_config_model.save()
        system_importer_file_csv_config_model.csv_default_tag.add(tag_1)
        # get response
        response = self.client.get('/system/importer/file/csv/instant/', follow=True)
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)
        self.assertEqual(messages[0].message, 'Removing tags with prefix is only available when setting tags from CSV.')
        self.assertEqual(messages[0].level_tag, 'error')

    def test_system_importer_file_csv_check_config_attributes_upload_get_tag_prefix_and_delimiter(self):
        """ test importer view """

        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_check_config_attributes', password='VgnTh4qkYZH61F5YArC7')
        # create url
        destination = urllib.parse.quote('/system/', safe='/')

        """ CSV chosen and prefix and / or prefix delimiter not set """

        # change config
        system_importer_file_csv_config_model = SystemImporterFileCsvConfigModel.objects.get(system_importer_file_csv_config_name='SystemImporterFileCsvConfig')
        system_importer_file_csv_config_model.csv_choice_tag = True
        system_importer_file_csv_config_model.csv_column_tag = 2
        system_importer_file_csv_config_model.csv_tag_prefix = None
        system_importer_file_csv_config_model.csv_tag_prefix_delimiter = 'tag_prefix_underscore'
        system_importer_file_csv_config_model.csv_remove_tag = 'tag_remove_none'
        system_importer_file_csv_config_model.save()
        system_importer_file_csv_config_model.csv_default_tag.clear()
        # get response
        response = self.client.get('/system/importer/file/csv/upload/', follow=True)
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)
        self.assertEqual(messages[0].message, 'Choose prefix and delimiter for tag import from CSV to distinguish between manual set tags.')
        self.assertEqual(messages[0].level_tag, 'error')
        # change config
        system_importer_file_csv_config_model = SystemImporterFileCsvConfigModel.objects.get(system_importer_file_csv_config_name='SystemImporterFileCsvConfig')
        system_importer_file_csv_config_model.csv_choice_tag = True
        system_importer_file_csv_config_model.csv_column_tag = 2
        system_importer_file_csv_config_model.csv_tag_prefix = 'AUTO'
        system_importer_file_csv_config_model.csv_tag_prefix_delimiter = None
        system_importer_file_csv_config_model.csv_remove_tag = 'tag_remove_none'
        system_importer_file_csv_config_model.save()
        system_importer_file_csv_config_model.csv_default_tag.clear()
        # get response
        response = self.client.get('/system/importer/file/csv/upload/', follow=True)
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)
        self.assertEqual(messages[0].message, 'Choose prefix and delimiter for tag import from CSV to distinguish between manual set tags.')
        self.assertEqual(messages[0].level_tag, 'error')

        """ DB chosen and prefix and / or prefix delimiter chosen """

        # get object
        tag_1 = Tag.objects.get(tag_name='tag_1')
        # change config
        system_importer_file_csv_config_model = SystemImporterFileCsvConfigModel.objects.get(system_importer_file_csv_config_name='SystemImporterFileCsvConfig')
        system_importer_file_csv_config_model.csv_choice_tag = False
        system_importer_file_csv_config_model.csv_column_tag = None
        system_importer_file_csv_config_model.csv_tag_prefix = None
        system_importer_file_csv_config_model.csv_tag_prefix_delimiter = 'tag_prefix_underscore'
        system_importer_file_csv_config_model.csv_remove_tag = 'tag_remove_none'
        system_importer_file_csv_config_model.save()
        system_importer_file_csv_config_model.csv_default_tag.add(tag_1)
        # get response
        response = self.client.get('/system/importer/file/csv/upload/', follow=True)
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)
        self.assertEqual(messages[0].message, 'Prefix and delimiter are not available when setting tags from database.')
        self.assertEqual(messages[0].level_tag, 'error')
        # change config
        system_importer_file_csv_config_model = SystemImporterFileCsvConfigModel.objects.get(system_importer_file_csv_config_name='SystemImporterFileCsvConfig')
        system_importer_file_csv_config_model.csv_choice_tag = False
        system_importer_file_csv_config_model.csv_column_tag = None
        system_importer_file_csv_config_model.csv_tag_prefix = 'AUTO'
        system_importer_file_csv_config_model.csv_tag_prefix_delimiter = None
        system_importer_file_csv_config_model.csv_remove_tag = 'tag_remove_none'
        system_importer_file_csv_config_model.save()
        system_importer_file_csv_config_model.csv_default_tag.add(tag_1)
        # get response
        response = self.client.get('/system/importer/file/csv/upload/', follow=True)
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)
        self.assertEqual(messages[0].message, 'Prefix and delimiter are not available when setting tags from database.')
        self.assertEqual(messages[0].level_tag, 'error')

        """ DB chosen but special option 'tag_remove_prefix' set """

        # get object
        tag_1 = Tag.objects.get(tag_name='tag_1')
        # change config
        system_importer_file_csv_config_model = SystemImporterFileCsvConfigModel.objects.get(system_importer_file_csv_config_name='SystemImporterFileCsvConfig')
        system_importer_file_csv_config_model.csv_choice_tag = False
        system_importer_file_csv_config_model.csv_column_tag = None
        system_importer_file_csv_config_model.csv_tag_prefix = None
        system_importer_file_csv_config_model.csv_tag_prefix_delimiter = None
        system_importer_file_csv_config_model.csv_remove_tag = 'tag_remove_prefix'
        system_importer_file_csv_config_model.save()
        system_importer_file_csv_config_model.csv_default_tag.add(tag_1)
        # get response
        response = self.client.get('/system/importer/file/csv/upload/', follow=True)
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)
        self.assertEqual(messages[0].message, 'Removing tags with prefix is only available when setting tags from CSV.')
        self.assertEqual(messages[0].level_tag, 'error')
        # change config
        system_importer_file_csv_config_model = SystemImporterFileCsvConfigModel.objects.get(system_importer_file_csv_config_name='SystemImporterFileCsvConfig')
        system_importer_file_csv_config_model.csv_choice_tag = False
        system_importer_file_csv_config_model.csv_column_tag = None
        system_importer_file_csv_config_model.csv_tag_prefix = None
        system_importer_file_csv_config_model.csv_tag_prefix_delimiter = None
        system_importer_file_csv_config_model.csv_remove_tag = 'tag_remove_prefix'
        system_importer_file_csv_config_model.save()
        system_importer_file_csv_config_model.csv_default_tag.add(tag_1)
        # get response
        response = self.client.get('/system/importer/file/csv/upload/', follow=True)
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)
        self.assertEqual(messages[0].message, 'Removing tags with prefix is only available when setting tags from CSV.')
        self.assertEqual(messages[0].level_tag, 'error')

    def test_system_importer_file_csv_check_config_attributes_upload_post_tag_prefix_and_delimiter(self):
        """ test importer view """

        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_check_config_attributes', password='VgnTh4qkYZH61F5YArC7')
        # create url
        destination = urllib.parse.quote('/system/', safe='/')
        # open upload file
        systemcsv = open(os.path.join(BASE_DIR, 'dfirtrack_main/tests/system_importer/system_importer_file_csv_files/system_importer_file_csv_testfile_01_minimal_double_quotation.csv'), 'r')
        # create post data
        data_dict = {
            'systemcsv': systemcsv,
        }

        """ CSV chosen and prefix and / or prefix delimiter not set """

        # change config
        system_importer_file_csv_config_model = SystemImporterFileCsvConfigModel.objects.get(system_importer_file_csv_config_name='SystemImporterFileCsvConfig')
        system_importer_file_csv_config_model.csv_choice_tag = True
        system_importer_file_csv_config_model.csv_column_tag = 2
        system_importer_file_csv_config_model.csv_tag_prefix = None
        system_importer_file_csv_config_model.csv_tag_prefix_delimiter = 'tag_prefix_underscore'
        system_importer_file_csv_config_model.csv_remove_tag = 'tag_remove_none'
        system_importer_file_csv_config_model.save()
        system_importer_file_csv_config_model.csv_default_tag.clear()
        # get response
        response = self.client.post('/system/importer/file/csv/upload/', data_dict)
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)
        self.assertEqual(messages[0].message, 'Choose prefix and delimiter for tag import from CSV to distinguish between manual set tags.')
        self.assertEqual(messages[0].level_tag, 'error')
        # change config
        system_importer_file_csv_config_model = SystemImporterFileCsvConfigModel.objects.get(system_importer_file_csv_config_name='SystemImporterFileCsvConfig')
        system_importer_file_csv_config_model.csv_choice_tag = True
        system_importer_file_csv_config_model.csv_column_tag = 2
        system_importer_file_csv_config_model.csv_tag_prefix = 'AUTO'
        system_importer_file_csv_config_model.csv_tag_prefix_delimiter = None
        system_importer_file_csv_config_model.csv_remove_tag = 'tag_remove_none'
        system_importer_file_csv_config_model.save()
        system_importer_file_csv_config_model.csv_default_tag.clear()
        # get response
        response = self.client.post('/system/importer/file/csv/upload/', data_dict)
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)
        self.assertEqual(messages[0].message, 'Choose prefix and delimiter for tag import from CSV to distinguish between manual set tags.')
        self.assertEqual(messages[0].level_tag, 'error')

        """ DB chosen and prefix and / or prefix delimiter chosen """

        # get object
        tag_1 = Tag.objects.get(tag_name='tag_1')
        # change config
        system_importer_file_csv_config_model = SystemImporterFileCsvConfigModel.objects.get(system_importer_file_csv_config_name='SystemImporterFileCsvConfig')
        system_importer_file_csv_config_model.csv_choice_tag = False
        system_importer_file_csv_config_model.csv_column_tag = None
        system_importer_file_csv_config_model.csv_tag_prefix = None
        system_importer_file_csv_config_model.csv_tag_prefix_delimiter = 'tag_prefix_underscore'
        system_importer_file_csv_config_model.csv_remove_tag = 'tag_remove_none'
        system_importer_file_csv_config_model.save()
        system_importer_file_csv_config_model.csv_default_tag.add(tag_1)
        # get response
        response = self.client.post('/system/importer/file/csv/upload/', data_dict)
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)
        self.assertEqual(messages[0].message, 'Prefix and delimiter are not available when setting tags from database.')
        self.assertEqual(messages[0].level_tag, 'error')
        # change config
        system_importer_file_csv_config_model = SystemImporterFileCsvConfigModel.objects.get(system_importer_file_csv_config_name='SystemImporterFileCsvConfig')
        system_importer_file_csv_config_model.csv_choice_tag = False
        system_importer_file_csv_config_model.csv_column_tag = None
        system_importer_file_csv_config_model.csv_tag_prefix = 'AUTO'
        system_importer_file_csv_config_model.csv_tag_prefix_delimiter = None
        system_importer_file_csv_config_model.csv_remove_tag = 'tag_remove_none'
        system_importer_file_csv_config_model.save()
        system_importer_file_csv_config_model.csv_default_tag.add(tag_1)
        # get response
        response = self.client.post('/system/importer/file/csv/upload/', data_dict)
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)
        self.assertEqual(messages[0].message, 'Prefix and delimiter are not available when setting tags from database.')
        self.assertEqual(messages[0].level_tag, 'error')

        """ DB chosen but special option 'tag_remove_prefix' set """

        # get object
        tag_1 = Tag.objects.get(tag_name='tag_1')
        # change config
        system_importer_file_csv_config_model = SystemImporterFileCsvConfigModel.objects.get(system_importer_file_csv_config_name='SystemImporterFileCsvConfig')
        system_importer_file_csv_config_model.csv_choice_tag = False
        system_importer_file_csv_config_model.csv_column_tag = None
        system_importer_file_csv_config_model.csv_tag_prefix = None
        system_importer_file_csv_config_model.csv_tag_prefix_delimiter = None
        system_importer_file_csv_config_model.csv_remove_tag = 'tag_remove_prefix'
        system_importer_file_csv_config_model.save()
        system_importer_file_csv_config_model.csv_default_tag.add(tag_1)
        # get response
        response = self.client.post('/system/importer/file/csv/upload/', data_dict)
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)
        self.assertEqual(messages[0].message, 'Removing tags with prefix is only available when setting tags from CSV.')
        self.assertEqual(messages[0].level_tag, 'error')
        # change config
        system_importer_file_csv_config_model = SystemImporterFileCsvConfigModel.objects.get(system_importer_file_csv_config_name='SystemImporterFileCsvConfig')
        system_importer_file_csv_config_model.csv_choice_tag = False
        system_importer_file_csv_config_model.csv_column_tag = None
        system_importer_file_csv_config_model.csv_tag_prefix = None
        system_importer_file_csv_config_model.csv_tag_prefix_delimiter = None
        system_importer_file_csv_config_model.csv_remove_tag = 'tag_remove_prefix'
        system_importer_file_csv_config_model.save()
        system_importer_file_csv_config_model.csv_default_tag.add(tag_1)
        # get response
        response = self.client.post('/system/importer/file/csv/upload/', data_dict)
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)
        self.assertEqual(messages[0].message, 'Removing tags with prefix is only available when setting tags from CSV.')
        self.assertEqual(messages[0].level_tag, 'error')

        # close file
        systemcsv.close()

    """ check tagfree choices """

    def test_system_importer_file_csv_check_config_attributes_create_cron_tagfree_choices(self):
        """ test importer view """

        # change config
        set_config_check_config_attributes_tagfree_choices()

        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_check_config_attributes', password='VgnTh4qkYZH61F5YArC7')
        # create url
        destination = urllib.parse.quote('/system/', safe='/')
        # get response
        response = self.client.get('/system/importer/file/csv/cron/', follow=True)
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)
        self.assertEqual(messages[0].message, 'Alternative systemstatus only available with tags from CSV.')
        self.assertEqual(messages[0].level_tag, 'error')
        self.assertEqual(messages[1].message, 'Alternative analysisstatus only available with tags from CSV.')
        self.assertEqual(messages[1].level_tag, 'error')

    def test_system_importer_file_csv_check_config_attributes_cron_tagfree_choices(self):
        """ test importer view """

        # change config
        set_config_check_config_attributes_tagfree_choices()

        # execute cron job / scheduled task
        system_cron()
        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_check_config_attributes', password='VgnTh4qkYZH61F5YArC7')
        # get response
        response = self.client.get('/system/')
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare
        self.assertEqual(str(response.context['user']), 'testuser_system_importer_file_csv_check_config_attributes')
        self.assertEqual(messages[0].message, '[Scheduled task CSV system importer] There was an error within the configuration. Check config!')
        self.assertEqual(messages[0].level_tag, 'error')
        # switch user context
        self.client.logout()
        self.client.login(username='message_user', password='POPKkir2A2biti52AYJG')
        # get response
        response = self.client.get('/system/')
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare
        self.assertEqual(str(response.context['user']), 'message_user')
        self.assertEqual(messages[0].message, '[Scheduled task CSV system importer] There was an error within the configuration. Check config!')
        self.assertEqual(messages[0].level_tag, 'error')

    def test_system_importer_file_csv_check_config_attributes_instant_tagfree_choices(self):
        """ test importer view """

        # change config
        set_config_check_config_attributes_tagfree_choices()

        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_check_config_attributes', password='VgnTh4qkYZH61F5YArC7')
        # create url
        destination = urllib.parse.quote('/system/', safe='/')
        # get response
        response = self.client.get('/system/importer/file/csv/instant/', follow=True)
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)
        self.assertEqual(messages[0].message, 'Alternative systemstatus only available with tags from CSV.')
        self.assertEqual(messages[0].level_tag, 'error')
        self.assertEqual(messages[1].message, 'Alternative analysisstatus only available with tags from CSV.')
        self.assertEqual(messages[1].level_tag, 'error')

    def test_system_importer_file_csv_check_config_attributes_upload_get_tagfree_choices(self):
        """ test importer view """

        # change config
        set_config_check_config_attributes_tagfree_choices()

        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_check_config_attributes', password='VgnTh4qkYZH61F5YArC7')
        # create url
        destination = urllib.parse.quote('/system/', safe='/')
        # get response
        response = self.client.get('/system/importer/file/csv/upload/', follow=True)
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)
        self.assertEqual(messages[0].message, 'Alternative systemstatus only available with tags from CSV.')
        self.assertEqual(messages[0].level_tag, 'error')
        self.assertEqual(messages[1].message, 'Alternative analysisstatus only available with tags from CSV.')
        self.assertEqual(messages[1].level_tag, 'error')

    def test_system_importer_file_csv_check_config_attributes_upload_post_tagfree_choices(self):
        """ test importer view """

        # change config
        set_config_check_config_attributes_tagfree_choices()

        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_check_config_attributes', password='VgnTh4qkYZH61F5YArC7')
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
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)
        self.assertEqual(messages[0].message, 'Alternative systemstatus only available with tags from CSV.')
        self.assertEqual(messages[0].level_tag, 'error')
        self.assertEqual(messages[1].message, 'Alternative analysisstatus only available with tags from CSV.')
        self.assertEqual(messages[1].level_tag, 'error')
        # close file
        systemcsv.close()

    """ check numeric values of column fields for different values """

    def test_system_importer_file_csv_check_config_attributes_create_cron_column_fields_different_values(self):
        """ test importer view """

        # change config
        set_config_check_config_attributes_column_fields_equal_values()

        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_check_config_attributes', password='VgnTh4qkYZH61F5YArC7')
        # create url
        destination = urllib.parse.quote('/system/', safe='/')
        # get response
        response = self.client.get('/system/importer/file/csv/cron/', follow=True)
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)
        self.assertEqual(messages[0].message, 'The columns have to be unique. Check config!')
        self.assertEqual(messages[0].level_tag, 'error')

    def test_system_importer_file_csv_check_config_attributes_cron_column_fields_different_values(self):
        """ test importer view """

        # change config
        set_config_check_config_attributes_column_fields_equal_values()

        # execute cron job / scheduled task
        system_cron()
        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_check_config_attributes', password='VgnTh4qkYZH61F5YArC7')
        # get response
        response = self.client.get('/system/')
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare
        self.assertEqual(str(response.context['user']), 'testuser_system_importer_file_csv_check_config_attributes')
        self.assertEqual(messages[0].message, '[Scheduled task CSV system importer] There was an error within the configuration. Check config!')
        self.assertEqual(messages[0].level_tag, 'error')
        # switch user context
        self.client.logout()
        self.client.login(username='message_user', password='POPKkir2A2biti52AYJG')
        # get response
        response = self.client.get('/system/')
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare
        self.assertEqual(str(response.context['user']), 'message_user')
        self.assertEqual(messages[0].message, '[Scheduled task CSV system importer] There was an error within the configuration. Check config!')
        self.assertEqual(messages[0].level_tag, 'error')

    def test_system_importer_file_csv_check_config_attributes_instant_column_fields_different_values(self):
        """ test importer view """

        # change config
        set_config_check_config_attributes_column_fields_equal_values()

        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_check_config_attributes', password='VgnTh4qkYZH61F5YArC7')
        # create url
        destination = urllib.parse.quote('/system/', safe='/')
        # get response
        response = self.client.get('/system/importer/file/csv/instant/', follow=True)
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)
        self.assertEqual(messages[0].message, 'The columns have to be unique. Check config!')
        self.assertEqual(messages[0].level_tag, 'error')

    def test_system_importer_file_csv_check_config_attributes_upload_get_column_fields_different_values(self):
        """ test importer view """

        # change config
        set_config_check_config_attributes_column_fields_equal_values()

        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_check_config_attributes', password='VgnTh4qkYZH61F5YArC7')
        # create url
        destination = urllib.parse.quote('/system/', safe='/')
        # get response
        response = self.client.get('/system/importer/file/csv/upload/', follow=True)
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)
        self.assertEqual(messages[0].message, 'The columns have to be unique. Check config!')
        self.assertEqual(messages[0].level_tag, 'error')

    def test_system_importer_file_csv_check_config_attributes_upload_post_column_fields_different_values(self):
        """ test importer view """

        # change config
        set_config_check_config_attributes_column_fields_equal_values()

        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_check_config_attributes', password='VgnTh4qkYZH61F5YArC7')
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
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)
        self.assertEqual(messages[0].message, 'The columns have to be unique. Check config!')
        self.assertEqual(messages[0].level_tag, 'error')
        # close file
        systemcsv.close()

    """ check remove conditions in combination with skip condition """

    def test_system_importer_file_csv_check_config_attributes_create_cron_remove_choices(self):
        """ test importer view """

        # change config
        set_config_check_config_attributes_remove_choices()

        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_check_config_attributes', password='VgnTh4qkYZH61F5YArC7')
        # create url
        destination = urllib.parse.quote('/system/', safe='/')
        # get response
        response = self.client.get('/system/importer/file/csv/cron/', follow=True)
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)
        self.assertEqual(messages[0].message, 'There is an error regarding removing existing attributes. Check config!')
        self.assertEqual(messages[0].level_tag, 'error')

    def test_system_importer_file_csv_check_config_attributes_cron_remove_choices(self):
        """ test importer view """

        # change config
        set_config_check_config_attributes_remove_choices()

        # execute cron job / scheduled task
        system_cron()
        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_check_config_attributes', password='VgnTh4qkYZH61F5YArC7')
        # get response
        response = self.client.get('/system/')
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare
        self.assertEqual(str(response.context['user']), 'testuser_system_importer_file_csv_check_config_attributes')
        self.assertEqual(messages[0].message, '[Scheduled task CSV system importer] There was an error within the configuration. Check config!')
        self.assertEqual(messages[0].level_tag, 'error')
        # switch user context
        self.client.logout()
        self.client.login(username='message_user', password='POPKkir2A2biti52AYJG')
        # get response
        response = self.client.get('/system/')
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare
        self.assertEqual(str(response.context['user']), 'message_user')
        self.assertEqual(messages[0].message, '[Scheduled task CSV system importer] There was an error within the configuration. Check config!')
        self.assertEqual(messages[0].level_tag, 'error')

    def test_system_importer_file_csv_check_config_attributes_instant_remove_choices(self):
        """ test importer view """

        # change config
        set_config_check_config_attributes_remove_choices()

        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_check_config_attributes', password='VgnTh4qkYZH61F5YArC7')
        # create url
        destination = urllib.parse.quote('/system/', safe='/')
        # get response
        response = self.client.get('/system/importer/file/csv/instant/', follow=True)
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)
        self.assertEqual(messages[0].message, 'There is an error regarding removing existing attributes. Check config!')
        self.assertEqual(messages[0].level_tag, 'error')

    def test_system_importer_file_csv_check_config_attributes_upload_get_remove_choices(self):
        """ test importer view """

        # change config
        set_config_check_config_attributes_remove_choices()

        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_check_config_attributes', password='VgnTh4qkYZH61F5YArC7')
        # create url
        destination = urllib.parse.quote('/system/', safe='/')
        # get response
        response = self.client.get('/system/importer/file/csv/upload/', follow=True)
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)
        self.assertEqual(messages[0].message, 'There is an error regarding removing existing attributes. Check config!')
        self.assertEqual(messages[0].level_tag, 'error')

    def test_system_importer_file_csv_check_config_attributes_upload_post_remove_choices(self):
        """ test importer view """

        # change config
        set_config_check_config_attributes_remove_choices()

        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_check_config_attributes', password='VgnTh4qkYZH61F5YArC7')
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
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)
        self.assertEqual(messages[0].message, 'There is an error regarding removing existing attributes. Check config!')
        self.assertEqual(messages[0].level_tag, 'error')
        # close file
        systemcsv.close()
