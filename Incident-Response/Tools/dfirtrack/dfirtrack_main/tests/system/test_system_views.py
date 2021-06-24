from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.test import TestCase
from django.utils import timezone
from dfirtrack.settings import INSTALLED_APPS as installed_apps
from dfirtrack_artifacts.models import Artifact
#from dfirtrack_config.models import MainConfigModel
from dfirtrack_main.models import Ip, System, Systemstatus
import urllib.parse

class SystemViewTestCase(TestCase):
    """ system view tests """

    @classmethod
    def setUpTestData(cls):

        # create user
        test_user = User.objects.create_user(username='testuser_system', password='LqShcoecDud6JLRxhfKV')

        # create object
        systemstatus_1 = Systemstatus.objects.create(systemstatus_name='systemstatus_1')

        # create object
        System.objects.create(
            system_name = 'system_1',
            systemstatus = systemstatus_1,
            system_modify_time = timezone.now(),
            system_created_by_user_id = test_user,
            system_modified_by_user_id = test_user,
        )

    def test_system_list_not_logged_in(self):
        """ test list view """

        # create url
        destination = '/login/?next=' + urllib.parse.quote('/system/', safe='')
        # get response
        response = self.client.get('/system/', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)

    def test_system_list_logged_in(self):
        """ test list view """

        # login testuser
        self.client.login(username='testuser_system', password='LqShcoecDud6JLRxhfKV')
        # get response
        response = self.client.get('/system/')
        # compare
        self.assertEqual(response.status_code, 200)

    def test_system_list_template(self):
        """ test list view """

        # login testuser
        self.client.login(username='testuser_system', password='LqShcoecDud6JLRxhfKV')
        # get response
        response = self.client.get('/system/')
        # compare
        self.assertTemplateUsed(response, 'dfirtrack_main/system/system_list.html')

    def test_system_list_get_user_context(self):
        """ test list view """

        # login testuser
        self.client.login(username='testuser_system', password='LqShcoecDud6JLRxhfKV')
        # get response
        response = self.client.get('/system/')
        # compare
        self.assertEqual(str(response.context['user']), 'testuser_system')

    def test_system_list_redirect(self):
        """ test list view """

        # login testuser
        self.client.login(username='testuser_system', password='LqShcoecDud6JLRxhfKV')
        # create url
        destination = urllib.parse.quote('/system/', safe='/')
        # get response
        response = self.client.get('/system', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=301, target_status_code=200)

    def test_system_list_context_with_api(self):
        """ test list view """

        # add app to dfirtrack.settings
        if 'dfirtrack_api' not in installed_apps:
            installed_apps.append('dfirtrack_api')
        # login testuser
        self.client.login(username='testuser_system', password='LqShcoecDud6JLRxhfKV')
        # get response
        response = self.client.get('/system/')
        # compare
        self.assertTrue(response.context['dfirtrack_api'])

    def test_system_list_context_without_api(self):
        """ test list view """

        # remove app from dfirtrack.settings
        if 'dfirtrack_api' in installed_apps:
            installed_apps.remove('dfirtrack_api')
        # login testuser
        self.client.login(username='testuser_system', password='LqShcoecDud6JLRxhfKV')
        # get response
        response = self.client.get('/system/')
        # compare
        self.assertFalse(response.context['dfirtrack_api'])

    def test_system_detail_not_logged_in(self):
        """ test detail view """

        # get object
        system_1 = System.objects.get(system_name='system_1')
        # create url
        destination = '/login/?next=' + urllib.parse.quote('/system/' + str(system_1.system_id) + '/', safe='')
        # get response
        response = self.client.get('/system/' + str(system_1.system_id) + '/', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)

    def test_system_detail_logged_in(self):
        """ test detail view """

        # get object
        system_1 = System.objects.get(system_name='system_1')
        # login testuser
        self.client.login(username='testuser_system', password='LqShcoecDud6JLRxhfKV')
        # get response
        response = self.client.get('/system/' + str(system_1.system_id) + '/')
        # compare
        self.assertEqual(response.status_code, 200)

    def test_system_detail_template(self):
        """ test detail view """

        # get object
        system_1 = System.objects.get(system_name='system_1')
        # login testuser
        self.client.login(username='testuser_system', password='LqShcoecDud6JLRxhfKV')
        # get response
        response = self.client.get('/system/' + str(system_1.system_id) + '/')
        # compare
        self.assertTemplateUsed(response, 'dfirtrack_main/system/system_detail.html')

    def test_system_detail_get_user_context(self):
        """ test detail view """

        # get object
        system_1 = System.objects.get(system_name='system_1')
        # login testuser
        self.client.login(username='testuser_system', password='LqShcoecDud6JLRxhfKV')
        # get response
        response = self.client.get('/system/' + str(system_1.system_id) + '/')
        # compare
        self.assertEqual(str(response.context['user']), 'testuser_system')

    def test_system_detail_redirect(self):
        """ test detail view """

        # get object
        system_1 = System.objects.get(system_name='system_1')
        # login testuser
        self.client.login(username='testuser_system', password='LqShcoecDud6JLRxhfKV')
        # create url
        destination = urllib.parse.quote('/system/' + str(system_1.system_id) + '/', safe='/')
        # get response
        response = self.client.get('/system/' + str(system_1.system_id), follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=301, target_status_code=200)

    def test_system_detail_context_with_artifacts(self):
        """ test detail view """

        # add app to dfirtrack.settings
        if 'dfirtrack_artifacts' not in installed_apps:
            installed_apps.append('dfirtrack_artifacts')
        # get object
        system_1 = System.objects.get(system_name='system_1')
        # login testuser
        self.client.login(username='testuser_system', password='LqShcoecDud6JLRxhfKV')
        # get response
        response = self.client.get('/system/' + str(system_1.system_id) + '/')
        # compare
        self.assertTrue(response.context['dfirtrack_artifacts'])

    def test_system_detail_context_without_artifacts(self):
        """ test detail view """

        # remove app from dfirtrack.settings
        if 'dfirtrack_artifacts' in installed_apps:
            installed_apps.remove('dfirtrack_artifacts')
        # get object
        system_1 = System.objects.get(system_name='system_1')
        # login testuser
        self.client.login(username='testuser_system', password='LqShcoecDud6JLRxhfKV')
        # get response
        response = self.client.get('/system/' + str(system_1.system_id) + '/')
        # compare
        self.assertFalse(response.context['dfirtrack_artifacts'])

    def test_system_detail_queryset_context_with_artifacts(self):
        """ test detail view """

        # add app to dfirtrack.settings
        if 'dfirtrack_artifacts' not in installed_apps:
            installed_apps.append('dfirtrack_artifacts')
        # get object
        system_1 = System.objects.get(system_name='system_1')
        # login testuser
        self.client.login(username='testuser_system', password='LqShcoecDud6JLRxhfKV')
        # get queryset
        artifact_queryset = Artifact.objects.filter(system=system_1)
        # get response
        response = self.client.get('/system/' + str(system_1.system_id) + '/')
        # compare
        self.assertEqual(type(response.context['artifacts']), type(artifact_queryset))

    def test_system_detail_context_with_api(self):
        """ test detail view """

        # add app to dfirtrack.settings
        if 'dfirtrack_api' not in installed_apps:
            installed_apps.append('dfirtrack_api')
        # get object
        system_1 = System.objects.get(system_name='system_1')
        # login testuser
        self.client.login(username='testuser_system', password='LqShcoecDud6JLRxhfKV')
        # get response
        response = self.client.get('/system/' + str(system_1.system_id) + '/')
        # compare
        self.assertTrue(response.context['dfirtrack_api'])

    def test_system_detail_context_without_api(self):
        """ test detail view """

        # remove app from dfirtrack.settings
        if 'dfirtrack_api' in installed_apps:
            installed_apps.remove('dfirtrack_api')
        # get object
        system_1 = System.objects.get(system_name='system_1')
        # login testuser
        self.client.login(username='testuser_system', password='LqShcoecDud6JLRxhfKV')
        # get response
        response = self.client.get('/system/' + str(system_1.system_id) + '/')
        # compare
        self.assertFalse(response.context['dfirtrack_api'])

    def test_system_add_not_logged_in(self):
        """ test add view """

        # create url
        destination = '/login/?next=' + urllib.parse.quote('/system/add/', safe='')
        # get response
        response = self.client.get('/system/add/', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)

    def test_system_add_logged_in(self):
        """ test add view """

        # login testuser
        self.client.login(username='testuser_system', password='LqShcoecDud6JLRxhfKV')
        # get response
        response = self.client.get('/system/add/')
        # compare
        self.assertEqual(response.status_code, 200)

    def test_system_add_template(self):
        """ test add view """

        # login testuser
        self.client.login(username='testuser_system', password='LqShcoecDud6JLRxhfKV')
        # get response
        response = self.client.get('/system/add/')
        # compare
        self.assertTemplateUsed(response, 'dfirtrack_main/system/system_add.html')

    def test_system_add_get_user_context(self):
        """ test add view """

        # login testuser
        self.client.login(username='testuser_system', password='LqShcoecDud6JLRxhfKV')
        # get response
        response = self.client.get('/system/add/')
        # compare
        self.assertEqual(str(response.context['user']), 'testuser_system')

    def test_system_add_redirect(self):
        """ test add view """

        # login testuser
        self.client.login(username='testuser_system', password='LqShcoecDud6JLRxhfKV')
        # create url
        destination = urllib.parse.quote('/system/add/', safe='/')
        # get response
        response = self.client.get('/system/add', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=301, target_status_code=200)

    def test_system_add_post_redirect(self):
        """ test add view """

        # login testuser
        self.client.login(username='testuser_system', password='LqShcoecDud6JLRxhfKV')
        # get object
        systemstatus_id = Systemstatus.objects.get(systemstatus_name='systemstatus_1').systemstatus_id
        # create post data
        data_dict = {
            'system_name': 'system_add_post_test',
            'systemstatus': systemstatus_id,
            'iplist': '',
        }
        # get response
        response = self.client.post('/system/add/', data_dict)
        # get object
        system_id = System.objects.get(system_name = 'system_add_post_test').system_id
        # create url
        destination = urllib.parse.quote('/system/' + str(system_id) + '/', safe='/')
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)

    def test_system_add_post_invalid_reload(self):
        """ test add view """

        # login testuser
        self.client.login(username='testuser_system', password='LqShcoecDud6JLRxhfKV')
        # create post data
        data_dict = {}
        # get response
        response = self.client.post('/system/add/', data_dict)
        # compare
        self.assertEqual(response.status_code, 200)

    def test_system_add_post_invalid_template(self):
        """ test add view """

        # login testuser
        self.client.login(username='testuser_system', password='LqShcoecDud6JLRxhfKV')
        # create post data
        data_dict = {}
        # get response
        response = self.client.post('/system/add/', data_dict)
        # compare
        self.assertTemplateUsed(response, 'dfirtrack_main/system/system_add.html')

    def test_system_add_post_ips_save_valid(self):
        """ test add view """

        # login testuser
        self.client.login(username='testuser_system', password='LqShcoecDud6JLRxhfKV')
        # get object
        systemstatus_id = Systemstatus.objects.get(systemstatus_name='systemstatus_1').systemstatus_id
        # create post data
        data_dict = {
            'system_name': 'system_add_post_ips_save_valid_test',
            'systemstatus': systemstatus_id,
            'iplist': '127.0.0.3\n127.0.0.4',
        }
        # get response
        self.client.post('/system/add/', data_dict)
        # get object
        system_1 = System.objects.get(system_name = 'system_add_post_ips_save_valid_test')
        # get objects from system
        system_ip_3 = system_1.ip.filter(ip_ip = '127.0.0.3')[0]
        system_ip_4 = system_1.ip.filter(ip_ip = '127.0.0.4')[0]
        # get objects
        ip_3 = Ip.objects.get(ip_ip = '127.0.0.3')
        ip_4 = Ip.objects.get(ip_ip = '127.0.0.4')
        # compare
        self.assertEqual(system_ip_3, ip_3)
        self.assertEqual(system_ip_4, ip_4)

    def test_system_add_post_ips_save_empty_line_message(self):
        """ test add view """

        # login testuser
        self.client.login(username='testuser_system', password='LqShcoecDud6JLRxhfKV')
        # get object
        systemstatus_id = Systemstatus.objects.get(systemstatus_name='systemstatus_1').systemstatus_id
        # create post data
        data_dict = {
            'system_name': 'system_add_post_ips_save_empty_line_test',
            'systemstatus': systemstatus_id,
            'iplist': '\n127.0.0.5',
        }
        # get response
        response = self.client.post('/system/add/', data_dict)
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare
        self.assertEqual(str(messages[0]), 'Empty line instead of IP was provided')

    def test_system_add_post_ips_save_no_ip_message(self):
        """ test add view """

        # login testuser
        self.client.login(username='testuser_system', password='LqShcoecDud6JLRxhfKV')
        # get object
        systemstatus_id = Systemstatus.objects.get(systemstatus_name='systemstatus_1').systemstatus_id
        # create post data
        data_dict = {
            'system_name': 'system_add_post_ips_save_no_ip_test',
            'systemstatus': systemstatus_id,
            'iplist': 'foobar\n127.0.0.6',
        }
        # get response
        response = self.client.post('/system/add/', data_dict)
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare
        self.assertEqual(str(messages[0]), 'Provided string was no IP')

    def test_system_add_post_ips_save_ip_existing_message(self):
        """ test add view """

        # login testuser
        self.client.login(username='testuser_system', password='LqShcoecDud6JLRxhfKV')
        # create object
        Ip.objects.create(ip_ip = '127.0.0.7')
        # get object
        systemstatus_id = Systemstatus.objects.get(systemstatus_name='systemstatus_1').systemstatus_id
        # create post data
        data_dict = {
            'system_name': 'system_add_post_ips_save_ip_existing_test',
            'systemstatus': systemstatus_id,
            'iplist': '127.0.0.7',
        }
        # get response
        response = self.client.post('/system/add/', data_dict)
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare
        self.assertEqual(str(messages[0]), 'IP already exists in database')

    def test_system_edit_not_logged_in(self):
        """ test edit view """

        # get object
        system_1 = System.objects.get(system_name='system_1')
        # create url
        destination = '/login/?next=' + urllib.parse.quote('/system/' + str(system_1.system_id) + '/edit/', safe='')
        # get response
        response = self.client.get('/system/' + str(system_1.system_id) + '/edit/', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)

    def test_system_edit_logged_in(self):
        """ test edit view """

        # get object
        system_1 = System.objects.get(system_name='system_1')
        # login testuser
        self.client.login(username='testuser_system', password='LqShcoecDud6JLRxhfKV')
        # get response
        response = self.client.get('/system/' + str(system_1.system_id) + '/edit/')
        # compare
        self.assertEqual(response.status_code, 200)

    def test_system_edit_template(self):
        """ test edit view """

        # get object
        system_1 = System.objects.get(system_name='system_1')
        # login testuser
        self.client.login(username='testuser_system', password='LqShcoecDud6JLRxhfKV')
        # get response
        response = self.client.get('/system/' + str(system_1.system_id) + '/edit/')
        # compare
        self.assertTemplateUsed(response, 'dfirtrack_main/system/system_edit.html')

    def test_system_edit_get_user_context(self):
        """ test edit view """

        # get object
        system_1 = System.objects.get(system_name='system_1')
        # login testuser
        self.client.login(username='testuser_system', password='LqShcoecDud6JLRxhfKV')
        # get response
        response = self.client.get('/system/' + str(system_1.system_id) + '/edit/')
        # compare
        self.assertEqual(str(response.context['user']), 'testuser_system')

    def test_system_edit_redirect(self):
        """ test edit view """

        # get object
        system_1 = System.objects.get(system_name='system_1')
        # login testuser
        self.client.login(username='testuser_system', password='LqShcoecDud6JLRxhfKV')
        # create url
        destination = urllib.parse.quote('/system/' + str(system_1.system_id) + '/edit/', safe='/')
        # get response
        response = self.client.get('/system/' + str(system_1.system_id) + '/edit', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=301, target_status_code=200)

    def test_system_edit_initial_ipstring(self):
        """ test edit view """

        # get object
        system_1 = System.objects.get(system_name='system_1')
        # create objects
        ip_1 = Ip.objects.create(ip_ip = '127.0.0.1')
        ip_2 = Ip.objects.create(ip_ip = '127.0.0.2')
        # append objects
        system_1.ip.add(ip_1)
        system_1.ip.add(ip_2)
        # login testuser
        self.client.login(username='testuser_system', password='LqShcoecDud6JLRxhfKV')
        # get response
        response = self.client.get('/system/' + str(system_1.system_id) + '/edit/')
        # compare
        self.assertEqual(response.context['form'].initial['iplist'], '127.0.0.1\n127.0.0.2')

    def test_system_edit_post_redirect(self):
        """ test edit view """

        # login testuser
        self.client.login(username='testuser_system', password='LqShcoecDud6JLRxhfKV')
        # get user
        test_user = User.objects.get(username = 'testuser_system')
        # get object
        systemstatus_1 = Systemstatus.objects.get(systemstatus_name='systemstatus_1')
        # create object
        systemstatus_2 = Systemstatus.objects.create(systemstatus_name='systemstatus_2')
        # create object
        system_1 = System.objects.create(
            system_name = 'system_edit_post_test_1',
            systemstatus = systemstatus_1,
            system_modify_time = timezone.now(),
            system_created_by_user_id = test_user,
            system_modified_by_user_id = test_user,
        )
        # create post data
        data_dict = {
            'system_name': 'system_edit_post_test_1',
            'systemstatus': systemstatus_2.systemstatus_id,
            'iplist': '',
        }
        # get response
        response = self.client.post('/system/' + str(system_1.system_id) + '/edit/', data_dict)
        # get object
        system_2 = System.objects.get(system_name='system_edit_post_test_1')
        # create url
        destination = urllib.parse.quote('/system/' + str(system_2.system_id) + '/', safe='/')
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)

    def test_system_edit_post_invalid_reload(self):
        """ test edit view """

        # login testuser
        self.client.login(username='testuser_system', password='LqShcoecDud6JLRxhfKV')
        # get object
        system_id = System.objects.get(system_name='system_1').system_id
        # create post data
        data_dict = {}
        # get response
        response = self.client.post('/system/' + str(system_id) + '/edit/', data_dict)
        # compare
        self.assertEqual(response.status_code, 200)

    def test_system_edit_post_invalid_template(self):
        """ test edit view """

        # login testuser
        self.client.login(username='testuser_system', password='LqShcoecDud6JLRxhfKV')
        # get object
        system_id = System.objects.get(system_name='system_1').system_id
        # create post data
        data_dict = {}
        # get response
        response = self.client.post('/system/' + str(system_id) + '/edit/', data_dict)
        # compare
        self.assertTemplateUsed(response, 'dfirtrack_main/system/system_edit.html')

# TODO: does not work so far, model change in config does not affect the underlying view (it is not model related)
#    def test_system_edit_post_system_name_editable_redirect(self):
#        """ test edit view """
#
#        # login testuser
#        self.client.login(username='testuser_system', password='LqShcoecDud6JLRxhfKV')
#        # get config model
#        main_config_model = MainConfigModel.objects.get(main_config_name = 'MainConfig')
#        # set config model
#        main_config_model.system_name_editable = True
#        main_config_model.save()
#        # get user
#        test_user = User.objects.get(username = 'testuser_system')
#        # get object
#        systemstatus_1 = Systemstatus.objects.get(systemstatus_name='systemstatus_1')
#        # create object
#        system_1 = System.objects.create(
#            system_name = 'system_edit_post_test_3',
#            systemstatus = systemstatus_1,
#            system_modify_time = timezone.now(),
#            system_created_by_user_id = test_user,
#            system_modified_by_user_id = test_user,
#        )
#        # create post data
#        data_dict = {
#            'system_name': 'system_edit_post_test_4',
#            'systemstatus': systemstatus_1.systemstatus_id,
#            'iplist': '',
#        }
#        # get response
#        response = self.client.post('/system/' + str(system_1.system_id) + '/edit/', data_dict)
#        # get object
#        system_2 = System.objects.get(system_name='system_edit_post_test_4')
#        # create url
#        destination = urllib.parse.quote('/system/' + str(system_2.system_id) + '/', safe='/')
#        # compare
#        self.assertRedirects(response, destination, status_code=302, target_status_code=200)

    def test_system_edit_post_system_name_not_editable_redirect(self):
        """ test edit view """

        # login testuser
        self.client.login(username='testuser_system', password='LqShcoecDud6JLRxhfKV')
        # get user
        test_user = User.objects.get(username = 'testuser_system')
        # get object
        systemstatus_1 = Systemstatus.objects.get(systemstatus_name='systemstatus_1')
        # create object
        system_1 = System.objects.create(
            system_name = 'system_edit_post_test_5',
            systemstatus = systemstatus_1,
            system_modify_time = timezone.now(),
            system_created_by_user_id = test_user,
            system_modified_by_user_id = test_user,
        )
        # create post data
        data_dict = {
            'system_name': 'system_edit_post_test_6',
            'systemstatus': systemstatus_1.systemstatus_id,
            'iplist': '',
        }
        # get response
        response = self.client.post('/system/' + str(system_1.system_id) + '/edit/', data_dict)
        # get object
        system_2 = System.objects.get(system_name='system_edit_post_test_5')
        # create url
        destination = urllib.parse.quote('/system/' + str(system_2.system_id) + '/', safe='/')
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)
