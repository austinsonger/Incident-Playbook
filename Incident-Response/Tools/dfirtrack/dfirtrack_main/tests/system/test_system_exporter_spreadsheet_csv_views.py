import csv
from datetime import datetime
from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone
from dfirtrack_config.models import MainConfigModel, SystemExporterSpreadsheetCsvConfigModel
from dfirtrack_main.exporter.spreadsheet.csv import system_cron
from dfirtrack_main.models import Analysisstatus, Case, Company, Dnsname, Domain, Ip, Location, Os, Reason, Recommendation, Serviceprovider, System, Systemstatus, Systemtype, Tag, Tagcolor
from mock import patch
import urllib.parse

class SystemExporterSpreadsheetCsvViewTestCase(TestCase):
    """ system exporter spreadsheet CSV view tests """

    @classmethod
    def setUpTestData(cls):

        # create user
        test_user = User.objects.create_user(username='testuser_system_exporter_spreadsheet_csv', password='XJzSzgX2q39OUWluwxoj')

        # create objects
        dnsname_1 = Dnsname.objects.create(dnsname_name='dnsname_1')
        domain_1 = Domain.objects.create(domain_name='domain_1')
        systemstatus_1 = Systemstatus.objects.create(systemstatus_name='systemstatus_1')
        analysisstatus_1 = Analysisstatus.objects.create(analysisstatus_name='analysisstatus_1')
        reason_1 = Reason.objects.create(reason_name='reason_1')
        recommendation_1 = Recommendation.objects.create(recommendation_name='recommendation_1')
        systemtype_1 = Systemtype.objects.create(systemtype_name='systemtype_1')
        ip_1 = Ip.objects.create(ip_ip='127.0.0.1')
        ip_2 = Ip.objects.create(ip_ip='127.0.0.2')
        ip_3 = Ip.objects.create(ip_ip='127.0.0.3')
        os_1 = Os.objects.create(os_name='os_1')
        company_1 = Company.objects.create(company_name='company_1')
        company_2 = Company.objects.create(company_name='company_2')
        company_3 = Company.objects.create(company_name='company_3')
        location_1 = Location.objects.create(location_name='location_1')
        serviceprovider_1 = Serviceprovider.objects.create(serviceprovider_name='serviceprovider_1')
        tagcolor_1 = Tagcolor.objects.create(tagcolor_name='tagcolor_1')
        tag_1 = Tag.objects.create(
            tag_name='tag_1',
            tagcolor=tagcolor_1,
        )
        tag_2 = Tag.objects.create(
            tag_name='tag_2',
            tagcolor=tagcolor_1,
        )
        tag_3 = Tag.objects.create(
            tag_name='tag_3',
            tagcolor=tagcolor_1,
        )
        case_1 = Case.objects.create(
            case_name='case_1',
            case_is_incident=True,
            case_created_by_user_id=test_user,
        )
        case_2 = Case.objects.create(
            case_name='case_2',
            case_is_incident=False,
            case_created_by_user_id=test_user,
        )
        case_3 = Case.objects.create(
            case_name='case_3',
            case_is_incident=False,
            case_created_by_user_id=test_user,
        )

        """ create systems """

        # mock timezone.now()
        t_1 = datetime(2011, 12, 13, 14, 15, tzinfo=timezone.utc)
        with patch.object(timezone, 'now', return_value=t_1):

            # create object with maximum attributes
            system_1 = System.objects.create(
                system_name = 'system_1_all_attributes',
                dnsname = dnsname_1,
                domain = domain_1,
                systemstatus = systemstatus_1,
                analysisstatus = analysisstatus_1,
                reason = reason_1,
                recommendation = recommendation_1,
                systemtype = systemtype_1,
                os = os_1,
                location = location_1,
                serviceprovider = serviceprovider_1,
                system_modify_time = timezone.now(),
                system_created_by_user_id = test_user,
                system_modified_by_user_id = test_user,
            )

            # add many to many attributes
            system_1.ip.add(ip_1)
            system_1.ip.add(ip_2)
            system_1.ip.add(ip_3)
            system_1.company.add(company_1)
            system_1.company.add(company_2)
            system_1.company.add(company_3)
            system_1.tag.add(tag_1)
            system_1.tag.add(tag_2)
            system_1.tag.add(tag_3)
            system_1.case.add(case_1)
            system_1.case.add(case_2)
            system_1.case.add(case_3)

        # mock timezone.now()
        t_2 = datetime(2009, 8, 17, 16, 15, tzinfo=timezone.utc)
        with patch.object(timezone, 'now', return_value=t_2):

            # create object with minimum attributes
            System.objects.create(
                system_name = 'system_2_no_attributes',
                systemstatus = systemstatus_1,
                system_modify_time = timezone.now(),
                system_created_by_user_id = test_user,
                system_modified_by_user_id = test_user,
            )

        # create object that will not be exported
        System.objects.create(
            system_name = 'system_3_not_exported',
            systemstatus = systemstatus_1,
            system_export_spreadsheet = False,
            system_modify_time = timezone.now(),
            system_created_by_user_id = test_user,
            system_modified_by_user_id = test_user,
        )

    def test_system_exporter_spreadsheet_csv_not_logged_in(self):
        """ test exporter view """

        # create url
        destination = '/login/?next=' + urllib.parse.quote('/system/exporter/spreadsheet/csv/system/', safe='')
        # get response
        response = self.client.get('/system/exporter/spreadsheet/csv/system/', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)

    def test_system_exporter_spreadsheet_csv_logged_in(self):
        """ test exporter view """

        # login testuser
        self.client.login(username='testuser_system_exporter_spreadsheet_csv', password='XJzSzgX2q39OUWluwxoj')
        # get response
        response = self.client.get('/system/exporter/spreadsheet/csv/system/')
        # compare
        self.assertEqual(response.status_code, 200)

    def test_system_exporter_spreadsheet_csv_redirect(self):
        """ test exporter view """

        # login testuser
        self.client.login(username='testuser_system_exporter_spreadsheet_csv', password='XJzSzgX2q39OUWluwxoj')
        # create url
        destination = urllib.parse.quote('/system/exporter/spreadsheet/csv/system/', safe='/')
        # get response
        response = self.client.get('/system/exporter/spreadsheet/csv/system', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=301, target_status_code=200)

    def test_system_exporter_spreadsheet_csv_minimal_spreadsheet(self):
        """ test exporter view """

        """ modify config section """

        # get and modify config to show only mandatory columns
        system_exporter_spreadsheet_csv_config_model = SystemExporterSpreadsheetCsvConfigModel(system_exporter_spreadsheet_csv_config_name = 'SystemExporterSpreadsheetCsvConfig')
        system_exporter_spreadsheet_csv_config_model.spread_csv_system_id = False
        system_exporter_spreadsheet_csv_config_model.spread_csv_dnsname = False
        system_exporter_spreadsheet_csv_config_model.spread_csv_domain = False
        system_exporter_spreadsheet_csv_config_model.spread_csv_systemstatus = False
        system_exporter_spreadsheet_csv_config_model.spread_csv_analysisstatus = False
        system_exporter_spreadsheet_csv_config_model.spread_csv_reason = False
        system_exporter_spreadsheet_csv_config_model.spread_csv_recommendation = False
        system_exporter_spreadsheet_csv_config_model.spread_csv_systemtype = False
        system_exporter_spreadsheet_csv_config_model.spread_csv_ip = False
        system_exporter_spreadsheet_csv_config_model.spread_csv_os = False
        system_exporter_spreadsheet_csv_config_model.spread_csv_company = False
        system_exporter_spreadsheet_csv_config_model.spread_csv_location = False
        system_exporter_spreadsheet_csv_config_model.spread_csv_serviceprovider = False
        system_exporter_spreadsheet_csv_config_model.spread_csv_tag = False
        system_exporter_spreadsheet_csv_config_model.spread_csv_case = False
        system_exporter_spreadsheet_csv_config_model.spread_csv_system_create_time = False
        system_exporter_spreadsheet_csv_config_model.spread_csv_system_modify_time = False
        system_exporter_spreadsheet_csv_config_model.save()

        """ call view section """

        # login testuser
        self.client.login(username='testuser_system_exporter_spreadsheet_csv', password='XJzSzgX2q39OUWluwxoj')

        # mock timezone.now()
        t1_now = timezone.now()
        with patch.object(timezone, 'now', return_value=t1_now):

            # get response
            response = self.client.get('/system/exporter/spreadsheet/csv/system/')

        """ get file section """

        # get bytes object from response content
        csv_browser = response.content
        # decode and split at linebreaks
        csv_browser_decoded = csv_browser.decode('utf-8').split('\n')
        # open systemlist as csv object
        csv_reader = csv.reader(csv_browser_decoded, delimiter=',')

        """ compare values section """

        # compare number of rows
        self.assertEqual(len(csv_browser_decoded), 7)     # last linebreak leads to additional line because of split
        # TODO: there must be a more convenient way to random access csv cells directly than iterating over lines and switch for line numbers
        # TODO: like with 'xlrd' for xls files for example
        # set counter
        i = 1
        # compare lines
        for csv_line in csv_reader:
            if csv_line:
                if i == 1:
                    self.assertEqual(csv_line[0], 'System')
                elif i == 2:
                    self.assertEqual(csv_line[0], 'system_1_all_attributes')
                elif i == 3:
                    self.assertEqual(csv_line[0], 'system_2_no_attributes')
                elif i == 5:
                    self.assertEqual(csv_line[0], 'Created:')
                    self.assertEqual(csv_line[1], t1_now.strftime('%Y-%m-%d %H:%M'))
                elif i == 6:
                    self.assertEqual(csv_line[0], 'Created by:')
                    self.assertEqual(csv_line[1], 'testuser_system_exporter_spreadsheet_csv')
            # increase counter
            i += 1

    def test_system_exporter_spreadsheet_csv_complete_spreadsheet(self):
        """ test exporter view """

        """ modify config section """

        # get and modify config to show all columns
        system_exporter_spreadsheet_csv_config_model = SystemExporterSpreadsheetCsvConfigModel(system_exporter_spreadsheet_csv_config_name = 'SystemExporterSpreadsheetCsvConfig')
        system_exporter_spreadsheet_csv_config_model.spread_csv_system_id = True
        system_exporter_spreadsheet_csv_config_model.spread_csv_dnsname = True
        system_exporter_spreadsheet_csv_config_model.spread_csv_domain = True
        system_exporter_spreadsheet_csv_config_model.spread_csv_systemstatus = True
        system_exporter_spreadsheet_csv_config_model.spread_csv_analysisstatus = True
        system_exporter_spreadsheet_csv_config_model.spread_csv_reason = True
        system_exporter_spreadsheet_csv_config_model.spread_csv_recommendation = True
        system_exporter_spreadsheet_csv_config_model.spread_csv_systemtype = True
        system_exporter_spreadsheet_csv_config_model.spread_csv_ip = True
        system_exporter_spreadsheet_csv_config_model.spread_csv_os = True
        system_exporter_spreadsheet_csv_config_model.spread_csv_company = True
        system_exporter_spreadsheet_csv_config_model.spread_csv_location = True
        system_exporter_spreadsheet_csv_config_model.spread_csv_serviceprovider = True
        system_exporter_spreadsheet_csv_config_model.spread_csv_tag = True
        system_exporter_spreadsheet_csv_config_model.spread_csv_case = True
        system_exporter_spreadsheet_csv_config_model.spread_csv_system_create_time = True
        system_exporter_spreadsheet_csv_config_model.spread_csv_system_modify_time = True
        system_exporter_spreadsheet_csv_config_model.save()

        """ call view section """

        # login testuser
        self.client.login(username='testuser_system_exporter_spreadsheet_csv', password='XJzSzgX2q39OUWluwxoj')

        # mock timezone.now()
        t2_now = timezone.now()
        with patch.object(timezone, 'now', return_value=t2_now):

            # get response
            response = self.client.get('/system/exporter/spreadsheet/csv/system/')

        """ get file section """

        # get bytes object from response content
        csv_browser = response.content
        # decode and split at linebreaks
        csv_browser_decoded = csv_browser.decode('utf-8').split('\n')
        # open systemlist as csv object
        csv_reader = csv.reader(csv_browser_decoded, delimiter=',')

        """ prepare objects section """

        # get objects
        system_1 = System.objects.get(system_name='system_1_all_attributes')
        system_2 = System.objects.get(system_name='system_2_no_attributes')

        """ compare values section """

        # compare number of rows
        self.assertEqual(len(csv_browser_decoded), 7)     # last linebreak leads to additional line because of split
        # TODO: there must be a more convenient way to random access csv cells directly than iterating over lines and switch for line numbers
        # TODO: like with 'xlrd' for xls files for example
        # set counter
        i = 1
        # compare lines
        for csv_line in csv_reader:
            if csv_line:
                if i == 1:
                    self.assertEqual(csv_line[0], 'ID')
                    self.assertEqual(csv_line[1], 'System')
                    self.assertEqual(csv_line[2], 'DNS name')
                    self.assertEqual(csv_line[3], 'Domain')
                    self.assertEqual(csv_line[4], 'Systemstatus')
                    self.assertEqual(csv_line[5], 'Analysisstatus')
                    self.assertEqual(csv_line[6], 'Reason')
                    self.assertEqual(csv_line[7], 'Recommendation')
                    self.assertEqual(csv_line[8], 'Systemtype')
                    self.assertEqual(csv_line[9], 'IP')
                    self.assertEqual(csv_line[10], 'OS')
                    self.assertEqual(csv_line[11], 'Company')
                    self.assertEqual(csv_line[12], 'Location')
                    self.assertEqual(csv_line[13], 'Serviceprovider')
                    self.assertEqual(csv_line[14], 'Tag')
                    self.assertEqual(csv_line[15], 'Case')
                    self.assertEqual(csv_line[16], 'Created')
                    self.assertEqual(csv_line[17], 'Modified')
                elif i == 2:
                    self.assertEqual(csv_line[0], str(system_1.system_id))
                    self.assertEqual(csv_line[1], 'system_1_all_attributes')
                    self.assertEqual(csv_line[2], 'dnsname_1')
                    self.assertEqual(csv_line[3], 'domain_1')
                    self.assertEqual(csv_line[4], 'systemstatus_1')
                    self.assertEqual(csv_line[5], 'analysisstatus_1')
                    self.assertEqual(csv_line[6], 'reason_1')
                    self.assertEqual(csv_line[7], 'recommendation_1')
                    self.assertEqual(csv_line[8], 'systemtype_1')
                    self.assertEqual(csv_line[9], '127.0.0.1,127.0.0.2,127.0.0.3')
                    self.assertEqual(csv_line[10], 'os_1')
                    self.assertEqual(csv_line[11], 'company_1,company_2,company_3')
                    self.assertEqual(csv_line[12], 'location_1')
                    self.assertEqual(csv_line[13], 'serviceprovider_1')
                    self.assertEqual(csv_line[14], 'tag_1,tag_2,tag_3')
                    self.assertEqual(csv_line[15], 'case_1,case_2,case_3')
                    self.assertEqual(csv_line[16], '2011-12-13 14:15')
                    self.assertEqual(csv_line[17], '2011-12-13 14:15')
                elif i == 3:
                    self.assertEqual(csv_line[0], str(system_2.system_id))
                    self.assertEqual(csv_line[1], 'system_2_no_attributes')
                    self.assertEqual(csv_line[2], '')
                    self.assertEqual(csv_line[3], '')
                    self.assertEqual(csv_line[4], 'systemstatus_1')
                    self.assertEqual(csv_line[5], '')
                    self.assertEqual(csv_line[6], '')
                    self.assertEqual(csv_line[7], '')
                    self.assertEqual(csv_line[8], '')
                    self.assertEqual(csv_line[9], '')
                    self.assertEqual(csv_line[10], '')
                    self.assertEqual(csv_line[11], '')
                    self.assertEqual(csv_line[12], '')
                    self.assertEqual(csv_line[13], '')
                    self.assertEqual(csv_line[14], '')
                    self.assertEqual(csv_line[15], '')
                    self.assertEqual(csv_line[16], '2009-08-17 16:15')
                    self.assertEqual(csv_line[17], '2009-08-17 16:15')
                elif i == 5:
                    self.assertEqual(csv_line[0], 'Created:')
                    self.assertEqual(csv_line[1], t2_now.strftime('%Y-%m-%d %H:%M'))
                elif i == 6:
                    self.assertEqual(csv_line[0], 'Created by:')
                    self.assertEqual(csv_line[1], 'testuser_system_exporter_spreadsheet_csv')
            # increase counter
            i += 1

    def test_system_exporter_spreadsheet_csv_cron_complete_spreadsheet(self):
        """ test exporter view """

        """ modify config section """

        # get and modify main config
        main_config_model = MainConfigModel.objects.get(main_config_name = 'MainConfig')
        main_config_model.cron_export_path = '/tmp'
        main_config_model.cron_username = 'cron'
        main_config_model.save()

        # get and modify config to show all columns
        system_exporter_spreadsheet_csv_config_model = SystemExporterSpreadsheetCsvConfigModel(system_exporter_spreadsheet_csv_config_name = 'SystemExporterSpreadsheetCsvConfig')
        system_exporter_spreadsheet_csv_config_model.spread_csv_system_id = True
        system_exporter_spreadsheet_csv_config_model.spread_csv_dnsname = True
        system_exporter_spreadsheet_csv_config_model.spread_csv_domain = True
        system_exporter_spreadsheet_csv_config_model.spread_csv_systemstatus = True
        system_exporter_spreadsheet_csv_config_model.spread_csv_analysisstatus = True
        system_exporter_spreadsheet_csv_config_model.spread_csv_reason = True
        system_exporter_spreadsheet_csv_config_model.spread_csv_recommendation = True
        system_exporter_spreadsheet_csv_config_model.spread_csv_systemtype = True
        system_exporter_spreadsheet_csv_config_model.spread_csv_ip = True
        system_exporter_spreadsheet_csv_config_model.spread_csv_os = True
        system_exporter_spreadsheet_csv_config_model.spread_csv_company = True
        system_exporter_spreadsheet_csv_config_model.spread_csv_location = True
        system_exporter_spreadsheet_csv_config_model.spread_csv_serviceprovider = True
        system_exporter_spreadsheet_csv_config_model.spread_csv_tag = True
        system_exporter_spreadsheet_csv_config_model.spread_csv_case = True
        system_exporter_spreadsheet_csv_config_model.spread_csv_system_create_time = True
        system_exporter_spreadsheet_csv_config_model.spread_csv_system_modify_time = True
        system_exporter_spreadsheet_csv_config_model.save()

        """ call view section """

        # mock timezone.now()
        t3_now = timezone.now()
        with patch.object(timezone, 'now', return_value=t3_now):

            # create spreadsheet without GET by directly calling the function
            system_cron()

        """ get file section """

        # refresh config
        main_config_model.refresh_from_db()
        # get time for output file
        filetime = t3_now.strftime('%Y%m%d_%H%M')
        # prepare output file path
        output_file_path = main_config_model.cron_export_path + '/' + filetime + '_systems.csv'
        # open file from temp folder
        csv_disk = open(output_file_path, 'r')
        # open file as csv object
        csv_reader = csv.reader(csv_disk, delimiter=',')

        """ prepare objects section """

        # get objects
        system_1 = System.objects.get(system_name='system_1_all_attributes')
        system_2 = System.objects.get(system_name='system_2_no_attributes')

        """ compare values section """

        # TODO: there must be a more convenient way to random access csv cells directly than iterating over lines and switch for line numbers
        # TODO: like with 'xlrd' for xls files for example
        # set counter
        i = 1
        # compare lines
        for csv_line in csv_reader:
            if csv_line:
                if i == 1:
                    self.assertEqual(csv_line[0], 'ID')
                    self.assertEqual(csv_line[1], 'System')
                    self.assertEqual(csv_line[2], 'DNS name')
                    self.assertEqual(csv_line[3], 'Domain')
                    self.assertEqual(csv_line[4], 'Systemstatus')
                    self.assertEqual(csv_line[5], 'Analysisstatus')
                    self.assertEqual(csv_line[6], 'Reason')
                    self.assertEqual(csv_line[7], 'Recommendation')
                    self.assertEqual(csv_line[8], 'Systemtype')
                    self.assertEqual(csv_line[9], 'IP')
                    self.assertEqual(csv_line[10], 'OS')
                    self.assertEqual(csv_line[11], 'Company')
                    self.assertEqual(csv_line[12], 'Location')
                    self.assertEqual(csv_line[13], 'Serviceprovider')
                    self.assertEqual(csv_line[14], 'Tag')
                    self.assertEqual(csv_line[15], 'Case')
                    self.assertEqual(csv_line[16], 'Created')
                    self.assertEqual(csv_line[17], 'Modified')
                elif i == 2:
                    self.assertEqual(csv_line[0], str(system_1.system_id))
                    self.assertEqual(csv_line[1], 'system_1_all_attributes')
                    self.assertEqual(csv_line[2], 'dnsname_1')
                    self.assertEqual(csv_line[3], 'domain_1')
                    self.assertEqual(csv_line[4], 'systemstatus_1')
                    self.assertEqual(csv_line[5], 'analysisstatus_1')
                    self.assertEqual(csv_line[6], 'reason_1')
                    self.assertEqual(csv_line[7], 'recommendation_1')
                    self.assertEqual(csv_line[8], 'systemtype_1')
                    self.assertEqual(csv_line[9], '127.0.0.1,127.0.0.2,127.0.0.3')
                    self.assertEqual(csv_line[10], 'os_1')
                    self.assertEqual(csv_line[11], 'company_1,company_2,company_3')
                    self.assertEqual(csv_line[12], 'location_1')
                    self.assertEqual(csv_line[13], 'serviceprovider_1')
                    self.assertEqual(csv_line[14], 'tag_1,tag_2,tag_3')
                    self.assertEqual(csv_line[15], 'case_1,case_2,case_3')
                    self.assertEqual(csv_line[16], '2011-12-13 14:15')
                    self.assertEqual(csv_line[17], '2011-12-13 14:15')
                elif i == 3:
                    self.assertEqual(csv_line[0], str(system_2.system_id))
                    self.assertEqual(csv_line[1], 'system_2_no_attributes')
                    self.assertEqual(csv_line[2], '')
                    self.assertEqual(csv_line[3], '')
                    self.assertEqual(csv_line[4], 'systemstatus_1')
                    self.assertEqual(csv_line[5], '')
                    self.assertEqual(csv_line[6], '')
                    self.assertEqual(csv_line[7], '')
                    self.assertEqual(csv_line[8], '')
                    self.assertEqual(csv_line[9], '')
                    self.assertEqual(csv_line[10], '')
                    self.assertEqual(csv_line[11], '')
                    self.assertEqual(csv_line[12], '')
                    self.assertEqual(csv_line[13], '')
                    self.assertEqual(csv_line[14], '')
                    self.assertEqual(csv_line[15], '')
                    self.assertEqual(csv_line[16], '2009-08-17 16:15')
                    self.assertEqual(csv_line[17], '2009-08-17 16:15')
                elif i == 5:
                    self.assertEqual(csv_line[0], 'Created:')
                    self.assertEqual(csv_line[1], t3_now.strftime('%Y-%m-%d %H:%M'))
                elif i == 6:
                    self.assertEqual(csv_line[0], 'Created by:')
                    self.assertEqual(csv_line[1], 'cron')
            # increase counter
            i += 1
        # compare number of rows (needs to be at the end because 'line_num' is some kind of pointer)
        self.assertEqual(csv_reader.line_num, 6)

        # close file
        csv_disk.close()
