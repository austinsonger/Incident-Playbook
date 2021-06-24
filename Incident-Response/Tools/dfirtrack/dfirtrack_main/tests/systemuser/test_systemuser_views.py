from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone
from dfirtrack_main.models import System, Systemstatus, Systemuser
import urllib.parse

class SystemuserViewTestCase(TestCase):
    """ systemuser view tests """

    @classmethod
    def setUpTestData(cls):

        # create user
        test_user = User.objects.create_user(username='testuser_systemuser', password='BXgnvXckpl1BS3I5ShJs')

        # create object
        systemstatus_1 = Systemstatus.objects.create(systemstatus_name='systemstatus_1')

        # create object
        system_1 = System.objects.create(
            system_name='system_1',
            systemstatus = systemstatus_1,
            system_modify_time = timezone.now(),
            system_created_by_user_id = test_user,
            system_modified_by_user_id = test_user,
        )

        # create object
        Systemuser.objects.create(systemuser_name='systemuser_1', system = system_1)

    def test_systemuser_list_not_logged_in(self):
        """ test list view """

        # create url
        destination = '/login/?next=' + urllib.parse.quote('/systemuser/', safe='')
        # get response
        response = self.client.get('/systemuser/', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)

    def test_systemuser_list_logged_in(self):
        """ test list view """

        # login testuser
        self.client.login(username='testuser_systemuser', password='BXgnvXckpl1BS3I5ShJs')
        # get response
        response = self.client.get('/systemuser/')
        # compare
        self.assertEqual(response.status_code, 200)

    def test_systemuser_list_template(self):
        """ test list view """

        # login testuser
        self.client.login(username='testuser_systemuser', password='BXgnvXckpl1BS3I5ShJs')
        # get response
        response = self.client.get('/systemuser/')
        # compare
        self.assertTemplateUsed(response, 'dfirtrack_main/systemuser/systemuser_list.html')

    def test_systemuser_list_get_user_context(self):
        """ test list view """

        # login testuser
        self.client.login(username='testuser_systemuser', password='BXgnvXckpl1BS3I5ShJs')
        # get response
        response = self.client.get('/systemuser/')
        # compare
        self.assertEqual(str(response.context['user']), 'testuser_systemuser')

    def test_systemuser_list_redirect(self):
        """ test list view """

        # login testuser
        self.client.login(username='testuser_systemuser', password='BXgnvXckpl1BS3I5ShJs')
        # create url
        destination = urllib.parse.quote('/systemuser/', safe='/')
        # get response
        response = self.client.get('/systemuser', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=301, target_status_code=200)

    def test_systemuser_detail_not_logged_in(self):
        """ test detail view """

        # get object
        systemuser_1 = Systemuser.objects.get(systemuser_name='systemuser_1')
        # create url
        destination = '/login/?next=' + urllib.parse.quote('/systemuser/' + str(systemuser_1.systemuser_id) + '/', safe='')
        # get response
        response = self.client.get('/systemuser/' + str(systemuser_1.systemuser_id) + '/', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)

    def test_systemuser_detail_logged_in(self):
        """ test detail view """

        # get object
        systemuser_1 = Systemuser.objects.get(systemuser_name='systemuser_1')
        # login testuser
        self.client.login(username='testuser_systemuser', password='BXgnvXckpl1BS3I5ShJs')
        # get response
        response = self.client.get('/systemuser/' + str(systemuser_1.systemuser_id) + '/')
        # compare
        self.assertEqual(response.status_code, 200)

    def test_systemuser_detail_template(self):
        """ test detail view """

        # get object
        systemuser_1 = Systemuser.objects.get(systemuser_name='systemuser_1')
        # login testuser
        self.client.login(username='testuser_systemuser', password='BXgnvXckpl1BS3I5ShJs')
        # get response
        response = self.client.get('/systemuser/' + str(systemuser_1.systemuser_id) + '/')
        # compare
        self.assertTemplateUsed(response, 'dfirtrack_main/systemuser/systemuser_detail.html')

    def test_systemuser_detail_get_user_context(self):
        """ test detail view """

        # get object
        systemuser_1 = Systemuser.objects.get(systemuser_name='systemuser_1')
        # login testuser
        self.client.login(username='testuser_systemuser', password='BXgnvXckpl1BS3I5ShJs')
        # get response
        response = self.client.get('/systemuser/' + str(systemuser_1.systemuser_id) + '/')
        # compare
        self.assertEqual(str(response.context['user']), 'testuser_systemuser')

    def test_systemuser_detail_redirect(self):
        """ test detail view """

        # get object
        systemuser_1 = Systemuser.objects.get(systemuser_name='systemuser_1')
        # login testuser
        self.client.login(username='testuser_systemuser', password='BXgnvXckpl1BS3I5ShJs')
        # create url
        destination = urllib.parse.quote('/systemuser/' + str(systemuser_1.systemuser_id) + '/', safe='/')
        # get response
        response = self.client.get('/systemuser/' + str(systemuser_1.systemuser_id), follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=301, target_status_code=200)

    def test_systemuser_add_not_logged_in(self):
        """ test add view """

        # create url
        destination = '/login/?next=' + urllib.parse.quote('/systemuser/add/', safe='')
        # get response
        response = self.client.get('/systemuser/add/', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)

    def test_systemuser_add_logged_in(self):
        """ test add view """

        # login testuser
        self.client.login(username='testuser_systemuser', password='BXgnvXckpl1BS3I5ShJs')
        # get response
        response = self.client.get('/systemuser/add/')
        # compare
        self.assertEqual(response.status_code, 200)

    def test_systemuser_add_template(self):
        """ test add view """

        # login testuser
        self.client.login(username='testuser_systemuser', password='BXgnvXckpl1BS3I5ShJs')
        # get response
        response = self.client.get('/systemuser/add/')
        # compare
        self.assertTemplateUsed(response, 'dfirtrack_main/systemuser/systemuser_add.html')

    def test_systemuser_add_get_user_context(self):
        """ test add view """

        # login testuser
        self.client.login(username='testuser_systemuser', password='BXgnvXckpl1BS3I5ShJs')
        # get response
        response = self.client.get('/systemuser/add/')
        # compare
        self.assertEqual(str(response.context['user']), 'testuser_systemuser')

    def test_systemuser_add_redirect(self):
        """ test add view """

        # login testuser
        self.client.login(username='testuser_systemuser', password='BXgnvXckpl1BS3I5ShJs')
        # create url
        destination = urllib.parse.quote('/systemuser/add/', safe='/')
        # get response
        response = self.client.get('/systemuser/add', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=301, target_status_code=200)

    def test_systemuser_add_post_redirect(self):
        """ test add view """

        # login testuser
        self.client.login(username='testuser_systemuser', password='BXgnvXckpl1BS3I5ShJs')
        # get object
        system_id = System.objects.get(system_name = 'system_1').system_id
        # create post data
        data_dict = {
            'systemuser_name': 'systemuser_add_post_test',
            'system': system_id,
        }
        # get response
        response = self.client.post('/systemuser/add/', data_dict)
        # get object
        systemuser_id = Systemuser.objects.get(systemuser_name = 'systemuser_add_post_test').systemuser_id
        # create url
        destination = urllib.parse.quote('/systemuser/' + str(systemuser_id) + '/', safe='/')
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)

    def test_systemuser_add_post_invalid_reload(self):
        """ test add view """

        # login testuser
        self.client.login(username='testuser_systemuser', password='BXgnvXckpl1BS3I5ShJs')
        # create post data
        data_dict = {}
        # get response
        response = self.client.post('/systemuser/add/', data_dict)
        # compare
        self.assertEqual(response.status_code, 200)

    def test_systemuser_add_post_invalid_template(self):
        """ test add view """

        # login testuser
        self.client.login(username='testuser_systemuser', password='BXgnvXckpl1BS3I5ShJs')
        # create post data
        data_dict = {}
        # get response
        response = self.client.post('/systemuser/add/', data_dict)
        # compare
        self.assertTemplateUsed(response, 'dfirtrack_main/systemuser/systemuser_add.html')

    def test_systemuser_edit_not_logged_in(self):
        """ test edit view """

        # get object
        systemuser_1 = Systemuser.objects.get(systemuser_name='systemuser_1')
        # create url
        destination = '/login/?next=' + urllib.parse.quote('/systemuser/' + str(systemuser_1.systemuser_id) + '/edit/', safe='')
        # get response
        response = self.client.get('/systemuser/' + str(systemuser_1.systemuser_id) + '/edit/', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)

    def test_systemuser_edit_logged_in(self):
        """ test edit view """

        # get object
        systemuser_1 = Systemuser.objects.get(systemuser_name='systemuser_1')
        # login testuser
        self.client.login(username='testuser_systemuser', password='BXgnvXckpl1BS3I5ShJs')
        # get response
        response = self.client.get('/systemuser/' + str(systemuser_1.systemuser_id) + '/edit/')
        # compare
        self.assertEqual(response.status_code, 200)

    def test_systemuser_edit_template(self):
        """ test edit view """

        # get object
        systemuser_1 = Systemuser.objects.get(systemuser_name='systemuser_1')
        # login testuser
        self.client.login(username='testuser_systemuser', password='BXgnvXckpl1BS3I5ShJs')
        # get response
        response = self.client.get('/systemuser/' + str(systemuser_1.systemuser_id) + '/edit/')
        # compare
        self.assertTemplateUsed(response, 'dfirtrack_main/systemuser/systemuser_edit.html')

    def test_systemuser_edit_get_user_context(self):
        """ test edit view """

        # get object
        systemuser_1 = Systemuser.objects.get(systemuser_name='systemuser_1')
        # login testuser
        self.client.login(username='testuser_systemuser', password='BXgnvXckpl1BS3I5ShJs')
        # get response
        response = self.client.get('/systemuser/' + str(systemuser_1.systemuser_id) + '/edit/')
        # compare
        self.assertEqual(str(response.context['user']), 'testuser_systemuser')

    def test_systemuser_edit_redirect(self):
        """ test edit view """

        # get object
        systemuser_1 = Systemuser.objects.get(systemuser_name='systemuser_1')
        # login testuser
        self.client.login(username='testuser_systemuser', password='BXgnvXckpl1BS3I5ShJs')
        # create url
        destination = urllib.parse.quote('/systemuser/' + str(systemuser_1.systemuser_id) + '/edit/', safe='/')
        # get response
        response = self.client.get('/systemuser/' + str(systemuser_1.systemuser_id) + '/edit', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=301, target_status_code=200)

    def test_systemuser_edit_post_redirect(self):
        """ test edit view """

        # login testuser
        self.client.login(username='testuser_systemuser', password='BXgnvXckpl1BS3I5ShJs')
        # get object
        system_1 = System.objects.get(system_name = 'system_1')
        # create object
        systemuser_1 = Systemuser.objects.create(
            systemuser_name = 'systemuser_edit_post_test_1',
            system = system_1,
        )
        # create post data
        data_dict = {
            'systemuser_name': 'systemuser_edit_post_test_2',
            'system': system_1.system_id,
        }
        # get response
        response = self.client.post('/systemuser/' + str(systemuser_1.systemuser_id) + '/edit/', data_dict)
        # get object
        systemuser_2 = Systemuser.objects.get(systemuser_name='systemuser_edit_post_test_2')
        # create url
        destination = urllib.parse.quote('/systemuser/' + str(systemuser_2.systemuser_id) + '/', safe='/')
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)

    def test_systemuser_edit_post_invalid_reload(self):
        """ test edit view """

        # login testuser
        self.client.login(username='testuser_systemuser', password='BXgnvXckpl1BS3I5ShJs')
        # get object
        systemuser_id = Systemuser.objects.get(systemuser_name='systemuser_1').systemuser_id
        # create post data
        data_dict = {}
        # get response
        response = self.client.post('/systemuser/' + str(systemuser_id) + '/edit/', data_dict)
        # compare
        self.assertEqual(response.status_code, 200)

    def test_systemuser_edit_post_invalid_template(self):
        """ test edit view """

        # login testuser
        self.client.login(username='testuser_systemuser', password='BXgnvXckpl1BS3I5ShJs')
        # get object
        systemuser_id = Systemuser.objects.get(systemuser_name='systemuser_1').systemuser_id
        # create post data
        data_dict = {}
        # get response
        response = self.client.post('/systemuser/' + str(systemuser_id) + '/edit/', data_dict)
        # compare
        self.assertTemplateUsed(response, 'dfirtrack_main/systemuser/systemuser_edit.html')
