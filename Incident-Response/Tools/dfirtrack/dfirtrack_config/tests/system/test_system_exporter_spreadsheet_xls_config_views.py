from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.test import TestCase
import urllib.parse

class SystemExporterSpreadsheetXlsConfigViewTestCase(TestCase):
    """ system exporter spreadsheet XLS config view tests """

    @classmethod
    def setUpTestData(cls):

        # create user
        User.objects.create_user(username='testuser_system_exporter_spreadsheet_xls_config', password='dNpRr2hEnnj147CgNhWM')

    def test_system_exporter_spreadsheet_xls_config_not_logged_in(self):
        """ test exporter view """

        # create url
        destination = '/login/?next=' + urllib.parse.quote('/config/system/exporter/spreadsheet/xls/', safe='')
        # get response
        response = self.client.get('/config/system/exporter/spreadsheet/xls/', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)

    def test_system_exporter_spreadsheet_xls_config_logged_in(self):
        """ test view """

        # login testuser
        self.client.login(username='testuser_system_exporter_spreadsheet_xls_config', password='dNpRr2hEnnj147CgNhWM')
        # get response
        response = self.client.get('/config/system/exporter/spreadsheet/xls/')
        # compare
        self.assertEqual(response.status_code, 200)

    def test_system_exporter_spreadsheet_xls_config_template(self):
        """ test exporter view """

        # login testuser
        self.client.login(username='testuser_system_exporter_spreadsheet_xls_config', password='dNpRr2hEnnj147CgNhWM')
        # get response
        response = self.client.get('/config/system/exporter/spreadsheet/xls/')
        # compare
        self.assertTemplateUsed(response, 'dfirtrack_config/system/system_exporter_spreadsheet_xls_config_popup.html')

    def test_system_exporter_spreadsheet_xls_config_get_user_context(self):
        """ test exporter view """

        # login testuser
        self.client.login(username='testuser_system_exporter_spreadsheet_xls_config', password='dNpRr2hEnnj147CgNhWM')
        # get response
        response = self.client.get('/config/system/exporter/spreadsheet/xls/')
        # compare
        self.assertEqual(str(response.context['user']), 'testuser_system_exporter_spreadsheet_xls_config')

    def test_system_exporter_spreadsheet_xls_config_redirect(self):
        """ test view """

        # login testuser
        self.client.login(username='testuser_system_exporter_spreadsheet_xls_config', password='dNpRr2hEnnj147CgNhWM')
        # create url
        destination = urllib.parse.quote('/config/system/exporter/spreadsheet/xls/', safe='/')
        # get response
        response = self.client.get('/config/system/exporter/spreadsheet/xls', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=301, target_status_code=200)

    def test_system_exporter_spreadsheet_xls_config_post_message(self):
        """ test view """

        # login testuser
        self.client.login(username='testuser_system_exporter_spreadsheet_xls_config', password='dNpRr2hEnnj147CgNhWM')
        # create post data
        data_dict = {
            'spread_xls_system_id': 'on',
        }
        # get response
        response = self.client.post('/config/system/exporter/spreadsheet/xls/', data_dict)
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare
        self.assertEqual(str(messages[-1]), 'System exporter spreadsheet XLS config changed')

    def test_system_exporter_spreadsheet_xls_config_post_redirect(self):
        """ test view """

        # login testuser
        self.client.login(username='testuser_system_exporter_spreadsheet_xls_config', password='dNpRr2hEnnj147CgNhWM')
        # create post data
        data_dict = {
            'spread_xls_system_id': 'on',
        }
        # get response
        response = self.client.post('/config/system/exporter/spreadsheet/xls/', data_dict)
        # compare
        self.assertEqual(response.status_code, 200)

# TODO: with only non-mandatory model attributes, it is not possible to get an invalid form
# TODO: remove the coverage limitation with further mandatory model attributes in 'dfirtrack_config.exporter.spreadsheet.system_exporter_spreadsheet_config_editor'
#    def test_system_exporter_spreadsheet_xls_config_post_invalid_reload(self):
#        """ test view """
#
#        # login testuser
#        self.client.login(username='testuser_system_exporter_spreadsheet_xls_config', password='dNpRr2hEnnj147CgNhWM')
#        # create post data
#        data_dict = {}
#        # get response
#        response = self.client.post('/config/system/exporter/spreadsheet/xls/', data_dict)
#        # compare
#        self.assertEqual(response.status_code, 200)
#
#    def test_system_exporter_spreadsheet_xls_config_post_invalid_template(self):
#        """ test view """
#
#        # login testuser
#        self.client.login(username='testuser_system_exporter_spreadsheet_xls_config', password='dNpRr2hEnnj147CgNhWM')
#        # create post data
#        data_dict = {}
#        # get response
#        response = self.client.get('/config/system/exporter/spreadsheet/xls/', data_dict)
#        # compare
#        self.assertTemplateUsed(response, 'dfirtrack_config/system/system_exporter_spreadsheet_xls_config_popup.html')
