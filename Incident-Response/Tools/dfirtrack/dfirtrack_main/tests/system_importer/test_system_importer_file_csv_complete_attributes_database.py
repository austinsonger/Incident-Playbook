from datetime import datetime
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.test import TestCase
from django.utils import timezone
from dfirtrack.settings import BASE_DIR
from dfirtrack_config.models import SystemImporterFileCsvConfigModel
from dfirtrack_main.importer.file.csv import system_cron
from dfirtrack_main.models import Analysisstatus, Case, Company, Dnsname, Domain, Location, Os, Reason, Recommendation, Serviceprovider, System, Systemstatus, Systemtype, Tag, Tagcolor
from dfirtrack_main.tests.system_importer.config_functions import set_config_complete_attributes_database, set_csv_import_filename
from mock import patch
import os
import urllib.parse

def compare_messages_database(self, messages):
    """ compare messages """

    # compare - messages
    self.assertEqual(messages[0].message, '4 systems were created.')
    self.assertEqual(messages[0].level_tag, 'success')

    # return to test function
    return self

def compare_system_and_attributes_database(self):
    """ compare systems and associated attributes """

    # compare - systems
    self.assertTrue(System.objects.filter(system_name='system_csv_08_001').exists())
    self.assertTrue(System.objects.filter(system_name='system_csv_08_002').exists())
    self.assertTrue(System.objects.filter(system_name='system_csv_08_003').exists())
    self.assertTrue(System.objects.filter(system_name='system_csv_08_004').exists())
    # compare - relations
    self.assertTrue(System.objects.get(system_name='system_csv_08_001').case.filter(case_name='case_db_1').exists())
    self.assertTrue(System.objects.get(system_name='system_csv_08_002').case.filter(case_name='case_db_1').exists())
    self.assertTrue(System.objects.get(system_name='system_csv_08_003').case.filter(case_name='case_db_1').exists())
    self.assertTrue(System.objects.get(system_name='system_csv_08_004').case.filter(case_name='case_db_1').exists())
    self.assertTrue(System.objects.get(system_name='system_csv_08_001').company.filter(company_name='company_db_1').exists())
    self.assertTrue(System.objects.get(system_name='system_csv_08_002').company.filter(company_name='company_db_1').exists())
    self.assertTrue(System.objects.get(system_name='system_csv_08_003').company.filter(company_name='company_db_1').exists())
    self.assertTrue(System.objects.get(system_name='system_csv_08_004').company.filter(company_name='company_db_1').exists())
    self.assertEqual(System.objects.get(system_name='system_csv_08_001').dnsname, Dnsname.objects.get(dnsname_name='dnsname_db_1'))
    self.assertEqual(System.objects.get(system_name='system_csv_08_002').dnsname, Dnsname.objects.get(dnsname_name='dnsname_db_1'))
    self.assertEqual(System.objects.get(system_name='system_csv_08_003').dnsname, Dnsname.objects.get(dnsname_name='dnsname_db_1'))
    self.assertEqual(System.objects.get(system_name='system_csv_08_004').dnsname, Dnsname.objects.get(dnsname_name='dnsname_db_1'))
    self.assertEqual(System.objects.get(system_name='system_csv_08_001').domain, Domain.objects.get(domain_name='domain_db_1'))
    self.assertEqual(System.objects.get(system_name='system_csv_08_002').domain, Domain.objects.get(domain_name='domain_db_1'))
    self.assertEqual(System.objects.get(system_name='system_csv_08_003').domain, Domain.objects.get(domain_name='domain_db_1'))
    self.assertEqual(System.objects.get(system_name='system_csv_08_004').domain, Domain.objects.get(domain_name='domain_db_1'))
    self.assertEqual(System.objects.get(system_name='system_csv_08_001').location, Location.objects.get(location_name='location_db_1'))
    self.assertEqual(System.objects.get(system_name='system_csv_08_002').location, Location.objects.get(location_name='location_db_1'))
    self.assertEqual(System.objects.get(system_name='system_csv_08_003').location, Location.objects.get(location_name='location_db_1'))
    self.assertEqual(System.objects.get(system_name='system_csv_08_004').location, Location.objects.get(location_name='location_db_1'))
    self.assertEqual(System.objects.get(system_name='system_csv_08_001').os, Os.objects.get(os_name='os_db_1'))
    self.assertEqual(System.objects.get(system_name='system_csv_08_002').os, Os.objects.get(os_name='os_db_1'))
    self.assertEqual(System.objects.get(system_name='system_csv_08_003').os, Os.objects.get(os_name='os_db_1'))
    self.assertEqual(System.objects.get(system_name='system_csv_08_004').os, Os.objects.get(os_name='os_db_1'))
    self.assertEqual(System.objects.get(system_name='system_csv_08_001').reason, Reason.objects.get(reason_name='reason_db_1'))
    self.assertEqual(System.objects.get(system_name='system_csv_08_002').reason, Reason.objects.get(reason_name='reason_db_1'))
    self.assertEqual(System.objects.get(system_name='system_csv_08_003').reason, Reason.objects.get(reason_name='reason_db_1'))
    self.assertEqual(System.objects.get(system_name='system_csv_08_004').reason, Reason.objects.get(reason_name='reason_db_1'))
    self.assertEqual(System.objects.get(system_name='system_csv_08_001').recommendation, Recommendation.objects.get(recommendation_name='recommendation_db_1'))
    self.assertEqual(System.objects.get(system_name='system_csv_08_002').recommendation, Recommendation.objects.get(recommendation_name='recommendation_db_1'))
    self.assertEqual(System.objects.get(system_name='system_csv_08_003').recommendation, Recommendation.objects.get(recommendation_name='recommendation_db_1'))
    self.assertEqual(System.objects.get(system_name='system_csv_08_004').recommendation, Recommendation.objects.get(recommendation_name='recommendation_db_1'))
    self.assertEqual(System.objects.get(system_name='system_csv_08_001').serviceprovider, Serviceprovider.objects.get(serviceprovider_name='serviceprovider_db_1'))
    self.assertEqual(System.objects.get(system_name='system_csv_08_002').serviceprovider, Serviceprovider.objects.get(serviceprovider_name='serviceprovider_db_1'))
    self.assertEqual(System.objects.get(system_name='system_csv_08_003').serviceprovider, Serviceprovider.objects.get(serviceprovider_name='serviceprovider_db_1'))
    self.assertEqual(System.objects.get(system_name='system_csv_08_004').serviceprovider, Serviceprovider.objects.get(serviceprovider_name='serviceprovider_db_1'))
    self.assertEqual(System.objects.get(system_name='system_csv_08_001').systemtype, Systemtype.objects.get(systemtype_name='systemtype_db_1'))
    self.assertEqual(System.objects.get(system_name='system_csv_08_002').systemtype, Systemtype.objects.get(systemtype_name='systemtype_db_1'))
    self.assertEqual(System.objects.get(system_name='system_csv_08_003').systemtype, Systemtype.objects.get(systemtype_name='systemtype_db_1'))
    self.assertEqual(System.objects.get(system_name='system_csv_08_004').systemtype, Systemtype.objects.get(systemtype_name='systemtype_db_1'))
    self.assertTrue(System.objects.get(system_name='system_csv_08_001').tag.filter(tag_name='tag_db_1').exists())
    self.assertTrue(System.objects.get(system_name='system_csv_08_002').tag.filter(tag_name='tag_db_1').exists())
    self.assertTrue(System.objects.get(system_name='system_csv_08_003').tag.filter(tag_name='tag_db_1').exists())
    self.assertTrue(System.objects.get(system_name='system_csv_08_004').tag.filter(tag_name='tag_db_1').exists())

    # return to test function
    return self

class SystemImporterFileCsvCompleteAttributesDatabaseViewTestCase(TestCase):
    """ system importer file CSV view tests """

    @classmethod
    def setUpTestData(cls):
        """ one-time setup """

        """ create objects """

        # create users
        test_user = User.objects.create_user(username='testuser_system_importer_file_csv_complete_attributes_database', password='ZrPzqC6wBVzHfNvPiSX4')
        User.objects.create_user(username='message_user', password='eL2lekBo8ja7nmxfXcBr')

        # create objects
        analysisstatus_1 = Analysisstatus.objects.create(analysisstatus_name='analysisstatus_1')
        systemstatus_1 = Systemstatus.objects.create(systemstatus_name='systemstatus_1')

        Case.objects.create(
            case_name = 'case_db_1',
            case_is_incident = True,
            case_created_by_user_id=test_user,
        )
        Company.objects.create(company_name='company_db_1')
        Dnsname.objects.create(dnsname_name='dnsname_db_1')
        Domain.objects.create(domain_name='domain_db_1')
        Location.objects.create(location_name='location_db_1')
        Os.objects.create(os_name='os_db_1')
        Reason.objects.create(reason_name='reason_db_1')
        Recommendation.objects.create(recommendation_name='recommendation_db_1')
        Serviceprovider.objects.create(serviceprovider_name='serviceprovider_db_1')
        Systemtype.objects.create(systemtype_name='systemtype_db_1')

        tagcolor_1 = Tagcolor.objects.create(tagcolor_name='tagcolor_1')
        Tag.objects.create(
            tag_name = 'tag_db_1',
            tagcolor = tagcolor_1,
        )

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

    """ database attributes """

    def test_system_importer_file_csv_complete_attributes_database_cron(self):
        """ test importer view """

        # change config
        set_config_complete_attributes_database()
        # change config
        set_csv_import_filename('system_importer_file_csv_testfile_08_complete_database.csv')

        # mock timezone.now()
        t_3 = datetime(2021, 3, 8, 18, 15, tzinfo=timezone.utc)
        with patch.object(timezone, 'now', return_value=t_3):

            # execute cron job / scheduled task
            system_cron()

        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_complete_attributes_database', password='ZrPzqC6wBVzHfNvPiSX4')
        # get response
        response = self.client.get('/system/')
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare - user 1
        self.assertEqual(str(response.context['user']), 'testuser_system_importer_file_csv_complete_attributes_database')
        self.assertEqual(messages[0].message, 'System CSV importer: created: 4 | updated: 0 | skipped: 0 | multiple: 0 [2021-03-08 18:15:00 - 2021-03-08 18:15:00]')
        self.assertEqual(messages[0].level_tag, 'success')
        # switch user context
        self.client.logout()
        self.client.login(username='message_user', password='eL2lekBo8ja7nmxfXcBr')
        # get response
        response = self.client.get('/system/')
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare - user 2
        self.assertEqual(str(response.context['user']), 'message_user')
        self.assertEqual(messages[0].message, 'System CSV importer: created: 4 | updated: 0 | skipped: 0 | multiple: 0 [2021-03-08 18:15:00 - 2021-03-08 18:15:00]')
        self.assertEqual(messages[0].level_tag, 'success')
        # compare - systems / attributes
        self = compare_system_and_attributes_database(self)

    def test_system_importer_file_csv_complete_attributes_database_instant(self):
        """ test importer view """

        # change config
        set_config_complete_attributes_database()
        # change config
        set_csv_import_filename('system_importer_file_csv_testfile_08_complete_database.csv')

        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_complete_attributes_database', password='ZrPzqC6wBVzHfNvPiSX4')
        # create url
        destination = urllib.parse.quote('/system/', safe='/')
        # get response
        response = self.client.get('/system/importer/file/csv/instant/', follow=True)
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare - meta
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)
        # compare - messages
        self = compare_messages_database(self, messages)
        # compare - systems / attributes
        self = compare_system_and_attributes_database(self)

    def test_system_importer_file_csv_complete_attributes_database_upload_post(self):
        """ test importer view """

        # change config
        set_config_complete_attributes_database()

        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_complete_attributes_database', password='ZrPzqC6wBVzHfNvPiSX4')
        # open upload file
        systemcsv = open(os.path.join(BASE_DIR, 'dfirtrack_main/tests/system_importer/system_importer_file_csv_files/system_importer_file_csv_testfile_08_complete_database.csv'), 'r')
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
        self = compare_messages_database(self, messages)
        # compare - systems / attributes
        self = compare_system_and_attributes_database(self)
        # close file
        systemcsv.close()
