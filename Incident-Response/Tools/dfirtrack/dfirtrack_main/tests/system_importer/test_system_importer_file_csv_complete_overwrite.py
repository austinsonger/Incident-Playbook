from datetime import datetime
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.test import TestCase
from django.utils import timezone
from dfirtrack.settings import BASE_DIR
from dfirtrack_config.models import SystemImporterFileCsvConfigModel
from dfirtrack_main.importer.file.csv import system_cron
from dfirtrack_main.models import Analysisstatus, Case, Company, Dnsname, Domain, Location, Ip, Os, Reason, Recommendation, Serviceprovider, System, Systemstatus, Systemtype, Tag, Tagcolor
from dfirtrack_main.tests.system_importer.config_functions import set_config_complete_attributes_csv, set_config_complete_overwrite_csv, set_csv_import_filename, set_csv_import_path
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

def pre_compare_system_and_attributes_csv(self):
    """ compare systems and associated attributes before action """

    # get objects
    analysisstatus_1 = Analysisstatus.objects.get(analysisstatus_name='analysisstatus_1')
    systemstatus_1 = Systemstatus.objects.get(systemstatus_name='systemstatus_1')

    # compare - existence of objects
    self.assertFalse(Dnsname.objects.filter(dnsname_name='dnsname_41_1').exists())
    self.assertFalse(Domain.objects.filter(domain_name='domain_41_1').exists())
    self.assertFalse(Location.objects.filter(location_name='location_41_1').exists())
    self.assertFalse(Os.objects.filter(os_name='os_41_1').exists())
    self.assertFalse(Ip.objects.filter(ip_ip='127.41.1.1').exists())
    self.assertFalse(Ip.objects.filter(ip_ip='127.41.1.2').exists())
    self.assertFalse(Ip.objects.filter(ip_ip='127.41.1.3').exists())
    self.assertFalse(Ip.objects.filter(ip_ip='127.41.2.1').exists())
    self.assertFalse(Ip.objects.filter(ip_ip='127.41.2.2').exists())
    self.assertFalse(Ip.objects.filter(ip_ip='127.41.2.3').exists())
    self.assertFalse(Ip.objects.filter(ip_ip='127.41.3.1').exists())
    self.assertFalse(Ip.objects.filter(ip_ip='127.41.3.2').exists())
    self.assertFalse(Ip.objects.filter(ip_ip='127.41.3.3').exists())
    self.assertFalse(Reason.objects.filter(reason_name='reason_41_1').exists())
    self.assertFalse(Recommendation.objects.filter(recommendation_name='recommendation_41_1').exists())
    self.assertFalse(Serviceprovider.objects.filter(serviceprovider_name='serviceprovider_41_1').exists())
    self.assertFalse(Systemtype.objects.filter(systemtype_name='systemtype_41_1').exists())
    self.assertFalse(Tag.objects.filter(tag_name='AUTO_tag_41_1').exists())
    self.assertFalse(Tag.objects.filter(tag_name='AUTO_tag_41_2').exists())
    self.assertFalse(Case.objects.filter(case_name='case_41_1').exists())
    self.assertFalse(Company.objects.filter(company_name='company_41_1').exists())
    # get fk objects (to increase the performance for the following comparisons / for better readability)
    dnsname_1 = Dnsname.objects.get(dnsname_name='dnsname_1')
    domain_1 = Domain.objects.get(domain_name='domain_1')
    location_1 = Location.objects.get(location_name='location_1')
    os_1 = Os.objects.get(os_name='os_1')
    reason_1= Reason.objects.get(reason_name='reason_1')
    recommendation_1 = Recommendation.objects.get(recommendation_name='recommendation_1')
    serviceprovider_1 = Serviceprovider.objects.get(serviceprovider_name='serviceprovider_1')
    systemtype_1 = Systemtype.objects.get(systemtype_name='systemtype_1')
    # get systems
    system_csv_41_001 = System.objects.get(system_name='system_csv_41_001')
    system_csv_41_002 = System.objects.get(system_name='system_csv_41_002')
    system_csv_41_003 = System.objects.get(system_name='system_csv_41_003')
    # compare - relations
    self.assertEqual(system_csv_41_001.analysisstatus, analysisstatus_1)
    self.assertEqual(system_csv_41_002.analysisstatus, analysisstatus_1)
    self.assertEqual(system_csv_41_003.analysisstatus, analysisstatus_1)
    self.assertEqual(system_csv_41_001.systemstatus, systemstatus_1)
    self.assertEqual(system_csv_41_002.systemstatus, systemstatus_1)
    self.assertEqual(system_csv_41_003.systemstatus, systemstatus_1)
    self.assertFalse(system_csv_41_001.ip.filter(ip_ip='127.41.1.1').exists())
    self.assertFalse(system_csv_41_001.ip.filter(ip_ip='127.41.1.2').exists())
    self.assertFalse(system_csv_41_001.ip.filter(ip_ip='127.41.1.3').exists())
    self.assertFalse(system_csv_41_002.ip.filter(ip_ip='127.41.2.1').exists())
    self.assertFalse(system_csv_41_002.ip.filter(ip_ip='127.41.2.2').exists())
    self.assertFalse(system_csv_41_002.ip.filter(ip_ip='127.41.2.3').exists())
    self.assertFalse(system_csv_41_003.ip.filter(ip_ip='127.41.3.1').exists())
    self.assertFalse(system_csv_41_003.ip.filter(ip_ip='127.41.3.2').exists())
    self.assertFalse(system_csv_41_003.ip.filter(ip_ip='127.41.3.3').exists())
    self.assertTrue(system_csv_41_001.ip.filter(ip_ip='127.99.1.1').exists())
    self.assertTrue(system_csv_41_002.ip.filter(ip_ip='127.99.2.2').exists())
    self.assertTrue(system_csv_41_003.ip.filter(ip_ip='127.99.3.3').exists())
    self.assertTrue(system_csv_41_001.tag.filter(tag_name='tag_99_1').exists())
    self.assertTrue(system_csv_41_002.tag.filter(tag_name='tag_99_1').exists())
    self.assertTrue(system_csv_41_003.tag.filter(tag_name='tag_99_1').exists())
    self.assertFalse(system_csv_41_001.tag.filter(tag_name='AUTO_tag_41_1').exists())
    self.assertFalse(system_csv_41_001.tag.filter(tag_name='AUTO_tag_41_2').exists())
    self.assertFalse(system_csv_41_002.tag.filter(tag_name='AUTO_tag_41_1').exists())
    self.assertFalse(system_csv_41_002.tag.filter(tag_name='AUTO_tag_41_2').exists())
    self.assertFalse(system_csv_41_003.tag.filter(tag_name='AUTO_tag_41_1').exists())
    self.assertFalse(system_csv_41_003.tag.filter(tag_name='AUTO_tag_41_2').exists())
    self.assertEqual(system_csv_41_001.dnsname, dnsname_1)
    self.assertEqual(system_csv_41_002.dnsname, dnsname_1)
    self.assertEqual(system_csv_41_003.dnsname, dnsname_1)
    self.assertEqual(system_csv_41_001.domain, domain_1)
    self.assertEqual(system_csv_41_002.domain, domain_1)
    self.assertEqual(system_csv_41_003.domain, domain_1)
    self.assertEqual(system_csv_41_001.location, location_1)
    self.assertEqual(system_csv_41_002.location, location_1)
    self.assertEqual(system_csv_41_003.location, location_1)
    self.assertEqual(system_csv_41_001.os, os_1)
    self.assertEqual(system_csv_41_002.os, os_1)
    self.assertEqual(system_csv_41_003.os, os_1)
    self.assertEqual(system_csv_41_001.reason, reason_1)
    self.assertEqual(system_csv_41_002.reason, reason_1)
    self.assertEqual(system_csv_41_003.reason, reason_1)
    self.assertEqual(system_csv_41_001.recommendation, recommendation_1)
    self.assertEqual(system_csv_41_002.recommendation, recommendation_1)
    self.assertEqual(system_csv_41_003.recommendation, recommendation_1)
    self.assertEqual(system_csv_41_001.serviceprovider, serviceprovider_1)
    self.assertEqual(system_csv_41_002.serviceprovider, serviceprovider_1)
    self.assertEqual(system_csv_41_003.serviceprovider, serviceprovider_1)
    self.assertEqual(system_csv_41_001.systemtype, systemtype_1)
    self.assertEqual(system_csv_41_002.systemtype, systemtype_1)
    self.assertEqual(system_csv_41_003.systemtype, systemtype_1)
    self.assertFalse(system_csv_41_001.case.filter(case_name='case_41_1').exists())
    self.assertFalse(system_csv_41_002.case.filter(case_name='case_41_1').exists())
    self.assertFalse(system_csv_41_003.case.filter(case_name='case_41_1').exists())
    self.assertTrue(system_csv_41_001.case.filter(case_name='case_1').exists())
    self.assertTrue(system_csv_41_002.case.filter(case_name='case_1').exists())
    self.assertTrue(system_csv_41_003.case.filter(case_name='case_1').exists())
    self.assertFalse(system_csv_41_001.company.filter(company_name='company_41_1').exists())
    self.assertFalse(system_csv_41_002.company.filter(company_name='company_41_1').exists())
    self.assertFalse(system_csv_41_003.company.filter(company_name='company_41_1').exists())
    self.assertTrue(system_csv_41_001.company.filter(company_name='company_1').exists())
    self.assertTrue(system_csv_41_002.company.filter(company_name='company_1').exists())
    self.assertTrue(system_csv_41_003.company.filter(company_name='company_1').exists())

    # return to test function
    return self

def compare_system_and_attributes_csv(self):
    """ compare systems and associated attributes """

    # get objects
    analysisstatus_2 = Analysisstatus.objects.get(analysisstatus_name='analysisstatus_2')
    systemstatus_2 = Systemstatus.objects.get(systemstatus_name='systemstatus_2')

    # compare - existence of objects
    self.assertTrue(Dnsname.objects.filter(dnsname_name='dnsname_41_1').exists())
    self.assertTrue(Domain.objects.filter(domain_name='domain_41_1').exists())
    self.assertTrue(Location.objects.filter(location_name='location_41_1').exists())
    self.assertTrue(Os.objects.filter(os_name='os_41_1').exists())
    self.assertTrue(Ip.objects.filter(ip_ip='127.41.1.1').exists())
    self.assertTrue(Ip.objects.filter(ip_ip='127.41.1.2').exists())
    self.assertTrue(Ip.objects.filter(ip_ip='127.41.1.3').exists())
    self.assertTrue(Ip.objects.filter(ip_ip='127.41.2.1').exists())
    self.assertTrue(Ip.objects.filter(ip_ip='127.41.2.2').exists())
    self.assertTrue(Ip.objects.filter(ip_ip='127.41.2.3').exists())
    self.assertTrue(Ip.objects.filter(ip_ip='127.41.3.1').exists())
    self.assertTrue(Ip.objects.filter(ip_ip='127.41.3.2').exists())
    self.assertTrue(Ip.objects.filter(ip_ip='127.41.3.3').exists())
    self.assertTrue(Reason.objects.filter(reason_name='reason_41_1').exists())
    self.assertTrue(Recommendation.objects.filter(recommendation_name='recommendation_41_1').exists())
    self.assertTrue(Serviceprovider.objects.filter(serviceprovider_name='serviceprovider_41_1').exists())
    self.assertTrue(Systemtype.objects.filter(systemtype_name='systemtype_41_1').exists())
    self.assertTrue(Tag.objects.filter(tag_name='AUTO_tag_41_1').exists())
    self.assertTrue(Tag.objects.filter(tag_name='AUTO_tag_41_2').exists())
    self.assertTrue(Case.objects.filter(case_name='case_41_1').exists())
    self.assertTrue(Company.objects.filter(company_name='company_41_1').exists())
    # get fk objects (to increase the performance for the following comparisons / for better readability)
    dnsname_41_1 = Dnsname.objects.get(dnsname_name='dnsname_41_1')
    domain_41_1 = Domain.objects.get(domain_name='domain_41_1')
    location_41_1 = Location.objects.get(location_name='location_41_1')
    os_41_1 = Os.objects.get(os_name='os_41_1')
    reason_41_1= Reason.objects.get(reason_name='reason_41_1')
    recommendation_41_1 = Recommendation.objects.get(recommendation_name='recommendation_41_1')
    serviceprovider_41_1 = Serviceprovider.objects.get(serviceprovider_name='serviceprovider_41_1')
    systemtype_41_1 = Systemtype.objects.get(systemtype_name='systemtype_41_1')
    # get systems
    system_csv_41_001 = System.objects.get(system_name='system_csv_41_001')
    system_csv_41_002 = System.objects.get(system_name='system_csv_41_002')
    system_csv_41_003 = System.objects.get(system_name='system_csv_41_003')
    # compare - relations
    self.assertEqual(system_csv_41_001.analysisstatus, analysisstatus_2)
    self.assertEqual(system_csv_41_002.analysisstatus, analysisstatus_2)
    self.assertEqual(system_csv_41_003.analysisstatus, analysisstatus_2)
    self.assertEqual(system_csv_41_001.systemstatus, systemstatus_2)
    self.assertEqual(system_csv_41_002.systemstatus, systemstatus_2)
    self.assertEqual(system_csv_41_003.systemstatus, systemstatus_2)
    self.assertTrue(system_csv_41_001.ip.filter(ip_ip='127.41.1.1').exists())
    self.assertTrue(system_csv_41_001.ip.filter(ip_ip='127.41.1.2').exists())
    self.assertTrue(system_csv_41_001.ip.filter(ip_ip='127.41.1.3').exists())
    self.assertTrue(system_csv_41_002.ip.filter(ip_ip='127.41.2.1').exists())
    self.assertTrue(system_csv_41_002.ip.filter(ip_ip='127.41.2.2').exists())
    self.assertTrue(system_csv_41_002.ip.filter(ip_ip='127.41.2.3').exists())
    self.assertTrue(system_csv_41_003.ip.filter(ip_ip='127.41.3.1').exists())
    self.assertTrue(system_csv_41_003.ip.filter(ip_ip='127.41.3.2').exists())
    self.assertTrue(system_csv_41_003.ip.filter(ip_ip='127.41.3.3').exists())
    self.assertFalse(system_csv_41_001.ip.filter(ip_ip='127.99.1.1').exists())
    self.assertFalse(system_csv_41_002.ip.filter(ip_ip='127.99.2.2').exists())
    self.assertFalse(system_csv_41_003.ip.filter(ip_ip='127.99.3.3').exists())
    self.assertTrue(system_csv_41_001.tag.filter(tag_name='tag_99_1').exists())
    self.assertTrue(system_csv_41_002.tag.filter(tag_name='tag_99_1').exists())
    self.assertTrue(system_csv_41_003.tag.filter(tag_name='tag_99_1').exists())
    self.assertTrue(system_csv_41_001.tag.filter(tag_name='AUTO_tag_41_1').exists())
    self.assertTrue(system_csv_41_001.tag.filter(tag_name='AUTO_tag_41_2').exists())
    self.assertTrue(system_csv_41_002.tag.filter(tag_name='AUTO_tag_41_1').exists())
    self.assertTrue(system_csv_41_002.tag.filter(tag_name='AUTO_tag_41_2').exists())
    self.assertTrue(system_csv_41_003.tag.filter(tag_name='AUTO_tag_41_1').exists())
    self.assertTrue(system_csv_41_003.tag.filter(tag_name='AUTO_tag_41_2').exists())
    self.assertEqual(system_csv_41_001.dnsname, dnsname_41_1)
    self.assertEqual(system_csv_41_002.dnsname, dnsname_41_1)
    self.assertEqual(system_csv_41_003.dnsname, dnsname_41_1)
    self.assertEqual(system_csv_41_001.domain, domain_41_1)
    self.assertEqual(system_csv_41_002.domain, domain_41_1)
    self.assertEqual(system_csv_41_003.domain, domain_41_1)
    self.assertEqual(system_csv_41_001.location, location_41_1)
    self.assertEqual(system_csv_41_002.location, location_41_1)
    self.assertEqual(system_csv_41_003.location, location_41_1)
    self.assertEqual(system_csv_41_001.os, os_41_1)
    self.assertEqual(system_csv_41_002.os, os_41_1)
    self.assertEqual(system_csv_41_003.os, os_41_1)
    self.assertEqual(system_csv_41_001.reason, reason_41_1)
    self.assertEqual(system_csv_41_002.reason, reason_41_1)
    self.assertEqual(system_csv_41_003.reason, reason_41_1)
    self.assertEqual(system_csv_41_001.recommendation, recommendation_41_1)
    self.assertEqual(system_csv_41_002.recommendation, recommendation_41_1)
    self.assertEqual(system_csv_41_003.recommendation, recommendation_41_1)
    self.assertEqual(system_csv_41_001.serviceprovider, serviceprovider_41_1)
    self.assertEqual(system_csv_41_002.serviceprovider, serviceprovider_41_1)
    self.assertEqual(system_csv_41_003.serviceprovider, serviceprovider_41_1)
    self.assertEqual(system_csv_41_001.systemtype, systemtype_41_1)
    self.assertEqual(system_csv_41_002.systemtype, systemtype_41_1)
    self.assertEqual(system_csv_41_003.systemtype, systemtype_41_1)
    self.assertTrue(system_csv_41_001.case.filter(case_name='case_41_1').exists())
    self.assertTrue(system_csv_41_002.case.filter(case_name='case_41_1').exists())
    self.assertTrue(system_csv_41_003.case.filter(case_name='case_41_1').exists())
    self.assertFalse(system_csv_41_001.case.filter(case_name='case_1').exists())
    self.assertFalse(system_csv_41_002.case.filter(case_name='case_1').exists())
    self.assertFalse(system_csv_41_003.case.filter(case_name='case_1').exists())
    self.assertTrue(system_csv_41_001.company.filter(company_name='company_41_1').exists())
    self.assertTrue(system_csv_41_002.company.filter(company_name='company_41_1').exists())
    self.assertTrue(system_csv_41_003.company.filter(company_name='company_41_1').exists())
    self.assertFalse(system_csv_41_001.company.filter(company_name='company_1').exists())
    self.assertFalse(system_csv_41_002.company.filter(company_name='company_1').exists())
    self.assertFalse(system_csv_41_003.company.filter(company_name='company_1').exists())

    # return to test function
    return self

class SystemImporterFileCsvCompleteOverwriteViewTestCase(TestCase):
    """ system importer file CSV view tests """

    @classmethod
    def setUpTestData(cls):
        """ one-time setup """

        # create user
        test_user = User.objects.create_user(username='testuser_system_importer_file_csv_complete_overwrite', password='EeD9m7nMmWTVeUeAAPUC')
        User.objects.create_user(username='message_user', password='AUDrWv4ksLwPhgrDPZ6y')

        """ create objects and add attributes """

        # create status
        analysisstatus_1 = Analysisstatus.objects.create(analysisstatus_name='analysisstatus_1')
        analysisstatus_2 = Analysisstatus.objects.create(analysisstatus_name='analysisstatus_2')
        analysisstatus_3 = Analysisstatus.objects.create(analysisstatus_name='analysisstatus_3')
        systemstatus_1 = Systemstatus.objects.create(systemstatus_name='systemstatus_1')
        systemstatus_2 = Systemstatus.objects.create(systemstatus_name='systemstatus_2')
        systemstatus_3 = Systemstatus.objects.create(systemstatus_name='systemstatus_3')

        # create fk objects
        dnsname_1 = Dnsname.objects.create(dnsname_name='dnsname_1')
        domain_1 = Domain.objects.create(domain_name='domain_1')
        location_1 = Location.objects.create(location_name='location_1')
        os_1 = Os.objects.create(os_name='os_1')
        reason_1 = Reason.objects.create(reason_name='reason_1')
        recommendation_1 = Recommendation.objects.create(recommendation_name='recommendation_1')
        serviceprovider_1 = Serviceprovider.objects.create(serviceprovider_name='serviceprovider_1')
        systemtype_1 = Systemtype.objects.create(systemtype_name='systemtype_1')

        # create systems
        system_csv_41_001 = System.objects.create(
            system_name = 'system_csv_41_001',
            systemstatus = systemstatus_1,
            analysisstatus = analysisstatus_1,
            dnsname = dnsname_1,
            domain = domain_1,
            location = location_1,
            os = os_1,
            reason = reason_1,
            recommendation = recommendation_1,
            serviceprovider = serviceprovider_1,
            systemtype = systemtype_1,
            system_modify_time = timezone.now(),
            system_created_by_user_id = test_user,
            system_modified_by_user_id = test_user,
        )
        system_csv_41_002 = System.objects.create(
            system_name = 'system_csv_41_002',
            systemstatus = systemstatus_1,
            analysisstatus = analysisstatus_1,
            dnsname = dnsname_1,
            domain = domain_1,
            location = location_1,
            os = os_1,
            reason = reason_1,
            recommendation = recommendation_1,
            serviceprovider = serviceprovider_1,
            systemtype = systemtype_1,
            system_modify_time = timezone.now(),
            system_created_by_user_id = test_user,
            system_modified_by_user_id = test_user,
        )
        system_csv_41_003 = System.objects.create(
            system_name = 'system_csv_41_003',
            systemstatus = systemstatus_1,
            analysisstatus = analysisstatus_1,
            dnsname = dnsname_1,
            domain = domain_1,
            location = location_1,
            os = os_1,
            reason = reason_1,
            recommendation = recommendation_1,
            serviceprovider = serviceprovider_1,
            systemtype = systemtype_1,
            system_modify_time = timezone.now(),
            system_created_by_user_id = test_user,
            system_modified_by_user_id = test_user,
        )

        # create / add m2m objects
        case_1 = Case.objects.create(
            case_name='case_1',
            case_is_incident=True,
            case_created_by_user_id=test_user,
        )

        system_csv_41_001.case.add(case_1)
        system_csv_41_002.case.add(case_1)
        system_csv_41_003.case.add(case_1)

        company_1 = Company.objects.create(company_name='company_1')

        system_csv_41_001.company.add(company_1)
        system_csv_41_002.company.add(company_1)
        system_csv_41_003.company.add(company_1)

        ip_1 = Ip.objects.create(ip_ip='127.99.1.1')
        ip_2 = Ip.objects.create(ip_ip='127.99.2.2')
        ip_3 = Ip.objects.create(ip_ip='127.99.3.3')

        system_csv_41_001.ip.add(ip_1)
        system_csv_41_002.ip.add(ip_2)
        system_csv_41_003.ip.add(ip_3)

        tagcolor_1 = Tagcolor.objects.create(tagcolor_name='tagcolor_1')
        tag_99_1 = Tag.objects.create(
            tag_name='tag_99_1',
            tagcolor=tagcolor_1,
        )

        system_csv_41_001.tag.add(tag_99_1)
        system_csv_41_002.tag.add(tag_99_1)
        system_csv_41_003.tag.add(tag_99_1)

        """ config """

        # build local path with test files
        set_csv_import_path(os.path.join(BASE_DIR, 'dfirtrack_main/tests/system_importer/system_importer_file_csv_files/'))

        # set config
        system_importer_file_csv_config_model = SystemImporterFileCsvConfigModel.objects.get(system_importer_file_csv_config_name='SystemImporterFileCsvConfig')
        system_importer_file_csv_config_model.csv_column_system = 1
        system_importer_file_csv_config_model.csv_skip_existing_system = False
        system_importer_file_csv_config_model.csv_headline = False
        system_importer_file_csv_config_model.csv_import_username = test_user
        system_importer_file_csv_config_model.csv_default_systemstatus = systemstatus_2
        system_importer_file_csv_config_model.csv_default_analysisstatus = analysisstatus_2
        system_importer_file_csv_config_model.csv_default_tagfree_systemstatus = systemstatus_3
        system_importer_file_csv_config_model.csv_default_tagfree_analysisstatus = analysisstatus_3
        system_importer_file_csv_config_model.csv_tag_lock_systemstatus = 'LOCK_SYSTEMSTATUS'
        system_importer_file_csv_config_model.csv_tag_lock_analysisstatus = 'LOCK_ANALYSISSTATUS'
        system_importer_file_csv_config_model.csv_remove_tag = 'tag_remove_prefix'
        system_importer_file_csv_config_model.csv_field_delimiter = 'field_comma'
        system_importer_file_csv_config_model.csv_text_quote = 'text_double_quotation_marks'
        system_importer_file_csv_config_model.csv_ip_delimiter = 'ip_semicolon'
        system_importer_file_csv_config_model.csv_tag_delimiter = 'tag_space'
        system_importer_file_csv_config_model.save()

    def test_system_importer_file_csv_complete_overwrite_cron(self):
        """ test importer view """

        # compare before action - systems / attributes
        self = pre_compare_system_and_attributes_csv(self)

        # change config
        set_csv_import_filename('system_importer_file_csv_testfile_41_complete_overwrite.csv')
        # change config
        set_config_complete_attributes_csv()
        # change config
        set_config_complete_overwrite_csv()

        # mock timezone.now()
        t_1 = datetime(2021, 3, 17, 19, 30, tzinfo=timezone.utc)
        with patch.object(timezone, 'now', return_value=t_1):

            # execute cron job / scheduled task
            system_cron()

        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_complete_overwrite', password='EeD9m7nMmWTVeUeAAPUC')
        # get response
        response = self.client.get('/system/')
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare - user 1
        self.assertEqual(str(response.context['user']), 'testuser_system_importer_file_csv_complete_overwrite')
        self.assertEqual(messages[0].message, 'System CSV importer: created: 0 | updated: 3 | skipped: 0 | multiple: 0 [2021-03-17 19:30:00 - 2021-03-17 19:30:00]')
        self.assertEqual(messages[0].level_tag, 'success')
        # switch user context
        self.client.logout()
        self.client.login(username='message_user', password='AUDrWv4ksLwPhgrDPZ6y')
        # get response
        response = self.client.get('/system/')
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare - user 2
        self.assertEqual(str(response.context['user']), 'message_user')
        self.assertEqual(messages[0].message, 'System CSV importer: created: 0 | updated: 3 | skipped: 0 | multiple: 0 [2021-03-17 19:30:00 - 2021-03-17 19:30:00]')
        self.assertEqual(messages[0].level_tag, 'success')
        # compare - systems / attributes
        self = compare_system_and_attributes_csv(self)

    def test_system_importer_file_csv_complete_overwrite_instant(self):
        """ test importer view """

        # compare before action - systems / attributes
        self = pre_compare_system_and_attributes_csv(self)

        # change config
        set_csv_import_filename('system_importer_file_csv_testfile_41_complete_overwrite.csv')
        # change config
        set_config_complete_attributes_csv()
        # change config
        set_config_complete_overwrite_csv()

        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_complete_overwrite', password='EeD9m7nMmWTVeUeAAPUC')
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

    def test_system_importer_file_csv_complete_overwrite_upload_post(self):
        """ test importer view """

        # compare before action - systems / attributes
        self = pre_compare_system_and_attributes_csv(self)

        # change config
        set_config_complete_attributes_csv()
        # change config
        set_config_complete_overwrite_csv()

        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_complete_overwrite', password='EeD9m7nMmWTVeUeAAPUC')
        # open upload file
        systemcsv = open(os.path.join(BASE_DIR, 'dfirtrack_main/tests/system_importer/system_importer_file_csv_files/system_importer_file_csv_testfile_41_complete_overwrite.csv'), 'r')
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
