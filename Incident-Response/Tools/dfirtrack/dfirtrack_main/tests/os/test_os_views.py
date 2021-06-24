from django.contrib.auth.models import User
from django.test import TestCase
from dfirtrack_main.models import Os
import urllib.parse

class OsViewTestCase(TestCase):
    """ os view tests """

    @classmethod
    def setUpTestData(cls):

        # create object
        Os.objects.create(os_name='os_1')
        # create user
        User.objects.create_user(username='testuser_os', password='n7hIWBsrGsG0n4mSjbfw')

    def test_os_list_not_logged_in(self):
        """ test list view """

        # create url
        destination = '/login/?next=' + urllib.parse.quote('/os/', safe='')
        # get response
        response = self.client.get('/os/', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)

    def test_os_list_logged_in(self):
        """ test list view """

        # login testuser
        self.client.login(username='testuser_os', password='n7hIWBsrGsG0n4mSjbfw')
        # get response
        response = self.client.get('/os/')
        # compare
        self.assertEqual(response.status_code, 200)

    def test_os_list_template(self):
        """ test list view """

        # login testuser
        self.client.login(username='testuser_os', password='n7hIWBsrGsG0n4mSjbfw')
        # get response
        response = self.client.get('/os/')
        # compare
        self.assertTemplateUsed(response, 'dfirtrack_main/os/os_list.html')

    def test_os_list_get_user_context(self):
        """ test list view """

        # login testuser
        self.client.login(username='testuser_os', password='n7hIWBsrGsG0n4mSjbfw')
        # get response
        response = self.client.get('/os/')
        # compare
        self.assertEqual(str(response.context['user']), 'testuser_os')

    def test_os_list_redirect(self):
        """ test list view """

        # login testuser
        self.client.login(username='testuser_os', password='n7hIWBsrGsG0n4mSjbfw')
        # create url
        destination = urllib.parse.quote('/os/', safe='/')
        # get response
        response = self.client.get('/os', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=301, target_status_code=200)

    def test_os_detail_not_logged_in(self):
        """ test detail view """

        # get object
        os_1 = Os.objects.get(os_name='os_1')
        # create url
        destination = '/login/?next=' + urllib.parse.quote('/os/' + str(os_1.os_id) + '/', safe='')
        # get response
        response = self.client.get('/os/' + str(os_1.os_id) + '/', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)

    def test_os_detail_logged_in(self):
        """ test detail view """

        # get object
        os_1 = Os.objects.get(os_name='os_1')
        # login testuser
        self.client.login(username='testuser_os', password='n7hIWBsrGsG0n4mSjbfw')
        # get response
        response = self.client.get('/os/' + str(os_1.os_id) + '/')
        # compare
        self.assertEqual(response.status_code, 200)

    def test_os_detail_template(self):
        """ test detail view """

        # get object
        os_1 = Os.objects.get(os_name='os_1')
        # login testuser
        self.client.login(username='testuser_os', password='n7hIWBsrGsG0n4mSjbfw')
        # get response
        response = self.client.get('/os/' + str(os_1.os_id) + '/')
        # compare
        self.assertTemplateUsed(response, 'dfirtrack_main/os/os_detail.html')

    def test_os_detail_get_user_context(self):
        """ test detail view """

        # get object
        os_1 = Os.objects.get(os_name='os_1')
        # login testuser
        self.client.login(username='testuser_os', password='n7hIWBsrGsG0n4mSjbfw')
        # get response
        response = self.client.get('/os/' + str(os_1.os_id) + '/')
        # compare
        self.assertEqual(str(response.context['user']), 'testuser_os')

    def test_os_detail_redirect(self):
        """ test detail view """

        # get object
        os_1 = Os.objects.get(os_name='os_1')
        # login testuser
        self.client.login(username='testuser_os', password='n7hIWBsrGsG0n4mSjbfw')
        # create url
        destination = urllib.parse.quote('/os/' + str(os_1.os_id) + '/', safe='/')
        # get response
        response = self.client.get('/os/' + str(os_1.os_id), follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=301, target_status_code=200)

    def test_os_add_not_logged_in(self):
        """ test add view """

        # create url
        destination = '/login/?next=' + urllib.parse.quote('/os/add/', safe='')
        # get response
        response = self.client.get('/os/add/', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)

    def test_os_add_logged_in(self):
        """ test add view """

        # login testuser
        self.client.login(username='testuser_os', password='n7hIWBsrGsG0n4mSjbfw')
        # get response
        response = self.client.get('/os/add/')
        # compare
        self.assertEqual(response.status_code, 200)

    def test_os_add_template(self):
        """ test add view """

        # login testuser
        self.client.login(username='testuser_os', password='n7hIWBsrGsG0n4mSjbfw')
        # get response
        response = self.client.get('/os/add/')
        # compare
        self.assertTemplateUsed(response, 'dfirtrack_main/os/os_add.html')

    def test_os_add_get_user_context(self):
        """ test add view """

        # login testuser
        self.client.login(username='testuser_os', password='n7hIWBsrGsG0n4mSjbfw')
        # get response
        response = self.client.get('/os/add/')
        # compare
        self.assertEqual(str(response.context['user']), 'testuser_os')

    def test_os_add_redirect(self):
        """ test add view """

        # login testuser
        self.client.login(username='testuser_os', password='n7hIWBsrGsG0n4mSjbfw')
        # create url
        destination = urllib.parse.quote('/os/add/', safe='/')
        # get response
        response = self.client.get('/os/add', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=301, target_status_code=200)

    def test_os_add_post_redirect(self):
        """ test add view """

        # login testuser
        self.client.login(username='testuser_os', password='n7hIWBsrGsG0n4mSjbfw')
        # create post data
        data_dict = {
            'os_name': 'os_add_post_test',
        }
        # get response
        response = self.client.post('/os/add/', data_dict)
        # get object
        os_id = Os.objects.get(os_name = 'os_add_post_test').os_id
        # create url
        destination = urllib.parse.quote('/os/' + str(os_id) + '/', safe='/')
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)

    def test_os_add_post_invalid_reload(self):
        """ test add view """

        # login testuser
        self.client.login(username='testuser_os', password='n7hIWBsrGsG0n4mSjbfw')
        # create post data
        data_dict = {}
        # get response
        response = self.client.post('/os/add/', data_dict)
        # compare
        self.assertEqual(response.status_code, 200)
    def test_os_add_post_invalid_template(self):
        """ test add view """

        # login testuser
        self.client.login(username='testuser_os', password='n7hIWBsrGsG0n4mSjbfw')
        # create post data
        data_dict = {}
        # get response
        response = self.client.post('/os/add/', data_dict)
        # compare
        self.assertTemplateUsed(response, 'dfirtrack_main/os/os_add.html')

    def test_os_add_popup_not_logged_in(self):
        """ test add view """

        # create url
        destination = '/login/?next=' + urllib.parse.quote('/os/add_popup/', safe='')
        # get response
        response = self.client.get('/os/add_popup/', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)

    def test_os_add_popup_logged_in(self):
        """ test add view """

        # login testuser
        self.client.login(username='testuser_os', password='n7hIWBsrGsG0n4mSjbfw')
        # get response
        response = self.client.get('/os/add_popup/')
        # compare
        self.assertEqual(response.status_code, 200)

    def test_os_add_popup_template(self):
        """ test add view """

        # login testuser
        self.client.login(username='testuser_os', password='n7hIWBsrGsG0n4mSjbfw')
        # get response
        response = self.client.get('/os/add_popup/')
        # compare
        self.assertTemplateUsed(response, 'dfirtrack_main/os/os_add_popup.html')

    def test_os_add_popup_get_user_context(self):
        """ test add view """

        # login testuser
        self.client.login(username='testuser_os', password='n7hIWBsrGsG0n4mSjbfw')
        # get response
        response = self.client.get('/os/add_popup/')
        # compare
        self.assertEqual(str(response.context['user']), 'testuser_os')

    def test_os_add_popup_redirect(self):
        """ test add view """

        # login testuser
        self.client.login(username='testuser_os', password='n7hIWBsrGsG0n4mSjbfw')
        # create url
        destination = urllib.parse.quote('/os/add_popup/', safe='/')
        # get response
        response = self.client.get('/os/add_popup', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=301, target_status_code=200)

    def test_os_add_popup_post_redirect(self):
        """ test add view """

        # login testuser
        self.client.login(username='testuser_os', password='n7hIWBsrGsG0n4mSjbfw')
        # create post data
        data_dict = {
            'os_name': 'os_add_popup_post_test',
        }
        # get response
        response = self.client.post('/os/add_popup/', data_dict)
        # compare
        self.assertEqual(response.status_code, 200)

    def test_os_add_popup_post_invalid_reload(self):
        """ test add view """

        # login testuser
        self.client.login(username='testuser_os', password='n7hIWBsrGsG0n4mSjbfw')
        # create post data
        data_dict = {}
        # get response
        response = self.client.post('/os/add_popup/', data_dict)
        # compare
        self.assertEqual(response.status_code, 200)

    def test_os_add_popup_post_invalid_template(self):
        """ test add view """

        # login testuser
        self.client.login(username='testuser_os', password='n7hIWBsrGsG0n4mSjbfw')
        # create post data
        data_dict = {}
        # get response
        response = self.client.post('/os/add_popup/', data_dict)
        # compare
        self.assertTemplateUsed(response, 'dfirtrack_main/os/os_add_popup.html')

    def test_os_edit_not_logged_in(self):
        """ test edit view """

        # get object
        os_1 = Os.objects.get(os_name='os_1')
        # create url
        destination = '/login/?next=' + urllib.parse.quote('/os/' + str(os_1.os_id) + '/edit/', safe='')
        # get response
        response = self.client.get('/os/' + str(os_1.os_id) + '/edit/', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)

    def test_os_edit_logged_in(self):
        """ test edit view """

        # get object
        os_1 = Os.objects.get(os_name='os_1')
        # login testuser
        self.client.login(username='testuser_os', password='n7hIWBsrGsG0n4mSjbfw')
        # get response
        response = self.client.get('/os/' + str(os_1.os_id) + '/edit/')
        # compare
        self.assertEqual(response.status_code, 200)

    def test_os_edit_template(self):
        """ test edit view """

        # get object
        os_1 = Os.objects.get(os_name='os_1')
        # login testuser
        self.client.login(username='testuser_os', password='n7hIWBsrGsG0n4mSjbfw')
        # get response
        response = self.client.get('/os/' + str(os_1.os_id) + '/edit/')
        # compare
        self.assertTemplateUsed(response, 'dfirtrack_main/os/os_edit.html')

    def test_os_edit_get_user_context(self):
        """ test edit view """

        # get object
        os_1 = Os.objects.get(os_name='os_1')
        # login testuser
        self.client.login(username='testuser_os', password='n7hIWBsrGsG0n4mSjbfw')
        # get response
        response = self.client.get('/os/' + str(os_1.os_id) + '/edit/')
        # compare
        self.assertEqual(str(response.context['user']), 'testuser_os')

    def test_os_edit_redirect(self):
        """ test edit view """

        # get object
        os_1 = Os.objects.get(os_name='os_1')
        # login testuser
        self.client.login(username='testuser_os', password='n7hIWBsrGsG0n4mSjbfw')
        # create url
        destination = urllib.parse.quote('/os/' + str(os_1.os_id) + '/edit/', safe='/')
        # get response
        response = self.client.get('/os/' + str(os_1.os_id) + '/edit', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=301, target_status_code=200)

    def test_os_edit_post_redirect(self):
        """ test edit view """

        # login testuser
        self.client.login(username='testuser_os', password='n7hIWBsrGsG0n4mSjbfw')
        # create object
        os_1 = Os.objects.create(os_name='os_edit_post_test_1')
        # create post data
        data_dict = {
            'os_name': 'os_edit_post_test_2',
        }
        # get response
        response = self.client.post('/os/' + str(os_1.os_id) + '/edit/', data_dict)
        # get object
        os_2 = Os.objects.get(os_name='os_edit_post_test_2')
        # create url
        destination = urllib.parse.quote('/os/' + str(os_2.os_id) + '/', safe='/')
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)

    def test_os_edit_post_invalid_reload(self):
        """ test edit view """

        # login testuser
        self.client.login(username='testuser_os', password='n7hIWBsrGsG0n4mSjbfw')
        # get object
        os_id = Os.objects.get(os_name='os_1').os_id
        # create post data
        data_dict = {}
        # get response
        response = self.client.post('/os/' + str(os_id) + '/edit/', data_dict)
        # compare
        self.assertEqual(response.status_code, 200)

    def test_os_edit_post_invalid_template(self):
        """ test edit view """

        # login testuser
        self.client.login(username='testuser_os', password='n7hIWBsrGsG0n4mSjbfw')
        # get object
        os_id = Os.objects.get(os_name='os_1').os_id
        # create post data
        data_dict = {}
        # get response
        response = self.client.post('/os/' + str(os_id) + '/edit/', data_dict)
        # compare
        self.assertTemplateUsed(response, 'dfirtrack_main/os/os_edit.html')
