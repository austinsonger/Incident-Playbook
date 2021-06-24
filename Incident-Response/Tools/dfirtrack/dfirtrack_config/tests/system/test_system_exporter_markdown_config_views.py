from dfirtrack_config.models import SystemExporterMarkdownConfigModel
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.test import TestCase
import urllib.parse

class SystemExporterMarkdownConfigViewTestCase(TestCase):
    """ system exporter markdown config view tests """

    @classmethod
    def setUpTestData(cls):

        # create user
        User.objects.create_user(username='testuser_system_exporter_markdown_config', password='Rg6YK8f9LSlIY4yaBDxS')

    def test_system_exporter_markdown_config_not_logged_in(self):
        """ test exporter view """

        # create url
        destination = '/login/?next=' + urllib.parse.quote('/config/system/exporter/markdown/', safe='')
        # get response
        response = self.client.get('/config/system/exporter/markdown/', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)

    def test_system_exporter_markdown_config_logged_in(self):
        """ test exporter view """

        # login testuser
        self.client.login(username='testuser_system_exporter_markdown_config', password='Rg6YK8f9LSlIY4yaBDxS')
        # get response
        response = self.client.get('/config/system/exporter/markdown/', follow=True)
        # compare
        self.assertEqual(response.status_code, 200)

    def test_system_exporter_markdown_config_template(self):
        """ test exporter view """

        # login testuser
        self.client.login(username='testuser_system_exporter_markdown_config', password='Rg6YK8f9LSlIY4yaBDxS')
        # get response
        response = self.client.get('/config/system/exporter/markdown/')
        # compare
        self.assertTemplateUsed(response, 'dfirtrack_config/system/system_exporter_markdown_config_popup.html')

    def test_system_exporter_markdown_config_get_user_context(self):
        """ test exporter view """

        # login testuser
        self.client.login(username='testuser_system_exporter_markdown_config', password='Rg6YK8f9LSlIY4yaBDxS')
        # get response
        response = self.client.get('/config/system/exporter/markdown/')
        # compare
        self.assertEqual(str(response.context['user']), 'testuser_system_exporter_markdown_config')

    def test_system_exporter_markdown_config_redirect(self):
        """ test exporter view """

        # login testuser
        self.client.login(username='testuser_system_exporter_markdown_config', password='Rg6YK8f9LSlIY4yaBDxS')
        # create url
        destination = urllib.parse.quote('/config/system/exporter/markdown/', safe='/')
        # get response
        response = self.client.get('/config/system/exporter/markdown', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=301, target_status_code=200)

    def test_system_exporter_markdown_config_post_message(self):
            """ test exporter view """

            # login testuser
            self.client.login(username='testuser_system_exporter_markdown_config', password='Rg6YK8f9LSlIY4yaBDxS')
            # create post data
            data_dict = {
                'markdown_sorting': 'sys',
            }
            # get response
            response = self.client.post('/config/system/exporter/markdown/', data_dict)
            # get messages
            messages = list(get_messages(response.wsgi_request))
            # compare
            self.assertEqual(str(messages[-1]), 'System exporter markdown config changed')

    def test_system_exporter_markdown_config_post_redirect(self):
            """ test exporter view """

            # login testuser
            self.client.login(username='testuser_system_exporter_markdown_config', password='Rg6YK8f9LSlIY4yaBDxS')
            # create post data
            data_dict = {
                'markdown_sorting': 'sys',
            }
            # get response
            response = self.client.post('/config/system/exporter/markdown/', data_dict)
            # compare
            self.assertEqual(response.status_code, 200)

    def test_system_exporter_markdown_config_post_systemsorted(self):
            """ test exporter view """

            # login testuser
            self.client.login(username='testuser_system_exporter_markdown_config', password='Rg6YK8f9LSlIY4yaBDxS')
            # create post data
            data_dict = {
                'markdown_sorting': 'sys',
            }
            # get response
            self.client.post('/config/system/exporter/markdown/', data_dict)
            # get object
            system_exporter_markdown_config_model = SystemExporterMarkdownConfigModel.objects.get(system_exporter_markdown_config_name = 'SystemExporterMarkdownConfig')
            # compare
            self.assertEqual(system_exporter_markdown_config_model.markdown_sorting, 'sys')

    def test_system_exporter_markdown_config_post_domainsorted(self):
            """ test exporter view """

            # login testuser
            self.client.login(username='testuser_system_exporter_markdown_config', password='Rg6YK8f9LSlIY4yaBDxS')
            # create post data
            data_dict = {
                'markdown_sorting': 'dom',
            }
            # get response
            self.client.post('/config/system/exporter/markdown/', data_dict)
            # get object
            system_exporter_markdown_config_model = SystemExporterMarkdownConfigModel.objects.get(system_exporter_markdown_config_name = 'SystemExporterMarkdownConfig')
            # compare
            self.assertEqual(system_exporter_markdown_config_model.markdown_sorting, 'dom')

    def test_system_exporter_markdown_config_post_invalid_reload(self):
            """ test exporter view """

            # login testuser
            self.client.login(username='testuser_system_exporter_markdown_config', password='Rg6YK8f9LSlIY4yaBDxS')
            # create post data
            data_dict = {}
            # get response
            response = self.client.post('/config/system/exporter/markdown/', data_dict)
            # compare
            self.assertEqual(response.status_code, 200)

    def test_system_exporter_markdown_config_post_invalid_template(self):
            """ test exporter view """

            # login testuser
            self.client.login(username='testuser_system_exporter_markdown_config', password='Rg6YK8f9LSlIY4yaBDxS')
            # create post data
            data_dict = {}
            # get response
            response = self.client.post('/config/system/exporter/markdown/', data_dict)
            # compare
            self.assertTemplateUsed(response, 'dfirtrack_config/system/system_exporter_markdown_config_popup.html')
