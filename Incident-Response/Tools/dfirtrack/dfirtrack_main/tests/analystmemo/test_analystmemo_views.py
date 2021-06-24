from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone
from dfirtrack_main.models import Analystmemo, System, Systemstatus
import urllib.parse

class AnalystmemoViewTestCase(TestCase):
    """ analystmemo view tests """

    @classmethod
    def setUpTestData(cls):

        # create user
        test_user = User.objects.create_user(username='testuser_analystmemo', password='M4d878CFQiHcJQrZr4iN')

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
        Analystmemo.objects.create(
            analystmemo_note='lorem ipsum',
            system = system_1,
            analystmemo_created_by_user_id = test_user,
            analystmemo_modified_by_user_id = test_user,
        )

    def test_analystmemo_list_not_logged_in(self):
        """ test list view """

        # create url
        destination = '/login/?next=' + urllib.parse.quote('/analystmemo/', safe='')
        # get response
        response = self.client.get('/analystmemo/', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)

    def test_analystmemo_list_logged_in(self):
        """ test list view """

        # login testuser
        self.client.login(username='testuser_analystmemo', password='M4d878CFQiHcJQrZr4iN')
        # get response
        response = self.client.get('/analystmemo/')
        # compare
        self.assertEqual(response.status_code, 200)

    def test_analystmemo_list_template(self):
        """ test list view """

        # login testuser
        self.client.login(username='testuser_analystmemo', password='M4d878CFQiHcJQrZr4iN')
        # get response
        response = self.client.get('/analystmemo/')
        # compare
        self.assertTemplateUsed(response, 'dfirtrack_main/analystmemo/analystmemo_list.html')

    def test_analystmemo_list_get_user_context(self):
        """ test list view """

        # login testuser
        self.client.login(username='testuser_analystmemo', password='M4d878CFQiHcJQrZr4iN')
        # get response
        response = self.client.get('/analystmemo/')
        # compare
        self.assertEqual(str(response.context['user']), 'testuser_analystmemo')

    def test_analystmemo_list_redirect(self):
        """ test list view """

        # login testuser
        self.client.login(username='testuser_analystmemo', password='M4d878CFQiHcJQrZr4iN')
        # create url
        destination = urllib.parse.quote('/analystmemo/', safe='/')
        # get response
        response = self.client.get('/analystmemo', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=301, target_status_code=200)

    def test_analystmemo_detail_not_logged_in(self):
        """ test detail view """

        # get object
        analystmemo_1 = Analystmemo.objects.get(analystmemo_note='lorem ipsum')
        # create url
        destination = '/login/?next=' + urllib.parse.quote('/analystmemo/' + str(analystmemo_1.analystmemo_id) + '/', safe='')
        # get response
        response = self.client.get('/analystmemo/' + str(analystmemo_1.analystmemo_id) + '/', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)

    def test_analystmemo_detail_logged_in(self):
        """ test detail view """

        # get object
        analystmemo_1 = Analystmemo.objects.get(analystmemo_note='lorem ipsum')
        # login testuser
        self.client.login(username='testuser_analystmemo', password='M4d878CFQiHcJQrZr4iN')
        # get response
        response = self.client.get('/analystmemo/' + str(analystmemo_1.analystmemo_id) + '/')
        # compare
        self.assertEqual(response.status_code, 200)

    def test_analystmemo_detail_template(self):
        """ test detail view """

        # get object
        analystmemo_1 = Analystmemo.objects.get(analystmemo_note='lorem ipsum')
        # login testuser
        self.client.login(username='testuser_analystmemo', password='M4d878CFQiHcJQrZr4iN')
        # get response
        response = self.client.get('/analystmemo/' + str(analystmemo_1.analystmemo_id) + '/')
        # compare
        self.assertTemplateUsed(response, 'dfirtrack_main/analystmemo/analystmemo_detail.html')

    def test_analystmemo_detail_get_user_context(self):
        """ test detail view """

        # get object
        analystmemo_1 = Analystmemo.objects.get(analystmemo_note='lorem ipsum')
        # login testuser
        self.client.login(username='testuser_analystmemo', password='M4d878CFQiHcJQrZr4iN')
        # get response
        response = self.client.get('/analystmemo/' + str(analystmemo_1.analystmemo_id) + '/')
        # compare
        self.assertEqual(str(response.context['user']), 'testuser_analystmemo')

    def test_analystmemo_detail_redirect(self):
        """ test detail view """

        # get object
        analystmemo_1 = Analystmemo.objects.get(analystmemo_note='lorem ipsum')
        # login testuser
        self.client.login(username='testuser_analystmemo', password='M4d878CFQiHcJQrZr4iN')
        # create url
        destination = urllib.parse.quote('/analystmemo/' + str(analystmemo_1.analystmemo_id) + '/', safe='/')
        # get response
        response = self.client.get('/analystmemo/' + str(analystmemo_1.analystmemo_id), follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=301, target_status_code=200)

    def test_analystmemo_add_not_logged_in(self):
        """ test add view """

        # create url
        destination = '/login/?next=' + urllib.parse.quote('/analystmemo/add/', safe='')
        # get response
        response = self.client.get('/analystmemo/add/', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)

    def test_analystmemo_add_logged_in(self):
        """ test add view """

        # login testuser
        self.client.login(username='testuser_analystmemo', password='M4d878CFQiHcJQrZr4iN')
        # get response
        response = self.client.get('/analystmemo/add/')
        # compare
        self.assertEqual(response.status_code, 200)

    def test_analystmemo_add_system_selected(self):
        """ test add view """

        # login testuser
        self.client.login(username='testuser_analystmemo', password='M4d878CFQiHcJQrZr4iN')
        # get object
        system_id = System.objects.get(system_name = 'system_1').system_id
        # get response
        response = self.client.get('/analystmemo/add/?system=' + str(system_id))
        # compare
        self.assertEqual(response.status_code, 200)

    def test_analystmemo_add_template(self):
        """ test add view """

        # login testuser
        self.client.login(username='testuser_analystmemo', password='M4d878CFQiHcJQrZr4iN')
        # get response
        response = self.client.get('/analystmemo/add/')
        # compare
        self.assertTemplateUsed(response, 'dfirtrack_main/analystmemo/analystmemo_add.html')

    def test_analystmemo_add_get_user_context(self):
        """ test add view """

        # login testuser
        self.client.login(username='testuser_analystmemo', password='M4d878CFQiHcJQrZr4iN')
        # get response
        response = self.client.get('/analystmemo/add/')
        # compare
        self.assertEqual(str(response.context['user']), 'testuser_analystmemo')

    def test_analystmemo_add_redirect(self):
        """ test add view """

        # login testuser
        self.client.login(username='testuser_analystmemo', password='M4d878CFQiHcJQrZr4iN')
        # create url
        destination = urllib.parse.quote('/analystmemo/add/', safe='/')
        # get response
        response = self.client.get('/analystmemo/add', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=301, target_status_code=200)

    def test_analystmemo_add_post_redirect(self):
        """ test add view """

        # login testuser
        self.client.login(username='testuser_analystmemo', password='M4d878CFQiHcJQrZr4iN')
        # get object
        system_id = System.objects.get(system_name = 'system_1').system_id
        # create post data
        data_dict = {
            'analystmemo_note': 'analystmemo_add_post_test',
            'system': system_id,
        }
        # get response
        response = self.client.post('/analystmemo/add/', data_dict)
        # create url
        destination = urllib.parse.quote('/system/' + str(system_id) + '/', safe='/')
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)

    def test_analystmemo_add_post_invalid_reload(self):
        """ test add view """

        # login testuser
        self.client.login(username='testuser_analystmemo', password='M4d878CFQiHcJQrZr4iN')
        # create post data
        data_dict = {}
        # get response
        response = self.client.post('/analystmemo/add/', data_dict)
        # compare
        self.assertEqual(response.status_code, 200)

    def test_analystmemo_add_post_invalid_template(self):
        """ test add view """

        # login testuser
        self.client.login(username='testuser_analystmemo', password='M4d878CFQiHcJQrZr4iN')
        # create post data
        data_dict = {}
        # get response
        response = self.client.post('/analystmemo/add/', data_dict)
        # compare
        self.assertTemplateUsed(response, 'dfirtrack_main/analystmemo/analystmemo_add.html')

    def test_analystmemo_edit_not_logged_in(self):
        """ test edit view """

        # get object
        analystmemo_1 = Analystmemo.objects.get(analystmemo_note='lorem ipsum')
        # create url
        destination = '/login/?next=' + urllib.parse.quote('/analystmemo/' + str(analystmemo_1.analystmemo_id) + '/edit/', safe='')
        # get response
        response = self.client.get('/analystmemo/' + str(analystmemo_1.analystmemo_id) + '/edit/', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)

    def test_analystmemo_edit_logged_in(self):
        """ test edit view """

        # get object
        analystmemo_1 = Analystmemo.objects.get(analystmemo_note='lorem ipsum')
        # login testuser
        self.client.login(username='testuser_analystmemo', password='M4d878CFQiHcJQrZr4iN')
        # get response
        response = self.client.get('/analystmemo/' + str(analystmemo_1.analystmemo_id) + '/edit/')
        # compare
        self.assertEqual(response.status_code, 200)

    def test_analystmemo_edit_template(self):
        """ test edit view """

        # get object
        analystmemo_1 = Analystmemo.objects.get(analystmemo_note='lorem ipsum')
        # login testuser
        self.client.login(username='testuser_analystmemo', password='M4d878CFQiHcJQrZr4iN')
        # get response
        response = self.client.get('/analystmemo/' + str(analystmemo_1.analystmemo_id) + '/edit/')
        # compare
        self.assertTemplateUsed(response, 'dfirtrack_main/analystmemo/analystmemo_edit.html')

    def test_analystmemo_edit_get_user_context(self):
        """ test edit view """

        # get object
        analystmemo_1 = Analystmemo.objects.get(analystmemo_note='lorem ipsum')
        # login testuser
        self.client.login(username='testuser_analystmemo', password='M4d878CFQiHcJQrZr4iN')
        # get response
        response = self.client.get('/analystmemo/' + str(analystmemo_1.analystmemo_id) + '/edit/')
        # compare
        self.assertEqual(str(response.context['user']), 'testuser_analystmemo')

    def test_analystmemo_edit_redirect(self):
        """ test edit view """

        # get object
        analystmemo_1 = Analystmemo.objects.get(analystmemo_note='lorem ipsum')
        # login testuser
        self.client.login(username='testuser_analystmemo', password='M4d878CFQiHcJQrZr4iN')
        # create url
        destination = urllib.parse.quote('/analystmemo/' + str(analystmemo_1.analystmemo_id) + '/edit/', safe='/')
        # get response
        response = self.client.get('/analystmemo/' + str(analystmemo_1.analystmemo_id) + '/edit', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=301, target_status_code=200)

    def test_analystmemo_edit_post_redirect(self):
        """ test edit view """

        # login testuser
        self.client.login(username='testuser_analystmemo', password='M4d878CFQiHcJQrZr4iN')
        # get user
        test_user = User.objects.get(username='testuser_analystmemo')
        # get object
        system_1 = System.objects.get(system_name = 'system_1')
        # create object
        analystmemo_1 = Analystmemo.objects.create(
            analystmemo_note = 'analystmemo_edit_post_test_1',
            system = system_1,
            analystmemo_created_by_user_id = test_user,
            analystmemo_modified_by_user_id = test_user,
        )
        # create post data
        data_dict = {
            'analystmemo_note': 'analystmemo_edit_post_test_2',
            'system': system_1.system_id,
        }
        # get response
        response = self.client.post('/analystmemo/' + str(analystmemo_1.analystmemo_id) + '/edit/', data_dict)
        # create url
        destination = urllib.parse.quote('/system/' + str(system_1.system_id) + '/', safe='/')
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)

    def test_analystmemo_edit_post_invalid_reload(self):
        """ test edit view """

        # login testuser
        self.client.login(username='testuser_analystmemo', password='M4d878CFQiHcJQrZr4iN')
        # get object
        analystmemo_id = Analystmemo.objects.get(analystmemo_note='lorem ipsum').analystmemo_id
        # create post data
        data_dict = {}
        # get response
        response = self.client.post('/analystmemo/' + str(analystmemo_id) + '/edit/', data_dict)
        # compare
        self.assertEqual(response.status_code, 200)

    def test_analystmemo_edit_post_invalid_template(self):
        """ test edit view """

        # login testuser
        self.client.login(username='testuser_analystmemo', password='M4d878CFQiHcJQrZr4iN')
        # get object
        analystmemo_id = Analystmemo.objects.get(analystmemo_note='lorem ipsum').analystmemo_id
        # create post data
        data_dict = {}
        # get response
        response = self.client.post('/analystmemo/' + str(analystmemo_id) + '/edit/', data_dict)
        # compare
        self.assertTemplateUsed(response, 'dfirtrack_main/analystmemo/analystmemo_edit.html')
