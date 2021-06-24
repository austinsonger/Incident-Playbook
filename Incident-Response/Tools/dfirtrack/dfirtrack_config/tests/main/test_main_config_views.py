from dfirtrack_config.models import MainConfigModel
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.test import TestCase
import urllib.parse

class MainConfigViewTestCase(TestCase):
    """ main config view tests """

    @classmethod
    def setUpTestData(cls):

        # create user
        User.objects.create_user(username='testuser_main_config', password='4jl475KM3wof8w5mQ7SN')

    def test_main_config_not_logged_in(self):
        """ test view """

        # create url
        destination = '/login/?next=' + urllib.parse.quote('/config/main/', safe='')
        # get response
        response = self.client.get('/config/main/', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)

    def test_main_config_logged_in(self):
        """ test view """

        # login testuser
        self.client.login(username='testuser_main_config', password='4jl475KM3wof8w5mQ7SN')
        # get response
        response = self.client.get('/config/main/')
        # compare
        self.assertEqual(response.status_code, 200)

    def test_main_config_template(self):
        """ test view """

        # login testuser
        self.client.login(username='testuser_main_config', password='4jl475KM3wof8w5mQ7SN')
        # get response
        response = self.client.get('/config/main/')
        # compare
        self.assertTemplateUsed(response, 'dfirtrack_config/main_config_popup.html')

    def test_main_config_get_user_context(self):
        """ test view """

        # login testuser
        self.client.login(username='testuser_main_config', password='4jl475KM3wof8w5mQ7SN')
        # get response
        response = self.client.get('/config/main/')
        # compare
        self.assertEqual(str(response.context['user']), 'testuser_main_config')

    def test_main_config_redirect(self):
        """ test view """

        # login testuser
        self.client.login(username='testuser_main_config', password='4jl475KM3wof8w5mQ7SN')
        # create url
        destination = urllib.parse.quote('/config/main/', safe='/')
        # get response
        response = self.client.get('/config/main', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=301, target_status_code=200)

    def test_main_config_post_message(self):
        """ test view """

        # login testuser
        self.client.login(username='testuser_main_config', password='4jl475KM3wof8w5mQ7SN')
        # create post data
        data_dict = {
            'system_name_editable': 'on',
            'statushistory_entry_numbers': 6,
            'cron_export_path': '/tmp',
            'cron_username': 'cron',
        }
        # get response
        response = self.client.post('/config/main/', data_dict)
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare
        self.assertEqual(str(messages[-1]), 'Main config changed')

    def test_main_config_post_redirect(self):
        """ test view """

        # login testuser
        self.client.login(username='testuser_main_config', password='4jl475KM3wof8w5mQ7SN')
        # create post data
        data_dict = {
            'system_name_editable': 'on',
            'statushistory_entry_numbers': 7,
            'cron_export_path': '/tmp',
            'cron_username': 'cron',
        }
        # get response
        response = self.client.post('/config/main/', data_dict)
        # compare
        self.assertEqual(response.status_code, 200)

    def test_main_config_post_system_name_editable_true(self):
        """ test view """

        # login testuser
        self.client.login(username='testuser_main_config', password='4jl475KM3wof8w5mQ7SN')
        # get object
        main_config_model = MainConfigModel.objects.get(main_config_name = 'MainConfig')
        # set opposite value
        main_config_model.system_name_editable = False
        # save config
        main_config_model.save()
        # compare (before post)
        self.assertFalse(main_config_model.system_name_editable)
        # create post data
        data_dict = {
            'system_name_editable': 'on',
            'statushistory_entry_numbers': 8,
            'cron_export_path': '/tmp',
            'cron_username': 'cron',
        }
        # get response
        self.client.post('/config/main/', data_dict)
        # refresh object
        main_config_model.refresh_from_db()
        # compare
        self.assertTrue(main_config_model.system_name_editable)

    def test_main_config_post_system_name_editable_false(self):
        """ test view """

        # login testuser
        self.client.login(username='testuser_main_config', password='4jl475KM3wof8w5mQ7SN')
        # get object
        main_config_model = MainConfigModel.objects.get(main_config_name = 'MainConfig')
        # set opposite value
        main_config_model.system_name_editable = True
        # save config
        main_config_model.save()
        # compare (before post)
        self.assertTrue(main_config_model.system_name_editable)
        # create post data
        data_dict = {
            'statushistory_entry_numbers': 9,
            'cron_export_path': '/tmp',
            'cron_username': 'cron',
        }
        # get response
        self.client.post('/config/main/', data_dict)
        # get object
        main_config_model = MainConfigModel.objects.get(main_config_name = 'MainConfig')
        # compare
        self.assertFalse(main_config_model.system_name_editable)

    def test_main_config_post_invalid_reload(self):
        """ test view """

        # login testuser
        self.client.login(username='testuser_main_config', password='4jl475KM3wof8w5mQ7SN')
        # create post data
        data_dict = {}
        # get response
        response = self.client.post('/config/main/', data_dict)
        # compare
        self.assertEqual(response.status_code, 200)

    def test_main_config_post_invalid_template(self):
        """ test view """

        # login testuser
        self.client.login(username='testuser_main_config', password='4jl475KM3wof8w5mQ7SN')
        # create post data
        data_dict = {}
        # get response
        response = self.client.post('/config/main/', data_dict)
        # compare
        self.assertTemplateUsed(response, 'dfirtrack_config/main_config_popup.html')
