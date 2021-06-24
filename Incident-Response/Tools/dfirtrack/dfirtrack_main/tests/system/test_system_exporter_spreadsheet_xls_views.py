from datetime import datetime
from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone
from dfirtrack_config.models import MainConfigModel, SystemExporterSpreadsheetXlsConfigModel
from dfirtrack_main.exporter.spreadsheet.xls import system_cron
from dfirtrack_main.models import Analysisstatus, Case, Company, Dnsname, Domain, Ip, Location, Os, Reason, Recommendation, Serviceprovider, System, Systemstatus, Systemtype, Tag, Tagcolor
from mock import patch
import urllib.parse
import xlrd

class SystemExporterSpreadsheetXlsViewTestCase(TestCase):
    """ system exporter spreadsheet XLS view tests """

    @classmethod
    def setUpTestData(cls):

        # create user
        test_user = User.objects.create_user(username='testuser_system_exporter_spreadsheet_xls', password='AIsOtQ2zchYhNZBfWIHu')

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
        t_1 = datetime(2001, 2, 3, 4, 5, tzinfo=timezone.utc)
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
        t_2 = datetime(2009, 8, 7, 6, 5, tzinfo=timezone.utc)
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

    def test_system_exporter_spreadsheet_xls_not_logged_in(self):
        """ test exporter view """

        # create url
        destination = '/login/?next=' + urllib.parse.quote('/system/exporter/spreadsheet/xls/system/', safe='')
        # get response
        response = self.client.get('/system/exporter/spreadsheet/xls/system/', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)

    def test_system_exporter_spreadsheet_xls_logged_in(self):
        """ test exporter view """

        # login testuser
        self.client.login(username='testuser_system_exporter_spreadsheet_xls', password='AIsOtQ2zchYhNZBfWIHu')
        # get response
        response = self.client.get('/system/exporter/spreadsheet/xls/system/')
        # compare
        self.assertEqual(response.status_code, 200)

    def test_system_exporter_spreadsheet_xls_redirect(self):
        """ test exporter view """

        # login testuser
        self.client.login(username='testuser_system_exporter_spreadsheet_xls', password='AIsOtQ2zchYhNZBfWIHu')
        # create url
        destination = urllib.parse.quote('/system/exporter/spreadsheet/xls/system/', safe='/')
        # get response
        response = self.client.get('/system/exporter/spreadsheet/xls/system', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=301, target_status_code=200)

    def test_system_exporter_spreadsheet_xls_minimal_spreadsheet(self):
        """ test exporter view """

        """ modify config section """

        # get and modify config to show only mandatory columns
        system_exporter_spreadsheet_xls_config_model = SystemExporterSpreadsheetXlsConfigModel(system_exporter_spreadsheet_xls_config_name = 'SystemExporterSpreadsheetXlsConfig')
        system_exporter_spreadsheet_xls_config_model.spread_xls_system_id = False
        system_exporter_spreadsheet_xls_config_model.spread_xls_dnsname = False
        system_exporter_spreadsheet_xls_config_model.spread_xls_domain = False
        system_exporter_spreadsheet_xls_config_model.spread_xls_systemstatus = False
        system_exporter_spreadsheet_xls_config_model.spread_xls_analysisstatus = False
        system_exporter_spreadsheet_xls_config_model.spread_xls_reason = False
        system_exporter_spreadsheet_xls_config_model.spread_xls_recommendation = False
        system_exporter_spreadsheet_xls_config_model.spread_xls_systemtype = False
        system_exporter_spreadsheet_xls_config_model.spread_xls_ip = False
        system_exporter_spreadsheet_xls_config_model.spread_xls_os = False
        system_exporter_spreadsheet_xls_config_model.spread_xls_company = False
        system_exporter_spreadsheet_xls_config_model.spread_xls_location = False
        system_exporter_spreadsheet_xls_config_model.spread_xls_serviceprovider = False
        system_exporter_spreadsheet_xls_config_model.spread_xls_tag = False
        system_exporter_spreadsheet_xls_config_model.spread_xls_case = False
        system_exporter_spreadsheet_xls_config_model.spread_xls_system_create_time = False
        system_exporter_spreadsheet_xls_config_model.spread_xls_system_modify_time = False
        system_exporter_spreadsheet_xls_config_model.spread_xls_worksheet_systemstatus = False
        system_exporter_spreadsheet_xls_config_model.spread_xls_worksheet_analysisstatus = False
        system_exporter_spreadsheet_xls_config_model.spread_xls_worksheet_reason = False
        system_exporter_spreadsheet_xls_config_model.spread_xls_worksheet_recommendation = False
        system_exporter_spreadsheet_xls_config_model.spread_xls_worksheet_tag = False
        system_exporter_spreadsheet_xls_config_model.save()

        """ call view section """

        # login testuser
        self.client.login(username='testuser_system_exporter_spreadsheet_xls', password='AIsOtQ2zchYhNZBfWIHu')

        # mock timezone.now()
        t1_now = timezone.now()
        with patch.object(timezone, 'now', return_value=t1_now):

            # get response
            response = self.client.get('/system/exporter/spreadsheet/xls/system/')

        """ get file section """

        # get file from response content
        xls_browser = response.content
        # open systemlist directly from byte stream
        systemlist = xlrd.open_workbook(file_contents=xls_browser)

        """ prepare objects section """

        # get objects
        system_1 = System.objects.get(system_name='system_1_all_attributes')
        system_2 = System.objects.get(system_name='system_2_no_attributes')

        # get sheets
        sheet_systems = systemlist.sheet_by_name('systems')

        """ compare values section """

        # compare non-available sheets
        self.assertRaises(xlrd.biffh.XLRDError, systemlist.sheet_by_name, sheet_name='systemstatus')
        self.assertRaises(xlrd.biffh.XLRDError, systemlist.sheet_by_name, sheet_name='analysisstatus')
        self.assertRaises(xlrd.biffh.XLRDError, systemlist.sheet_by_name, sheet_name='reasons')
        self.assertRaises(xlrd.biffh.XLRDError, systemlist.sheet_by_name, sheet_name='recommendations')
        self.assertRaises(xlrd.biffh.XLRDError, systemlist.sheet_by_name, sheet_name='tags')
        # compare number of rows and columns
        self.assertEqual(sheet_systems.nrows, 6)
        self.assertEqual(sheet_systems.ncols, 2)
        # compare headlines
        self.assertEqual(sheet_systems.row_values(0), ['System', ''])
        # compare content - system 1
        self.assertEqual(sheet_systems.cell(1,0).value, system_1.system_name)
        # compare content - system 2
        self.assertEqual(sheet_systems.cell(2,0).value, system_2.system_name)
        # compare content - metadata
        self.assertEqual(sheet_systems.cell(4,0).value, 'Created:')
        self.assertEqual(sheet_systems.cell(4,1).value,  t1_now.strftime('%Y-%m-%d %H:%M'))
        self.assertEqual(sheet_systems.cell(5,0).value, 'Created by:')
        self.assertEqual(sheet_systems.cell(5,1).value, 'testuser_system_exporter_spreadsheet_xls')

    def test_system_exporter_spreadsheet_xls_complete_spreadsheet(self):
        """ test exporter view """

        """ modify config section """

        # get and modify config to show all columns and sheets
        system_exporter_spreadsheet_xls_config_model = SystemExporterSpreadsheetXlsConfigModel(system_exporter_spreadsheet_xls_config_name = 'SystemExporterSpreadsheetXlsConfig')
        system_exporter_spreadsheet_xls_config_model.spread_xls_system_id = True
        system_exporter_spreadsheet_xls_config_model.spread_xls_dnsname = True
        system_exporter_spreadsheet_xls_config_model.spread_xls_domain = True
        system_exporter_spreadsheet_xls_config_model.spread_xls_systemstatus = True
        system_exporter_spreadsheet_xls_config_model.spread_xls_analysisstatus = True
        system_exporter_spreadsheet_xls_config_model.spread_xls_reason = True
        system_exporter_spreadsheet_xls_config_model.spread_xls_recommendation = True
        system_exporter_spreadsheet_xls_config_model.spread_xls_systemtype = True
        system_exporter_spreadsheet_xls_config_model.spread_xls_ip = True
        system_exporter_spreadsheet_xls_config_model.spread_xls_os = True
        system_exporter_spreadsheet_xls_config_model.spread_xls_company = True
        system_exporter_spreadsheet_xls_config_model.spread_xls_location = True
        system_exporter_spreadsheet_xls_config_model.spread_xls_serviceprovider = True
        system_exporter_spreadsheet_xls_config_model.spread_xls_tag = True
        system_exporter_spreadsheet_xls_config_model.spread_xls_case = True
        system_exporter_spreadsheet_xls_config_model.spread_xls_system_create_time = True
        system_exporter_spreadsheet_xls_config_model.spread_xls_system_modify_time = True
        system_exporter_spreadsheet_xls_config_model.spread_xls_worksheet_systemstatus = True
        system_exporter_spreadsheet_xls_config_model.spread_xls_worksheet_analysisstatus = True
        system_exporter_spreadsheet_xls_config_model.spread_xls_worksheet_reason = True
        system_exporter_spreadsheet_xls_config_model.spread_xls_worksheet_recommendation = True
        system_exporter_spreadsheet_xls_config_model.spread_xls_worksheet_tag = True
        system_exporter_spreadsheet_xls_config_model.save()

        """ call view section """

        # login testuser
        self.client.login(username='testuser_system_exporter_spreadsheet_xls', password='AIsOtQ2zchYhNZBfWIHu')

        # mock timezone.now()
        t2_now = timezone.now()
        with patch.object(timezone, 'now', return_value=t2_now):

            # get response
            response = self.client.get('/system/exporter/spreadsheet/xls/system/')

        """ get file section """

        # get file from response content
        xls_browser = response.content
        # open systemlist directly from byte stream
        systemlist = xlrd.open_workbook(file_contents=xls_browser)

        """ prepare objects section """

        # get objects
        system_1 = System.objects.get(system_name='system_1_all_attributes')
        system_2 = System.objects.get(system_name='system_2_no_attributes')

        # create lists for easier comparison with whole columns - systemstatus
        systemstatus_id_list = ['ID']
        systemstatus_name_list = ['Systemstatus']
        systemstatus_note_list = ['Note']
        all_systemstatus = Systemstatus.objects.all().order_by('systemstatus_name')
        for systemstatus_object in all_systemstatus:
            # the conversion to float was carried out, because otherwise the return values from the spreadsheet would have had to be converted to int, which would have been more time-consuming
            systemstatus_id_list.append(float(systemstatus_object.systemstatus_id))
            systemstatus_name_list.append(systemstatus_object.systemstatus_name)
            if systemstatus_object.systemstatus_note:
                systemstatus_note_list.append(systemstatus_object.systemstatus_note)
            else:
                systemstatus_note_list.append('')

        # create lists for easier comparison with whole columns - analysisstatus
        analysisstatus_id_list = ['ID']
        analysisstatus_name_list = ['Analysisstatus']
        analysisstatus_note_list = ['Note']
        all_analysisstatus = Analysisstatus.objects.all().order_by('analysisstatus_name')
        for analysisstatus_object in all_analysisstatus:
            # the conversion to float was carried out, because otherwise the return values from the spreadsheet would have had to be converted to int, which would have been more time-consuming
            analysisstatus_id_list.append(float(analysisstatus_object.analysisstatus_id))
            analysisstatus_name_list.append(analysisstatus_object.analysisstatus_name)
            if analysisstatus_object.analysisstatus_note:
                analysisstatus_note_list.append(analysisstatus_object.analysisstatus_note)
            else:
                analysisstatus_note_list.append('')

        # create lists for easier comparison with whole columns - reason
        reason_id_list = ['ID']
        reason_name_list = ['Reason']
        reason_note_list = ['Note']
        all_reason = Reason.objects.all().order_by('reason_name')
        for reason_object in all_reason:
            # the conversion to float was carried out, because otherwise the return values from the spreadsheet would have had to be converted to int, which would have been more time-consuming
            reason_id_list.append(float(reason_object.reason_id))
            reason_name_list.append(reason_object.reason_name)
            if reason_object.reason_note:
                reason_note_list.append(reason_object.reason_note)
            else:
                reason_note_list.append('')

        # create lists for easier comparison with whole columns - recommendation
        recommendation_id_list = ['ID']
        recommendation_name_list = ['Recommendation']
        recommendation_note_list = ['Note']
        all_recommendation = Recommendation.objects.all().order_by('recommendation_name')
        for recommendation_object in all_recommendation:
            # the conversion to float was carried out, because otherwise the return values from the spreadsheet would have had to be converted to int, which would have been more time-consuming
            recommendation_id_list.append(float(recommendation_object.recommendation_id))
            recommendation_name_list.append(recommendation_object.recommendation_name)
            if recommendation_object.recommendation_note:
                recommendation_note_list.append(recommendation_object.recommendation_note)
            else:
                recommendation_note_list.append('')

        # create lists for easier comparison with whole columns - tag
        tag_id_list = ['ID']
        tag_name_list = ['Tag']
        tag_note_list = ['Note']
        all_tag = Tag.objects.all().order_by('tag_name')
        for tag_object in all_tag:
            # the conversion to float was carried out, because otherwise the return values from the spreadsheet would have had to be converted to int, which would have been more time-consuming
            tag_id_list.append(float(tag_object.tag_id))
            tag_name_list.append(tag_object.tag_name)
            if tag_object.tag_note:
                tag_note_list.append(tag_object.tag_note)
            else:
                tag_note_list.append('')

        # get sheets
        sheet_systems = systemlist.sheet_by_name('systems')
        sheet_systemstatus = systemlist.sheet_by_name('systemstatus')
        sheet_analysisstatus = systemlist.sheet_by_name('analysisstatus')
        sheet_reasons = systemlist.sheet_by_name('reasons')
        sheet_recommendations = systemlist.sheet_by_name('recommendations')
        sheet_tags = systemlist.sheet_by_name('tags')

        """ compare values section """

        # compare number of rows and columns
        self.assertEqual(sheet_systems.nrows, 6)
        self.assertEqual(sheet_systems.ncols, 18)
        self.assertEqual(sheet_systemstatus.nrows, 10)
        self.assertEqual(sheet_systemstatus.ncols, 3)
        self.assertEqual(sheet_analysisstatus.nrows, 7)
        self.assertEqual(sheet_analysisstatus.ncols, 3)
        self.assertEqual(sheet_reasons.nrows, 2)
        self.assertEqual(sheet_reasons.ncols, 3)
        self.assertEqual(sheet_recommendations.nrows, 2)
        self.assertEqual(sheet_recommendations.ncols, 3)
        self.assertEqual(sheet_tags.nrows, 9)
        self.assertEqual(sheet_tags.ncols, 3)
        # compare headlines
        self.assertEqual(sheet_systems.row_values(0), ['ID', 'System', 'DNS name', 'Domain', 'Systemstatus', 'Analysisstatus', 'Reason', 'Recommendation', 'Systemtype', 'IP', 'OS', 'Company', 'Location', 'Serviceprovider', 'Tag', 'Case', 'Created', 'Modified'])
        # compare content - system 1
        self.assertEqual(int(sheet_systems.cell(1,0).value), system_1.system_id)
        self.assertEqual(sheet_systems.cell(1,1).value, system_1.system_name)
        self.assertEqual(sheet_systems.cell(1,2).value, system_1.dnsname.dnsname_name)
        self.assertEqual(sheet_systems.cell(1,3).value, system_1.domain.domain_name)
        self.assertEqual(sheet_systems.cell(1,4).value, system_1.systemstatus.systemstatus_name)
        self.assertEqual(sheet_systems.cell(1,5).value, system_1.analysisstatus.analysisstatus_name)
        self.assertEqual(sheet_systems.cell(1,6).value, system_1.reason.reason_name)
        self.assertEqual(sheet_systems.cell(1,7).value, system_1.recommendation.recommendation_name)
        self.assertEqual(sheet_systems.cell(1,8).value, system_1.systemtype.systemtype_name)
        self.assertEqual(sheet_systems.cell(1,9).value, '127.0.0.1\n127.0.0.2\n127.0.0.3')
        self.assertEqual(sheet_systems.cell(1,10).value, system_1.os.os_name)
        self.assertEqual(sheet_systems.cell(1,11).value, 'company_1\ncompany_2\ncompany_3')
        self.assertEqual(sheet_systems.cell(1,12).value, system_1.location.location_name)
        self.assertEqual(sheet_systems.cell(1,13).value, system_1.serviceprovider.serviceprovider_name)
        self.assertEqual(sheet_systems.cell(1,14).value, 'tag_1\ntag_2\ntag_3')
        self.assertEqual(sheet_systems.cell(1,15).value, 'case_1\ncase_2\ncase_3')
        self.assertEqual(sheet_systems.cell(1,16).value, '2001-02-03 04:05')
        self.assertEqual(sheet_systems.cell(1,17).value, '2001-02-03 04:05')
        # compare content - system 2
        self.assertEqual(int(sheet_systems.cell(2,0).value), system_2.system_id)
        self.assertEqual(sheet_systems.cell(2,1).value, system_2.system_name)
        self.assertEqual(sheet_systems.cell(2,2).value, '')
        self.assertEqual(sheet_systems.cell(2,3).value, '')
        self.assertEqual(sheet_systems.cell(2,4).value, system_2.systemstatus.systemstatus_name)
        self.assertEqual(sheet_systems.cell(2,5).value, '')
        self.assertEqual(sheet_systems.cell(2,6).value, '')
        self.assertEqual(sheet_systems.cell(2,7).value, '')
        self.assertEqual(sheet_systems.cell(2,8).value, '')
        self.assertEqual(sheet_systems.cell(2,9).value, '')
        self.assertEqual(sheet_systems.cell(2,10).value, '')
        self.assertEqual(sheet_systems.cell(2,11).value, '')
        self.assertEqual(sheet_systems.cell(2,12).value, '')
        self.assertEqual(sheet_systems.cell(2,13).value, '')
        self.assertEqual(sheet_systems.cell(2,14).value, '')
        self.assertEqual(sheet_systems.cell(2,16).value, '2009-08-07 06:05')
        self.assertEqual(sheet_systems.cell(2,17).value, '2009-08-07 06:05')
        # compare content - systemstatus worksheet (whole columns)
        self.assertEqual(sheet_systemstatus.col_values(0), systemstatus_id_list)
        self.assertEqual(sheet_systemstatus.col_values(1), systemstatus_name_list)
        self.assertEqual(sheet_systemstatus.col_values(2), systemstatus_note_list)
        # compare content - analysisstatus worksheet (whole columns)
        self.assertEqual(sheet_analysisstatus.col_values(0), analysisstatus_id_list)
        self.assertEqual(sheet_analysisstatus.col_values(1), analysisstatus_name_list)
        self.assertEqual(sheet_analysisstatus.col_values(2), analysisstatus_note_list)
        # compare content - reason worksheet (whole columns)
        self.assertEqual(sheet_reasons.col_values(0), reason_id_list)
        self.assertEqual(sheet_reasons.col_values(1), reason_name_list)
        self.assertEqual(sheet_reasons.col_values(2), reason_note_list)
        # compare content - recommendation worksheet (whole columns)
        self.assertEqual(sheet_recommendations.col_values(0), recommendation_id_list)
        self.assertEqual(sheet_recommendations.col_values(1), recommendation_name_list)
        self.assertEqual(sheet_recommendations.col_values(2), recommendation_note_list)
        # compare content - tag worksheet (whole columns)
        self.assertEqual(sheet_tags.col_values(0), tag_id_list)
        self.assertEqual(sheet_tags.col_values(1), tag_name_list)
        self.assertEqual(sheet_tags.col_values(2), tag_note_list)
        # compare content - metadata
        self.assertEqual(sheet_systems.cell(4,0).value, 'Created:')
        self.assertEqual(sheet_systems.cell(4,1).value,  t2_now.strftime('%Y-%m-%d %H:%M'))
        self.assertEqual(sheet_systems.cell(5,0).value, 'Created by:')
        self.assertEqual(sheet_systems.cell(5,1).value, 'testuser_system_exporter_spreadsheet_xls')

    def test_system_exporter_spreadsheet_xls_cron_complete_spreadsheet(self):
        """ test exporter view """

        """ modify config section """

        # get and modify main config
        main_config_model = MainConfigModel.objects.get(main_config_name = 'MainConfig')
        main_config_model.cron_export_path = '/tmp'
        main_config_model.cron_username = 'cron'
        main_config_model.save()

        # get and modify config to show all columns and sheets
        system_exporter_spreadsheet_xls_config_model = SystemExporterSpreadsheetXlsConfigModel(system_exporter_spreadsheet_xls_config_name = 'SystemExporterSpreadsheetXlsConfig')
        system_exporter_spreadsheet_xls_config_model.spread_xls_system_id = True
        system_exporter_spreadsheet_xls_config_model.spread_xls_dnsname = True
        system_exporter_spreadsheet_xls_config_model.spread_xls_domain = True
        system_exporter_spreadsheet_xls_config_model.spread_xls_systemstatus = True
        system_exporter_spreadsheet_xls_config_model.spread_xls_analysisstatus = True
        system_exporter_spreadsheet_xls_config_model.spread_xls_reason = True
        system_exporter_spreadsheet_xls_config_model.spread_xls_recommendation = True
        system_exporter_spreadsheet_xls_config_model.spread_xls_systemtype = True
        system_exporter_spreadsheet_xls_config_model.spread_xls_ip = True
        system_exporter_spreadsheet_xls_config_model.spread_xls_os = True
        system_exporter_spreadsheet_xls_config_model.spread_xls_company = True
        system_exporter_spreadsheet_xls_config_model.spread_xls_location = True
        system_exporter_spreadsheet_xls_config_model.spread_xls_serviceprovider = True
        system_exporter_spreadsheet_xls_config_model.spread_xls_tag = True
        system_exporter_spreadsheet_xls_config_model.spread_xls_case = True
        system_exporter_spreadsheet_xls_config_model.spread_xls_system_create_time = True
        system_exporter_spreadsheet_xls_config_model.spread_xls_system_modify_time = True
        system_exporter_spreadsheet_xls_config_model.spread_xls_worksheet_systemstatus = True
        system_exporter_spreadsheet_xls_config_model.spread_xls_worksheet_analysisstatus = True
        system_exporter_spreadsheet_xls_config_model.spread_xls_worksheet_reason = True
        system_exporter_spreadsheet_xls_config_model.spread_xls_worksheet_recommendation = True
        system_exporter_spreadsheet_xls_config_model.spread_xls_worksheet_tag = True
        system_exporter_spreadsheet_xls_config_model.save()

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
        output_file_path = main_config_model.cron_export_path + '/' + filetime + '_systems.xls'
        # open file from temp folder
        xls_disk = xlrd.open_workbook(output_file_path)

        """ prepare objects section """

        # get objects
        system_1 = System.objects.get(system_name='system_1_all_attributes')
        system_2 = System.objects.get(system_name='system_2_no_attributes')

        # create lists for easier comparison with whole columns - systemstatus
        systemstatus_id_list = ['ID']
        systemstatus_name_list = ['Systemstatus']
        systemstatus_note_list = ['Note']
        all_systemstatus = Systemstatus.objects.all().order_by('systemstatus_name')
        for systemstatus_object in all_systemstatus:
            # the conversion to float was carried out, because otherwise the return values from the spreadsheet would have had to be converted to int, which would have been more time-consuming
            systemstatus_id_list.append(float(systemstatus_object.systemstatus_id))
            systemstatus_name_list.append(systemstatus_object.systemstatus_name)
            if systemstatus_object.systemstatus_note:
                systemstatus_note_list.append(systemstatus_object.systemstatus_note)
            else:
                systemstatus_note_list.append('')

        # create lists for easier comparison with whole columns - analysisstatus
        analysisstatus_id_list = ['ID']
        analysisstatus_name_list = ['Analysisstatus']
        analysisstatus_note_list = ['Note']
        all_analysisstatus = Analysisstatus.objects.all().order_by('analysisstatus_name')
        for analysisstatus_object in all_analysisstatus:
            # the conversion to float was carried out, because otherwise the return values from the spreadsheet would have had to be converted to int, which would have been more time-consuming
            analysisstatus_id_list.append(float(analysisstatus_object.analysisstatus_id))
            analysisstatus_name_list.append(analysisstatus_object.analysisstatus_name)
            if analysisstatus_object.analysisstatus_note:
                analysisstatus_note_list.append(analysisstatus_object.analysisstatus_note)
            else:
                analysisstatus_note_list.append('')

        # create lists for easier comparison with whole columns - reason
        reason_id_list = ['ID']
        reason_name_list = ['Reason']
        reason_note_list = ['Note']
        all_reason = Reason.objects.all().order_by('reason_name')
        for reason_object in all_reason:
            # the conversion to float was carried out, because otherwise the return values from the spreadsheet would have had to be converted to int, which would have been more time-consuming
            reason_id_list.append(float(reason_object.reason_id))
            reason_name_list.append(reason_object.reason_name)
            if reason_object.reason_note:
                reason_note_list.append(reason_object.reason_note)
            else:
                reason_note_list.append('')

        # create lists for easier comparison with whole columns - recommendation
        recommendation_id_list = ['ID']
        recommendation_name_list = ['Recommendation']
        recommendation_note_list = ['Note']
        all_recommendation = Recommendation.objects.all().order_by('recommendation_name')
        for recommendation_object in all_recommendation:
            # the conversion to float was carried out, because otherwise the return values from the spreadsheet would have had to be converted to int, which would have been more time-consuming
            recommendation_id_list.append(float(recommendation_object.recommendation_id))
            recommendation_name_list.append(recommendation_object.recommendation_name)
            if recommendation_object.recommendation_note:
                recommendation_note_list.append(recommendation_object.recommendation_note)
            else:
                recommendation_note_list.append('')

        # create lists for easier comparison with whole columns - tag
        tag_id_list = ['ID']
        tag_name_list = ['Tag']
        tag_note_list = ['Note']
        all_tag = Tag.objects.all().order_by('tag_name')
        for tag_object in all_tag:
            # the conversion to float was carried out, because otherwise the return values from the spreadsheet would have had to be converted to int, which would have been more time-consuming
            tag_id_list.append(float(tag_object.tag_id))
            tag_name_list.append(tag_object.tag_name)
            if tag_object.tag_note:
                tag_note_list.append(tag_object.tag_note)
            else:
                tag_note_list.append('')

        # get sheets
        sheet_systems = xls_disk.sheet_by_name('systems')
        sheet_systemstatus = xls_disk.sheet_by_name('systemstatus')
        sheet_analysisstatus = xls_disk.sheet_by_name('analysisstatus')
        sheet_reasons = xls_disk.sheet_by_name('reasons')
        sheet_recommendations = xls_disk.sheet_by_name('recommendations')
        sheet_tags = xls_disk.sheet_by_name('tags')

        """ compare values section """

        # compare number of rows and columns
        self.assertEqual(sheet_systems.nrows, 6)
        self.assertEqual(sheet_systems.ncols, 18)
        self.assertEqual(sheet_systemstatus.nrows, 10)
        self.assertEqual(sheet_systemstatus.ncols, 3)
        self.assertEqual(sheet_analysisstatus.nrows, 7)
        self.assertEqual(sheet_analysisstatus.ncols, 3)
        self.assertEqual(sheet_reasons.nrows, 2)
        self.assertEqual(sheet_reasons.ncols, 3)
        self.assertEqual(sheet_recommendations.nrows, 2)
        self.assertEqual(sheet_recommendations.ncols, 3)
        self.assertEqual(sheet_tags.nrows, 9)
        self.assertEqual(sheet_tags.ncols, 3)
        # compare headlines
        self.assertEqual(sheet_systems.row_values(0), ['ID', 'System', 'DNS name', 'Domain', 'Systemstatus', 'Analysisstatus', 'Reason', 'Recommendation', 'Systemtype', 'IP', 'OS', 'Company', 'Location', 'Serviceprovider', 'Tag', 'Case', 'Created', 'Modified'])
        # compare content - system 1
        self.assertEqual(int(sheet_systems.cell(1,0).value), system_1.system_id)
        self.assertEqual(sheet_systems.cell(1,1).value, system_1.system_name)
        self.assertEqual(sheet_systems.cell(1,2).value, system_1.dnsname.dnsname_name)
        self.assertEqual(sheet_systems.cell(1,3).value, system_1.domain.domain_name)
        self.assertEqual(sheet_systems.cell(1,4).value, system_1.systemstatus.systemstatus_name)
        self.assertEqual(sheet_systems.cell(1,5).value, system_1.analysisstatus.analysisstatus_name)
        self.assertEqual(sheet_systems.cell(1,6).value, system_1.reason.reason_name)
        self.assertEqual(sheet_systems.cell(1,7).value, system_1.recommendation.recommendation_name)
        self.assertEqual(sheet_systems.cell(1,8).value, system_1.systemtype.systemtype_name)
        self.assertEqual(sheet_systems.cell(1,9).value, '127.0.0.1\n127.0.0.2\n127.0.0.3')
        self.assertEqual(sheet_systems.cell(1,10).value, system_1.os.os_name)
        self.assertEqual(sheet_systems.cell(1,11).value, 'company_1\ncompany_2\ncompany_3')
        self.assertEqual(sheet_systems.cell(1,12).value, system_1.location.location_name)
        self.assertEqual(sheet_systems.cell(1,13).value, system_1.serviceprovider.serviceprovider_name)
        self.assertEqual(sheet_systems.cell(1,14).value, 'tag_1\ntag_2\ntag_3')
        self.assertEqual(sheet_systems.cell(1,15).value, 'case_1\ncase_2\ncase_3')
        self.assertEqual(sheet_systems.cell(1,16).value, '2001-02-03 04:05')
        self.assertEqual(sheet_systems.cell(1,17).value, '2001-02-03 04:05')
        # compare content - system 2
        self.assertEqual(int(sheet_systems.cell(2,0).value), system_2.system_id)
        self.assertEqual(sheet_systems.cell(2,1).value, system_2.system_name)
        self.assertEqual(sheet_systems.cell(2,2).value, '')
        self.assertEqual(sheet_systems.cell(2,3).value, '')
        self.assertEqual(sheet_systems.cell(2,4).value, system_2.systemstatus.systemstatus_name)
        self.assertEqual(sheet_systems.cell(2,5).value, '')
        self.assertEqual(sheet_systems.cell(2,6).value, '')
        self.assertEqual(sheet_systems.cell(2,7).value, '')
        self.assertEqual(sheet_systems.cell(2,8).value, '')
        self.assertEqual(sheet_systems.cell(2,9).value, '')
        self.assertEqual(sheet_systems.cell(2,10).value, '')
        self.assertEqual(sheet_systems.cell(2,11).value, '')
        self.assertEqual(sheet_systems.cell(2,12).value, '')
        self.assertEqual(sheet_systems.cell(2,13).value, '')
        self.assertEqual(sheet_systems.cell(2,14).value, '')
        self.assertEqual(sheet_systems.cell(2,16).value, '2009-08-07 06:05')
        self.assertEqual(sheet_systems.cell(2,17).value, '2009-08-07 06:05')
        # compare content - systemstatus worksheet (whole columns)
        self.assertEqual(sheet_systemstatus.col_values(0), systemstatus_id_list)
        self.assertEqual(sheet_systemstatus.col_values(1), systemstatus_name_list)
        self.assertEqual(sheet_systemstatus.col_values(2), systemstatus_note_list)
        # compare content - analysisstatus worksheet (whole columns)
        self.assertEqual(sheet_analysisstatus.col_values(0), analysisstatus_id_list)
        self.assertEqual(sheet_analysisstatus.col_values(1), analysisstatus_name_list)
        self.assertEqual(sheet_analysisstatus.col_values(2), analysisstatus_note_list)
        # compare content - reason worksheet (whole columns)
        self.assertEqual(sheet_reasons.col_values(0), reason_id_list)
        self.assertEqual(sheet_reasons.col_values(1), reason_name_list)
        self.assertEqual(sheet_reasons.col_values(2), reason_note_list)
        # compare content - recommendation worksheet (whole columns)
        self.assertEqual(sheet_recommendations.col_values(0), recommendation_id_list)
        self.assertEqual(sheet_recommendations.col_values(1), recommendation_name_list)
        self.assertEqual(sheet_recommendations.col_values(2), recommendation_note_list)
        # compare content - tag worksheet (whole columns)
        self.assertEqual(sheet_tags.col_values(0), tag_id_list)
        self.assertEqual(sheet_tags.col_values(1), tag_name_list)
        self.assertEqual(sheet_tags.col_values(2), tag_note_list)
        # compare content - metadata
        self.assertEqual(sheet_systems.cell(4,0).value, 'Created:')
        self.assertEqual(sheet_systems.cell(4,1).value,  t3_now.strftime('%Y-%m-%d %H:%M'))
        self.assertEqual(sheet_systems.cell(5,0).value, 'Created by:')
        self.assertEqual(sheet_systems.cell(5,1).value, 'cron')
