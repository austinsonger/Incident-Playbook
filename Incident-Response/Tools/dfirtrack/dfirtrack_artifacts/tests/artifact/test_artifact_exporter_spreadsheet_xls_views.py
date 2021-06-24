from datetime import datetime
from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone
from dfirtrack_artifacts.exporter.spreadsheet.xls import artifact_cron
from dfirtrack_artifacts.models import Artifact, Artifactstatus, Artifacttype
from dfirtrack_config.models import ArtifactExporterSpreadsheetXlsConfigModel, MainConfigModel
from dfirtrack_main.models import System, Systemstatus
from mock import patch
import urllib.parse
import xlrd

class ArtifactExporterSpreadsheetXlsViewTestCase(TestCase):
    """ artifact exporter spreadsheet XLS view tests """

    @classmethod
    def setUpTestData(cls):

        # create user
        test_user = User.objects.create_user(username='testuser_artifact_exporter_spreadsheet_xls', password='LTzoNHIdxiJydsaJKf1G')

        # create object
        artifactstatus_3 = Artifactstatus.objects.create(artifactstatus_name = 'artifactstatus_3')

        # create object
        artifactstatus_1 = Artifactstatus.objects.create(
            artifactstatus_name='artifactstatus_1',
            artifactstatus_note='lorem ipsum',
        )

        # create objects
        artifacttype_1 = Artifacttype.objects.create(artifacttype_name='artifacttype_1')
        artifacttype_2 = Artifacttype.objects.create(
            artifacttype_name='artifacttype_2',
            artifacttype_note='lorem ipsum',
        )

        # create object
        systemstatus_1 = Systemstatus.objects.create(systemstatus_name='systemstatus_1')

        # create object
        system_1 = System.objects.create(
            system_name='artifact_exporter_spreadsheet_xls_system_1',
            systemstatus = systemstatus_1,
            system_modify_time = timezone.now(),
            system_created_by_user_id = test_user,
            system_modified_by_user_id = test_user,
        )

        """ create artifacts """

        # mock timezone.now()
        t_1 = datetime(2012, 11, 10, 12, 34, tzinfo=timezone.utc)
        with patch.object(timezone, 'now', return_value=t_1):

            # create object with maximum attributes
            Artifact.objects.create(
                artifact_name = 'artifact_exporter_spreadsheet_xls_artifact_1_all_attributes',
                artifactstatus = artifactstatus_3,
                artifacttype = artifacttype_1,
                system = system_1,
                artifact_source_path = 'C:\Temp\malicious.exe',
                artifact_note_internal = 'artifact note for internal usage',
                artifact_note_external = 'artifact note for external usage',
                artifact_note_analysisresult = 'artifact note for analysis result',
                artifact_md5 = 'd41d8cd98f00b204e9800998ecf8427e',
                artifact_sha1 = 'da39a3ee5e6b4b0d3255bfef95601890afd80709',
                artifact_sha256 = 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855',
                artifact_created_by_user_id = test_user,
                artifact_modified_by_user_id = test_user,
            )

        # mock timezone.now()
        t_2 = datetime(2009, 8, 7, 23, 45, tzinfo=timezone.utc)
        with patch.object(timezone, 'now', return_value=t_2):

            # create object with minimum attributes
            Artifact.objects.create(
                artifact_name = 'artifact_exporter_spreadsheet_xls_artifact_2_no_attributes',
                artifactstatus = artifactstatus_3,
                artifacttype = artifacttype_1,
                system = system_1,
                artifact_created_by_user_id = test_user,
                artifact_modified_by_user_id = test_user,
            )

        # create object that will not be exported
        Artifact.objects.create(
            artifact_name = 'artifact_exporter_spreadsheet_xls_artifact_3_not_exported',
            artifactstatus = artifactstatus_1,
            artifacttype = artifacttype_2,
            system = system_1,
            artifact_created_by_user_id = test_user,
            artifact_modified_by_user_id = test_user,
        )

    def test_artifact_exporter_spreadsheet_xls_not_logged_in(self):
        """ test exporter view """

        # create url
        destination = '/login/?next=' + urllib.parse.quote('/artifacts/artifact/exporter/spreadsheet/xls/artifact/', safe='')
        # get response
        response = self.client.get('/artifacts/artifact/exporter/spreadsheet/xls/artifact/', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)

    def test_artifact_exporter_spreadsheet_xls_logged_in(self):
        """ test exporter view """

        # login testuser
        self.client.login(username='testuser_artifact_exporter_spreadsheet_xls', password='LTzoNHIdxiJydsaJKf1G')
        # get response
        response = self.client.get('/artifacts/artifact/exporter/spreadsheet/xls/artifact/')
        # compare
        self.assertEqual(response.status_code, 200)

    def test_artifact_exporter_spreadsheet_xls_redirect(self):
        """ test exporter view """

        # login testuser
        self.client.login(username='testuser_artifact_exporter_spreadsheet_xls', password='LTzoNHIdxiJydsaJKf1G')
        # create url
        destination = urllib.parse.quote('/artifacts/artifact/exporter/spreadsheet/xls/artifact/', safe='/')
        # get response
        response = self.client.get('/artifacts/artifact/exporter/spreadsheet/xls/artifact', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=301, target_status_code=200)

    def test_artifact_exporter_spreadsheet_xls_minimal_spreadsheet(self):
        """ test exporter view """

        """ modify config section """

        # get and modify config to show only mandatory columns
        artifact_exporter_spreadsheet_xls_config_model = ArtifactExporterSpreadsheetXlsConfigModel.objects.get(artifact_exporter_spreadsheet_xls_config_name='ArtifactExporterSpreadsheetXlsConfig')
        artifact_exporter_spreadsheet_xls_config_model.artifactlist_xls_artifact_id = False
        artifact_exporter_spreadsheet_xls_config_model.artifactlist_xls_system_id = False
        artifact_exporter_spreadsheet_xls_config_model.artifactlist_xls_system_name = False
        artifact_exporter_spreadsheet_xls_config_model.artifactlist_xls_artifactstatus = False
        artifact_exporter_spreadsheet_xls_config_model.artifactlist_xls_artifactpriority = False
        artifact_exporter_spreadsheet_xls_config_model.artifactlist_xls_artifacttype = False
        artifact_exporter_spreadsheet_xls_config_model.artifactlist_xls_artifact_source_path = False
        artifact_exporter_spreadsheet_xls_config_model.artifactlist_xls_artifact_storage_path = False
        artifact_exporter_spreadsheet_xls_config_model.artifactlist_xls_artifact_note_internal = False
        artifact_exporter_spreadsheet_xls_config_model.artifactlist_xls_artifact_note_external = False
        artifact_exporter_spreadsheet_xls_config_model.artifactlist_xls_artifact_note_analysisresult = False
        artifact_exporter_spreadsheet_xls_config_model.artifactlist_xls_artifact_md5 = False
        artifact_exporter_spreadsheet_xls_config_model.artifactlist_xls_artifact_sha1 = False
        artifact_exporter_spreadsheet_xls_config_model.artifactlist_xls_artifact_sha256 = False
        artifact_exporter_spreadsheet_xls_config_model.artifactlist_xls_artifact_create_time = False
        artifact_exporter_spreadsheet_xls_config_model.artifactlist_xls_artifact_modify_time = False
        artifact_exporter_spreadsheet_xls_config_model.artifactlist_xls_worksheet_artifactstatus = False
        artifact_exporter_spreadsheet_xls_config_model.artifactlist_xls_worksheet_artifacttype = False
        artifact_exporter_spreadsheet_xls_config_model.save()
        # get object
        artifactstatus_3 = Artifactstatus.objects.get(artifactstatus_name = 'artifactstatus_3')
        # add artifactstatus to choice for export
        artifact_exporter_spreadsheet_xls_config_model.artifactlist_xls_choice_artifactstatus.add(artifactstatus_3)

        """ call view section """

        # login testuser
        self.client.login(username='testuser_artifact_exporter_spreadsheet_xls', password='LTzoNHIdxiJydsaJKf1G')

        # mock timezone.now()
        t1_now = timezone.now()
        with patch.object(timezone, 'now', return_value=t1_now):

            # get response
            response = self.client.get('/artifacts/artifact/exporter/spreadsheet/xls/artifact/')

        """ get file section """

        # get artifactlist from response content
        workbook = response.content
        # open artifactlist directly from byte stream
        artifactlist = xlrd.open_workbook(file_contents=workbook)

        """ prepare objects section """

        # get objects
        artifact_1 = Artifact.objects.get(artifact_name = 'artifact_exporter_spreadsheet_xls_artifact_1_all_attributes')
        artifact_2 = Artifact.objects.get(artifact_name = 'artifact_exporter_spreadsheet_xls_artifact_2_no_attributes')

        # get sheets
        sheet_artifacts = artifactlist.sheet_by_name('artifacts')

        """ compare values section """

        # compare non-available sheets
        self.assertRaises(xlrd.biffh.XLRDError, artifactlist.sheet_by_name, sheet_name='artifactstatus')
        self.assertRaises(xlrd.biffh.XLRDError, artifactlist.sheet_by_name, sheet_name='artifacttype')
        # compare number of rows and columns
        self.assertEqual(sheet_artifacts.nrows, 6)
        self.assertEqual(sheet_artifacts.ncols, 2)
        # compare headlines
        self.assertEqual(sheet_artifacts.row_values(0), ['Artifact', ''])
        # compare content - artifact 1
        self.assertEqual(sheet_artifacts.cell(1,0).value, artifact_1.artifact_name)
        # compare content - artifact 2
        self.assertEqual(sheet_artifacts.cell(2,0).value, artifact_2.artifact_name)
        # compare content - metadata
        self.assertEqual(sheet_artifacts.cell(4,0).value, 'Created:')
        self.assertEqual(sheet_artifacts.cell(4,1).value, t1_now.strftime('%Y-%m-%d %H:%M'))
        self.assertEqual(sheet_artifacts.cell(5,0).value, 'Created by:')
        self.assertEqual(sheet_artifacts.cell(5,1).value, 'testuser_artifact_exporter_spreadsheet_xls')

    def test_artifact_exporter_spreadsheet_xls_complete_spreadsheet(self):
        """ test exporter view """

        """ modify config section """

        # get and modify config to show all columns and sheets
        artifact_exporter_spreadsheet_xls_config_model = ArtifactExporterSpreadsheetXlsConfigModel.objects.get(artifact_exporter_spreadsheet_xls_config_name='ArtifactExporterSpreadsheetXlsConfig')
        artifact_exporter_spreadsheet_xls_config_model.artifactlist_xls_artifact_id = True
        artifact_exporter_spreadsheet_xls_config_model.artifactlist_xls_system_id = True
        artifact_exporter_spreadsheet_xls_config_model.artifactlist_xls_system_name = True
        artifact_exporter_spreadsheet_xls_config_model.artifactlist_xls_artifactstatus = True
        artifact_exporter_spreadsheet_xls_config_model.artifactlist_xls_artifactpriority = True
        artifact_exporter_spreadsheet_xls_config_model.artifactlist_xls_artifacttype = True
        artifact_exporter_spreadsheet_xls_config_model.artifactlist_xls_artifact_source_path = True
        artifact_exporter_spreadsheet_xls_config_model.artifactlist_xls_artifact_storage_path = True
        artifact_exporter_spreadsheet_xls_config_model.artifactlist_xls_artifact_note_internal = True
        artifact_exporter_spreadsheet_xls_config_model.artifactlist_xls_artifact_note_external = True
        artifact_exporter_spreadsheet_xls_config_model.artifactlist_xls_artifact_note_analysisresult = True
        artifact_exporter_spreadsheet_xls_config_model.artifactlist_xls_artifact_md5 = True
        artifact_exporter_spreadsheet_xls_config_model.artifactlist_xls_artifact_sha1 = True
        artifact_exporter_spreadsheet_xls_config_model.artifactlist_xls_artifact_sha256 = True
        artifact_exporter_spreadsheet_xls_config_model.artifactlist_xls_artifact_create_time = True
        artifact_exporter_spreadsheet_xls_config_model.artifactlist_xls_artifact_modify_time = True
        artifact_exporter_spreadsheet_xls_config_model.artifactlist_xls_worksheet_artifactstatus = True
        artifact_exporter_spreadsheet_xls_config_model.artifactlist_xls_worksheet_artifacttype = True
        artifact_exporter_spreadsheet_xls_config_model.save()
        # get object
        artifactstatus_3 = Artifactstatus.objects.get(artifactstatus_name = 'artifactstatus_3')
        # add artifactstatus to choice for export
        artifact_exporter_spreadsheet_xls_config_model.artifactlist_xls_choice_artifactstatus.add(artifactstatus_3)

        """ call view section """

        # login testuser
        self.client.login(username='testuser_artifact_exporter_spreadsheet_xls', password='LTzoNHIdxiJydsaJKf1G')

        # mock timezone.now()
        t2_now = timezone.now()
        with patch.object(timezone, 'now', return_value=t2_now):

            # get response
            response = self.client.get('/artifacts/artifact/exporter/spreadsheet/xls/artifact/')

        """ get file section """

        # get artifactlist from response content
        workbook = response.content
        # open artifactlist directly from byte stream
        artifactlist = xlrd.open_workbook(file_contents=workbook)

        """ prepare objects section """

        # get objects
        artifact_1 = Artifact.objects.get(artifact_name = 'artifact_exporter_spreadsheet_xls_artifact_1_all_attributes')
        artifact_2 = Artifact.objects.get(artifact_name = 'artifact_exporter_spreadsheet_xls_artifact_2_no_attributes')

        # create lists for easier comparison with whole columns - artifactstatus
        artifactstatus_id_list = ['ID']
        artifactstatus_name_list = ['Artifactstatus']
        artifactstatus_note_list = ['Note']
        all_artifactstatus = Artifactstatus.objects.all().order_by('artifactstatus_name')
        for artifactstatus_object in all_artifactstatus:
            # the conversion to float was carried out, because otherwise the return values from the spreadsheet would have had to be converted to int, which would have been more time-consuming
            artifactstatus_id_list.append(float(artifactstatus_object.artifactstatus_id))
            artifactstatus_name_list.append(artifactstatus_object.artifactstatus_name)
            if artifactstatus_object.artifactstatus_note:
                artifactstatus_note_list.append(artifactstatus_object.artifactstatus_note)
            else:
                artifactstatus_note_list.append('---')

        # create lists for easier comparison with whole columns - artifacttype
        artifacttype_id_list = ['ID']
        artifacttype_name_list = ['Artifacttype']
        artifacttype_note_list = ['Note']
        all_artifacttype = Artifacttype.objects.all().order_by('artifacttype_name')
        for artifacttype_object in all_artifacttype:
            # the conversion to float was carried out, because otherwise the return values from the spreadsheet would have had to be converted to int, which would have been more time-consuming
            artifacttype_id_list.append(float(artifacttype_object.artifacttype_id))
            artifacttype_name_list.append(artifacttype_object.artifacttype_name)
            if artifacttype_object.artifacttype_note:
                artifacttype_note_list.append(artifacttype_object.artifacttype_note)
            else:
                artifacttype_note_list.append('---')

        # get sheets
        sheet_artifacts = artifactlist.sheet_by_name('artifacts')
        sheet_artifactstatus = artifactlist.sheet_by_name('artifactstatus')
        sheet_artifacttype = artifactlist.sheet_by_name('artifacttype')

        """ compare values section """

        # compare number of rows and columns
        self.assertEqual(sheet_artifacts.nrows, 6)
        self.assertEqual(sheet_artifacts.ncols, 17)
        self.assertEqual(sheet_artifactstatus.nrows, 14)
        self.assertEqual(sheet_artifactstatus.ncols, 3)
        self.assertEqual(sheet_artifacttype.nrows, 7)
        self.assertEqual(sheet_artifacttype.ncols, 3)
        # compare headlines
        self.assertEqual(sheet_artifacts.row_values(0), ['Artifact ID', 'Artifact', 'System ID', 'System', 'Artifactstatus', 'Artifactpriority', 'Artifacttype', 'Source path', 'Storage path', 'Internal note','External note',  'Analysis result', 'MD5', 'SHA1', 'SHA256', 'Created', 'Modified'])
        self.assertEqual(sheet_artifactstatus.row_values(0), ['ID', 'Artifactstatus', 'Note'])
        self.assertEqual(sheet_artifacttype.row_values(0), ['ID', 'Artifacttype', 'Note'])
        # compare content - artifact 1
        self.assertEqual(int(sheet_artifacts.cell(1,0).value), artifact_1.artifact_id)
        self.assertEqual(sheet_artifacts.cell(1,1).value, artifact_1.artifact_name)
        self.assertEqual(int(sheet_artifacts.cell(1,2).value), artifact_1.system.system_id)
        self.assertEqual(sheet_artifacts.cell(1,3).value, artifact_1.system.system_name)
        self.assertEqual(sheet_artifacts.cell(1,4).value, artifact_1.artifactstatus.artifactstatus_name)
        self.assertEqual(sheet_artifacts.cell(1,5).value, artifact_1.artifactpriority.artifactpriority_name)
        self.assertEqual(sheet_artifacts.cell(1,6).value, artifact_1.artifacttype.artifacttype_name)
        self.assertEqual(sheet_artifacts.cell(1,7).value, artifact_1.artifact_source_path)
        self.assertEqual(sheet_artifacts.cell(1,8).value, artifact_1.artifact_storage_path)
        self.assertEqual(sheet_artifacts.cell(1,9).value, 'artifact note for internal usage')      # artifact_note_internal
        self.assertEqual(sheet_artifacts.cell(1,10).value, 'artifact note for external usage')       # artifact_note_external
        self.assertEqual(sheet_artifacts.cell(1,11).value, 'artifact note for analysis result')      # artifact_note_analysisresult
        self.assertEqual(sheet_artifacts.cell(1,12).value, artifact_1.artifact_md5)
        self.assertEqual(sheet_artifacts.cell(1,13).value, artifact_1.artifact_sha1)
        self.assertEqual(sheet_artifacts.cell(1,14).value, artifact_1.artifact_sha256)
        self.assertEqual(sheet_artifacts.cell(1,15).value, '2012-11-10 12:34')
        self.assertEqual(sheet_artifacts.cell(1,16).value, '2012-11-10 12:34')
        # compare content - artifact 2
        self.assertEqual(int(sheet_artifacts.cell(2,0).value), artifact_2.artifact_id)
        self.assertEqual(sheet_artifacts.cell(2,1).value, artifact_2.artifact_name)
        self.assertEqual(int(sheet_artifacts.cell(2,2).value), artifact_2.system.system_id)
        self.assertEqual(sheet_artifacts.cell(2,3).value, artifact_2.system.system_name)
        self.assertEqual(sheet_artifacts.cell(2,4).value, artifact_2.artifactstatus.artifactstatus_name)
        self.assertEqual(sheet_artifacts.cell(2,5).value, artifact_2.artifactpriority.artifactpriority_name)
        self.assertEqual(sheet_artifacts.cell(2,6).value, artifact_2.artifacttype.artifacttype_name)
        self.assertEqual(sheet_artifacts.cell(2,7).value, '')
        self.assertEqual(sheet_artifacts.cell(2,8).value, artifact_2.artifact_storage_path)
        self.assertEqual(sheet_artifacts.cell(2,9).value, '')
        self.assertEqual(sheet_artifacts.cell(2,10).value, '')
        self.assertEqual(sheet_artifacts.cell(2,11).value, '')
        self.assertEqual(sheet_artifacts.cell(2,12).value, '')
        self.assertEqual(sheet_artifacts.cell(2,13).value, '')
        self.assertEqual(sheet_artifacts.cell(2,14).value, '')
        self.assertEqual(sheet_artifacts.cell(2,15).value, '2009-08-07 23:45')
        self.assertEqual(sheet_artifacts.cell(2,16).value, '2009-08-07 23:45')
        # compare content - artifactstatus worksheet (whole columns)
        self.assertEqual(sheet_artifactstatus.col_values(0), artifactstatus_id_list)
        self.assertEqual(sheet_artifactstatus.col_values(1), artifactstatus_name_list)
        self.assertEqual(sheet_artifactstatus.col_values(2), artifactstatus_note_list)
        # compare content - artifacttype worksheet (whole columns)
        self.assertEqual(sheet_artifacttype.col_values(0), artifacttype_id_list)
        self.assertEqual(sheet_artifacttype.col_values(1), artifacttype_name_list)
        self.assertEqual(sheet_artifacttype.col_values(2), artifacttype_note_list)
        # compare content - metadata
        self.assertEqual(sheet_artifacts.cell(4,0).value, 'Created:')
        self.assertEqual(sheet_artifacts.cell(4,1).value, t2_now.strftime('%Y-%m-%d %H:%M'))
        self.assertEqual(sheet_artifacts.cell(5,0).value, 'Created by:')
        self.assertEqual(sheet_artifacts.cell(5,1).value, 'testuser_artifact_exporter_spreadsheet_xls')

    def test_artifact_exporter_spreadsheet_xls_cron_complete_spreadsheet(self):
        """ test exporter view """

        """ modify config section """

        # get and modify main config
        main_config_model = MainConfigModel.objects.get(main_config_name = 'MainConfig')
        main_config_model.cron_export_path = '/tmp'
        main_config_model.cron_username = 'cron'
        main_config_model.save()

        # get and modify config to show all columns and sheets
        artifact_exporter_spreadsheet_xls_config_model = ArtifactExporterSpreadsheetXlsConfigModel.objects.get(artifact_exporter_spreadsheet_xls_config_name='ArtifactExporterSpreadsheetXlsConfig')
        artifact_exporter_spreadsheet_xls_config_model.artifactlist_xls_artifact_id = True
        artifact_exporter_spreadsheet_xls_config_model.artifactlist_xls_system_id = True
        artifact_exporter_spreadsheet_xls_config_model.artifactlist_xls_system_name = True
        artifact_exporter_spreadsheet_xls_config_model.artifactlist_xls_artifactstatus = True
        artifact_exporter_spreadsheet_xls_config_model.artifactlist_xls_artifactpriority = True
        artifact_exporter_spreadsheet_xls_config_model.artifactlist_xls_artifacttype = True
        artifact_exporter_spreadsheet_xls_config_model.artifactlist_xls_artifact_source_path = True
        artifact_exporter_spreadsheet_xls_config_model.artifactlist_xls_artifact_storage_path = True
        artifact_exporter_spreadsheet_xls_config_model.artifactlist_xls_artifact_note_internal = True
        artifact_exporter_spreadsheet_xls_config_model.artifactlist_xls_artifact_note_external = True
        artifact_exporter_spreadsheet_xls_config_model.artifactlist_xls_artifact_note_analysisresult = True
        artifact_exporter_spreadsheet_xls_config_model.artifactlist_xls_artifact_md5 = True
        artifact_exporter_spreadsheet_xls_config_model.artifactlist_xls_artifact_sha1 = True
        artifact_exporter_spreadsheet_xls_config_model.artifactlist_xls_artifact_sha256 = True
        artifact_exporter_spreadsheet_xls_config_model.artifactlist_xls_artifact_create_time = True
        artifact_exporter_spreadsheet_xls_config_model.artifactlist_xls_artifact_modify_time = True
        artifact_exporter_spreadsheet_xls_config_model.artifactlist_xls_worksheet_artifactstatus = True
        artifact_exporter_spreadsheet_xls_config_model.artifactlist_xls_worksheet_artifacttype = True
        artifact_exporter_spreadsheet_xls_config_model.save()
        # get object
        artifactstatus_3 = Artifactstatus.objects.get(artifactstatus_name = 'artifactstatus_3')
        # add artifactstatus to choice for export
        artifact_exporter_spreadsheet_xls_config_model.artifactlist_xls_choice_artifactstatus.add(artifactstatus_3)

        """ call view section """

        # login testuser
        self.client.login(username='testuser_artifact_exporter_spreadsheet_xls', password='LTzoNHIdxiJydsaJKf1G')

        # mock timezone.now()
        t3_now = timezone.now()
        with patch.object(timezone, 'now', return_value=t3_now):

            # create spreadsheet without GET by directly calling the function
            artifact_cron()

        """ get file section """

        # refresh config
        main_config_model.refresh_from_db()
        # get time for output file
        filetime = t3_now.strftime('%Y%m%d_%H%M')
        # prepare output file path
        output_file_path = main_config_model.cron_export_path + '/' + filetime + '_artifacts.xls'
        # open file from temp folder
        xls_disk = xlrd.open_workbook(output_file_path)

        """ prepare objects section """

        # get objects
        artifact_1 = Artifact.objects.get(artifact_name = 'artifact_exporter_spreadsheet_xls_artifact_1_all_attributes')
        artifact_2 = Artifact.objects.get(artifact_name = 'artifact_exporter_spreadsheet_xls_artifact_2_no_attributes')

        # create lists for easier comparison with whole columns - artifactstatus
        artifactstatus_id_list = ['ID']
        artifactstatus_name_list = ['Artifactstatus']
        artifactstatus_note_list = ['Note']
        all_artifactstatus = Artifactstatus.objects.all().order_by('artifactstatus_name')
        for artifactstatus_object in all_artifactstatus:
            # the conversion to float was carried out, because otherwise the return values from the spreadsheet would have had to be converted to int, which would have been more time-consuming
            artifactstatus_id_list.append(float(artifactstatus_object.artifactstatus_id))
            artifactstatus_name_list.append(artifactstatus_object.artifactstatus_name)
            if artifactstatus_object.artifactstatus_note:
                artifactstatus_note_list.append(artifactstatus_object.artifactstatus_note)
            else:
                artifactstatus_note_list.append('---')

        # create lists for easier comparison with whole columns - artifacttype
        artifacttype_id_list = ['ID']
        artifacttype_name_list = ['Artifacttype']
        artifacttype_note_list = ['Note']
        all_artifacttype = Artifacttype.objects.all().order_by('artifacttype_name')
        for artifacttype_object in all_artifacttype:
            # the conversion to float was carried out, because otherwise the return values from the spreadsheet would have had to be converted to int, which would have been more time-consuming
            artifacttype_id_list.append(float(artifacttype_object.artifacttype_id))
            artifacttype_name_list.append(artifacttype_object.artifacttype_name)
            if artifacttype_object.artifacttype_note:
                artifacttype_note_list.append(artifacttype_object.artifacttype_note)
            else:
                artifacttype_note_list.append('---')

        # get sheets
        sheet_artifacts = xls_disk.sheet_by_name('artifacts')
        sheet_artifactstatus = xls_disk.sheet_by_name('artifactstatus')
        sheet_artifacttype = xls_disk.sheet_by_name('artifacttype')

        """ compare values section """

        # compare number of rows and columns
        self.assertEqual(sheet_artifacts.nrows, 6)
        self.assertEqual(sheet_artifacts.ncols, 17)
        self.assertEqual(sheet_artifactstatus.nrows, 14)
        self.assertEqual(sheet_artifactstatus.ncols, 3)
        self.assertEqual(sheet_artifacttype.nrows, 7)
        self.assertEqual(sheet_artifacttype.ncols, 3)
        # compare headlines
        self.assertEqual(sheet_artifacts.row_values(0), ['Artifact ID', 'Artifact', 'System ID', 'System', 'Artifactstatus', 'Artifactpriority', 'Artifacttype', 'Source path', 'Storage path', 'Internal note','External note',  'Analysis result', 'MD5', 'SHA1', 'SHA256', 'Created', 'Modified'])
        self.assertEqual(sheet_artifactstatus.row_values(0), ['ID', 'Artifactstatus', 'Note'])
        self.assertEqual(sheet_artifacttype.row_values(0), ['ID', 'Artifacttype', 'Note'])
        # compare content - artifact 1
        self.assertEqual(int(sheet_artifacts.cell(1,0).value), artifact_1.artifact_id)
        self.assertEqual(sheet_artifacts.cell(1,1).value, artifact_1.artifact_name)
        self.assertEqual(int(sheet_artifacts.cell(1,2).value), artifact_1.system.system_id)
        self.assertEqual(sheet_artifacts.cell(1,3).value, artifact_1.system.system_name)
        self.assertEqual(sheet_artifacts.cell(1,4).value, artifact_1.artifactstatus.artifactstatus_name)
        self.assertEqual(sheet_artifacts.cell(1,5).value, artifact_1.artifactpriority.artifactpriority_name)
        self.assertEqual(sheet_artifacts.cell(1,6).value, artifact_1.artifacttype.artifacttype_name)
        self.assertEqual(sheet_artifacts.cell(1,7).value, artifact_1.artifact_source_path)
        self.assertEqual(sheet_artifacts.cell(1,8).value, artifact_1.artifact_storage_path)
        self.assertEqual(sheet_artifacts.cell(1,9).value, 'artifact note for internal usage')      # artifact_note_internal
        self.assertEqual(sheet_artifacts.cell(1,10).value, 'artifact note for external usage')       # artifact_note_external
        self.assertEqual(sheet_artifacts.cell(1,11).value, 'artifact note for analysis result')      # artifact_note_analysisresult
        self.assertEqual(sheet_artifacts.cell(1,12).value, artifact_1.artifact_md5)
        self.assertEqual(sheet_artifacts.cell(1,13).value, artifact_1.artifact_sha1)
        self.assertEqual(sheet_artifacts.cell(1,14).value, artifact_1.artifact_sha256)
        self.assertEqual(sheet_artifacts.cell(1,15).value, '2012-11-10 12:34')
        self.assertEqual(sheet_artifacts.cell(1,16).value, '2012-11-10 12:34')
        # compare content - artifact 2
        self.assertEqual(int(sheet_artifacts.cell(2,0).value), artifact_2.artifact_id)
        self.assertEqual(sheet_artifacts.cell(2,1).value, artifact_2.artifact_name)
        self.assertEqual(int(sheet_artifacts.cell(2,2).value), artifact_2.system.system_id)
        self.assertEqual(sheet_artifacts.cell(2,3).value, artifact_2.system.system_name)
        self.assertEqual(sheet_artifacts.cell(2,4).value, artifact_2.artifactstatus.artifactstatus_name)
        self.assertEqual(sheet_artifacts.cell(2,5).value, artifact_2.artifactpriority.artifactpriority_name)
        self.assertEqual(sheet_artifacts.cell(2,6).value, artifact_2.artifacttype.artifacttype_name)
        self.assertEqual(sheet_artifacts.cell(2,7).value, '')
        self.assertEqual(sheet_artifacts.cell(2,8).value, artifact_2.artifact_storage_path)
        self.assertEqual(sheet_artifacts.cell(2,9).value, '')
        self.assertEqual(sheet_artifacts.cell(2,10).value, '')
        self.assertEqual(sheet_artifacts.cell(2,11).value, '')
        self.assertEqual(sheet_artifacts.cell(2,12).value, '')
        self.assertEqual(sheet_artifacts.cell(2,13).value, '')
        self.assertEqual(sheet_artifacts.cell(2,14).value, '')
        self.assertEqual(sheet_artifacts.cell(2,15).value, '2009-08-07 23:45')
        self.assertEqual(sheet_artifacts.cell(2,16).value, '2009-08-07 23:45')
        # compare content - artifactstatus worksheet (whole columns)
        self.assertEqual(sheet_artifactstatus.col_values(0), artifactstatus_id_list)
        self.assertEqual(sheet_artifactstatus.col_values(1), artifactstatus_name_list)
        self.assertEqual(sheet_artifactstatus.col_values(2), artifactstatus_note_list)
        # compare content - artifacttype worksheet (whole columns)
        self.assertEqual(sheet_artifacttype.col_values(0), artifacttype_id_list)
        self.assertEqual(sheet_artifacttype.col_values(1), artifacttype_name_list)
        self.assertEqual(sheet_artifacttype.col_values(2), artifacttype_note_list)
        # compare content - metadata
        self.assertEqual(sheet_artifacts.cell(4,0).value, 'Created:')
        self.assertEqual(sheet_artifacts.cell(4,1).value, t3_now.strftime('%Y-%m-%d %H:%M'))
        self.assertEqual(sheet_artifacts.cell(5,0).value, 'Created by:')
        self.assertEqual(sheet_artifacts.cell(5,1).value, 'cron')
