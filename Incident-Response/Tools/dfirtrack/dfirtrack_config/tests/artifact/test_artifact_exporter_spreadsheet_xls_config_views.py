from dfirtrack_artifacts.models import Artifactstatus
from dfirtrack_config.models import ArtifactExporterSpreadsheetXlsConfigModel
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.test import TestCase
import urllib.parse

class ArtifactExporterSpreadsheetXlsConfigViewTestCase(TestCase):
    """ artifact exporter spreadsheet XLS config view tests """

    @classmethod
    def setUpTestData(cls):

        # create user
        User.objects.create_user(username='testuser_artifact_exporter_spreadsheet_xls_config', password='i3jLLnbrAEgel24sGs9i')

        # create objects
        Artifactstatus.objects.create(
            artifactstatus_name = 'artifactstatus_1',
            artifactstatus_slug = 'artifactstatus_1',
        )
        Artifactstatus.objects.create(
            artifactstatus_name = 'artifactstatus_2',
            artifactstatus_slug = 'artifactstatus_2',
        )

    def test_artifact_exporter_spreadsheet_xls_config_not_logged_in(self):
        """ test exporter view """

        # create url
        destination = '/login/?next=' + urllib.parse.quote('/config/artifact/exporter/spreadsheet/xls/', safe='')
        # get response
        response = self.client.get('/config/artifact/exporter/spreadsheet/xls/', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)

    def test_artifact_exporter_spreadsheet_xls_config_logged_in(self):
        """ test view """

        # login testuser
        self.client.login(username='testuser_artifact_exporter_spreadsheet_xls_config', password='i3jLLnbrAEgel24sGs9i')
        # get response
        response = self.client.get('/config/artifact/exporter/spreadsheet/xls/')
        # compare
        self.assertEqual(response.status_code, 200)

    def test_artifact_exporter_spreadsheet_xls_config_template(self):
        """ test exporter view """

        # login testuser
        self.client.login(username='testuser_artifact_exporter_spreadsheet_xls_config', password='i3jLLnbrAEgel24sGs9i')
        # get response
        response = self.client.get('/config/artifact/exporter/spreadsheet/xls/')
        # compare
        self.assertTemplateUsed(response, 'dfirtrack_config/artifact/artifact_exporter_spreadsheet_xls_config_popup.html')

    def test_artifact_exporter_spreadsheet_xls_config_get_user_context(self):
        """ test exporter view """

        # login testuser
        self.client.login(username='testuser_artifact_exporter_spreadsheet_xls_config', password='i3jLLnbrAEgel24sGs9i')
        # get response
        response = self.client.get('/config/artifact/exporter/spreadsheet/xls/')
        # compare
        self.assertEqual(str(response.context['user']), 'testuser_artifact_exporter_spreadsheet_xls_config')

    def test_artifact_exporter_spreadsheet_xls_config_redirect(self):
        """ test view """

        # login testuser
        self.client.login(username='testuser_artifact_exporter_spreadsheet_xls_config', password='i3jLLnbrAEgel24sGs9i')
        # create url
        destination = urllib.parse.quote('/config/artifact/exporter/spreadsheet/xls/', safe='/')
        # get response
        response = self.client.get('/config/artifact/exporter/spreadsheet/xls', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=301, target_status_code=200)

    def test_artifact_exporter_spreadsheet_xls_config_post_message(self):
        """ test view """

        # login testuser
        self.client.login(username='testuser_artifact_exporter_spreadsheet_xls_config', password='i3jLLnbrAEgel24sGs9i')
        # get objects
        artifactstatus_1 = Artifactstatus.objects.get(artifactstatus_name = 'artifactstatus_1').artifactstatus_id
        artifactstatus_2 = Artifactstatus.objects.get(artifactstatus_name = 'artifactstatus_2').artifactstatus_id
        # create post data
        data_dict = {
            'artifactlist_xls_choice_artifactstatus': [str(artifactstatus_1), str(artifactstatus_2)],
        }
        # get response
        response = self.client.post('/config/artifact/exporter/spreadsheet/xls/', data_dict)
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare
        self.assertEqual(str(messages[-1]), 'Artifact exporter spreadsheet XLS config changed')

    def test_artifact_exporter_spreadsheet_xls_config_post_redirect(self):
        """ test view """

        # login testuser
        self.client.login(username='testuser_artifact_exporter_spreadsheet_xls_config', password='i3jLLnbrAEgel24sGs9i')
        # get objects
        artifactstatus_1 = Artifactstatus.objects.get(artifactstatus_name = 'artifactstatus_1').artifactstatus_id
        artifactstatus_2 = Artifactstatus.objects.get(artifactstatus_name = 'artifactstatus_2').artifactstatus_id
        # create post data
        data_dict = {
            'artifactlist_xls_choice_artifactstatus': [str(artifactstatus_1), str(artifactstatus_2)],
        }
        # get response
        response = self.client.post('/config/artifact/exporter/spreadsheet/xls/', data_dict)
        # compare
        self.assertEqual(response.status_code, 200)

    def test_artifact_exporter_spreadsheet_xls_config_post_artifact_id_false(self):
        """ test view """

        # login testuser
        self.client.login(username='testuser_artifact_exporter_spreadsheet_xls_config', password='i3jLLnbrAEgel24sGs9i')
        # get objects
        artifactstatus_1 = Artifactstatus.objects.get(artifactstatus_name = 'artifactstatus_1').artifactstatus_id
        artifactstatus_2 = Artifactstatus.objects.get(artifactstatus_name = 'artifactstatus_2').artifactstatus_id
        # create post data
        data_dict = {
            'artifactlist_xls_choice_artifactstatus': [str(artifactstatus_1), str(artifactstatus_2)],
        }
        # get response
        self.client.post('/config/artifact/exporter/spreadsheet/xls/', data_dict)
        # get object
        artifact_exporter_spreadsheet_xls_config_model = ArtifactExporterSpreadsheetXlsConfigModel.objects.get(artifact_exporter_spreadsheet_xls_config_name = 'ArtifactExporterSpreadsheetXlsConfig')
        # compare
        self.assertFalse(artifact_exporter_spreadsheet_xls_config_model.artifactlist_xls_artifact_id)

    def test_artifact_exporter_spreadsheet_xls_config_post_artifact_id_true(self):
        """ test view """

        # login testuser
        self.client.login(username='testuser_artifact_exporter_spreadsheet_xls_config', password='i3jLLnbrAEgel24sGs9i')
        # get objects
        artifactstatus_1 = Artifactstatus.objects.get(artifactstatus_name = 'artifactstatus_1').artifactstatus_id
        artifactstatus_2 = Artifactstatus.objects.get(artifactstatus_name = 'artifactstatus_2').artifactstatus_id
        # create post data
        data_dict = {
            'artifactlist_xls_choice_artifactstatus': [str(artifactstatus_1), str(artifactstatus_2)],
            'artifactlist_xls_artifact_id': 'on',
        }
        # get response
        self.client.post('/config/artifact/exporter/spreadsheet/xls/', data_dict)
        # get object
        artifact_exporter_spreadsheet_xls_config_model = ArtifactExporterSpreadsheetXlsConfigModel.objects.get(artifact_exporter_spreadsheet_xls_config_name = 'ArtifactExporterSpreadsheetXlsConfig')
        # compare
        self.assertTrue(artifact_exporter_spreadsheet_xls_config_model.artifactlist_xls_artifact_id)

    def test_artifact_exporter_spreadsheet_xls_config_post_invalid_reload(self):
        """ test view """

        # login testuser
        self.client.login(username='testuser_artifact_exporter_spreadsheet_xls_config', password='i3jLLnbrAEgel24sGs9i')
        # create post data
        data_dict = {}
        # get response
        response = self.client.post('/config/artifact/exporter/spreadsheet/xls/', data_dict)
        # compare
        self.assertEqual(response.status_code, 200)

    def test_artifact_exporter_spreadsheet_xls_config_post_invalid_template(self):
        """ test view """

        # login testuser
        self.client.login(username='testuser_artifact_exporter_spreadsheet_xls_config', password='i3jLLnbrAEgel24sGs9i')
        # create post data
        data_dict = {}
        # get response
        response = self.client.post('/config/artifact/exporter/spreadsheet/xls/', data_dict)
        # compare
        self.assertTemplateUsed(response, 'dfirtrack_config/artifact/artifact_exporter_spreadsheet_xls_config_popup.html')
