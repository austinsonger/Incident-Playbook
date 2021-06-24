from django.contrib.auth.models import User
from django.test import TestCase
from dfirtrack_main.models import Os, Osimportname
import urllib.parse

class OsimportnameViewTestCase(TestCase):
    """ osimportname view tests """

    @classmethod
    def setUpTestData(cls):

        # create object
        os_1 = Os.objects.create(os_name='os_1')
        # create object
        Osimportname.objects.create(osimportname_name='osimportname_1', osimportname_importer='osimportname_importer_1', os = os_1)
        # create user
        User.objects.create_user(username='testuser_osimportname', password='SU7QGdCzPMBJd3l9URoS')

    def test_osimportname_list_not_logged_in(self):
        """ test list view """

        # create url
        destination = '/login/?next=' + urllib.parse.quote('/osimportname/', safe='')
        # get response
        response = self.client.get('/osimportname/', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)

    def test_osimportname_list_logged_in(self):
        """ test list view """

        # login testuser
        self.client.login(username='testuser_osimportname', password='SU7QGdCzPMBJd3l9URoS')
        # get response
        response = self.client.get('/osimportname/')
        # compare
        self.assertEqual(response.status_code, 200)

    def test_osimportname_list_template(self):
        """ test list view """

        # login testuser
        self.client.login(username='testuser_osimportname', password='SU7QGdCzPMBJd3l9URoS')
        # get response
        response = self.client.get('/osimportname/')
        # compare
        self.assertTemplateUsed(response, 'dfirtrack_main/osimportname/osimportname_list.html')

    def test_osimportname_list_get_user_context(self):
        """ test list view """

        # login testuser
        self.client.login(username='testuser_osimportname', password='SU7QGdCzPMBJd3l9URoS')
        # get response
        response = self.client.get('/osimportname/')
        # compare
        self.assertEqual(str(response.context['user']), 'testuser_osimportname')

    def test_osimportname_list_redirect(self):
        """ test list view """

        # login testuser
        self.client.login(username='testuser_osimportname', password='SU7QGdCzPMBJd3l9URoS')
        # create url
        destination = urllib.parse.quote('/osimportname/', safe='/')
        # get response
        response = self.client.get('/osimportname', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=301, target_status_code=200)

    def test_osimportname_add_not_logged_in(self):
        """ test add view """

        # create url
        destination = '/login/?next=' + urllib.parse.quote('/osimportname/add/', safe='')
        # get response
        response = self.client.get('/osimportname/add/', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)

    def test_osimportname_add_logged_in(self):
        """ test add view """

        # login testuser
        self.client.login(username='testuser_osimportname', password='SU7QGdCzPMBJd3l9URoS')
        # get response
        response = self.client.get('/osimportname/add/')
        # compare
        self.assertEqual(response.status_code, 200)

    def test_osimportname_add_template(self):
        """ test add view """

        # login testuser
        self.client.login(username='testuser_osimportname', password='SU7QGdCzPMBJd3l9URoS')
        # get response
        response = self.client.get('/osimportname/add/')
        # compare
        self.assertTemplateUsed(response, 'dfirtrack_main/osimportname/osimportname_add.html')

    def test_osimportname_add_get_user_context(self):
        """ test add view """

        # login testuser
        self.client.login(username='testuser_osimportname', password='SU7QGdCzPMBJd3l9URoS')
        # get response
        response = self.client.get('/osimportname/add/')
        # compare
        self.assertEqual(str(response.context['user']), 'testuser_osimportname')

    def test_osimportname_add_redirect(self):
        """ test add view """

        # login testuser
        self.client.login(username='testuser_osimportname', password='SU7QGdCzPMBJd3l9URoS')
        # create url
        destination = urllib.parse.quote('/osimportname/add/', safe='/')
        # get response
        response = self.client.get('/osimportname/add', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=301, target_status_code=200)

    def test_osimportname_add_post_redirect(self):
        """ test add view """

        # login testuser
        self.client.login(username='testuser_osimportname', password='SU7QGdCzPMBJd3l9URoS')
        # get object
        os_id = Os.objects.get(os_name='os_1').os_id
        # create post data
        data_dict = {
            'osimportname_name': 'osimportname_add_post_test',
            'osimportname_importer': 'importer_1',
            'os': os_id,
        }
        # get response
        response = self.client.post('/osimportname/add/', data_dict)
        # create url
        destination = urllib.parse.quote('/osimportname/', safe='/')
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)

    def test_osimportname_add_post_invalid_reload(self):
        """ test add view """

        # login testuser
        self.client.login(username='testuser_osimportname', password='SU7QGdCzPMBJd3l9URoS')
        # create post data
        data_dict = {}
        # get response
        response = self.client.post('/osimportname/add/', data_dict)
        # compare
        self.assertEqual(response.status_code, 200)

    def test_osimportname_add_post_invalid_template(self):
        """ test add view """

        # login testuser
        self.client.login(username='testuser_osimportname', password='SU7QGdCzPMBJd3l9URoS')
        # create post data
        data_dict = {}
        # get response
        response = self.client.post('/osimportname/add/', data_dict)
        # compare
        self.assertTemplateUsed(response, 'dfirtrack_main/osimportname/osimportname_add.html')

    def test_osimportname_edit_not_logged_in(self):
        """ test edit view """

        # get object
        osimportname_1 = Osimportname.objects.get(osimportname_name='osimportname_1')
        # create url
        destination = '/login/?next=' + urllib.parse.quote('/osimportname/' + str(osimportname_1.osimportname_id) + '/edit/', safe='')
        # get response
        response = self.client.get('/osimportname/' + str(osimportname_1.osimportname_id) + '/edit/', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)

    def test_osimportname_edit_logged_in(self):
        """ test edit view """

        # get object
        osimportname_1 = Osimportname.objects.get(osimportname_name='osimportname_1')
        # login testuser
        self.client.login(username='testuser_osimportname', password='SU7QGdCzPMBJd3l9URoS')
        # get response
        response = self.client.get('/osimportname/' + str(osimportname_1.osimportname_id) + '/edit/')
        # compare
        self.assertEqual(response.status_code, 200)

    def test_osimportname_edit_template(self):
        """ test edit view """

        # get object
        osimportname_1 = Osimportname.objects.get(osimportname_name='osimportname_1')
        # login testuser
        self.client.login(username='testuser_osimportname', password='SU7QGdCzPMBJd3l9URoS')
        # get response
        response = self.client.get('/osimportname/' + str(osimportname_1.osimportname_id) + '/edit/')
        # compare
        self.assertTemplateUsed(response, 'dfirtrack_main/osimportname/osimportname_edit.html')

    def test_osimportname_edit_get_user_context(self):
        """ test edit view """

        # get object
        osimportname_1 = Osimportname.objects.get(osimportname_name='osimportname_1')
        # login testuser
        self.client.login(username='testuser_osimportname', password='SU7QGdCzPMBJd3l9URoS')
        # get response
        response = self.client.get('/osimportname/' + str(osimportname_1.osimportname_id) + '/edit/')
        # compare
        self.assertEqual(str(response.context['user']), 'testuser_osimportname')

    def test_osimportname_edit_redirect(self):
        """ test edit view """

        # get object
        osimportname_1 = Osimportname.objects.get(osimportname_name='osimportname_1')
        # login testuser
        self.client.login(username='testuser_osimportname', password='SU7QGdCzPMBJd3l9URoS')
        # create url
        destination = urllib.parse.quote('/osimportname/' + str(osimportname_1.osimportname_id) + '/edit/', safe='/')
        # get response
        response = self.client.get('/osimportname/' + str(osimportname_1.osimportname_id) + '/edit', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=301, target_status_code=200)

    def test_osimportname_edit_post_redirect(self):
        """ test edit view """

        # login testuser
        self.client.login(username='testuser_osimportname', password='SU7QGdCzPMBJd3l9URoS')
        # get object
        os_1 = Os.objects.get(os_name='os_1')
        # create object
        osimportname_1 = Osimportname.objects.create(
            osimportname_name = 'osimportname_edit_post_test_1',
            osimportname_importer = 'importer_1',
            os = os_1,
        )
        # create post data
        data_dict = {
            'osimportname_name': 'osimportname_edit_post_test_2',
            'osimportname_importer': 'importer_1',
            'os': os_1.os_id,
        }
        # get response
        response = self.client.post('/osimportname/' + str(osimportname_1.osimportname_id) + '/edit/', data_dict)
        # create url
        destination = urllib.parse.quote('/osimportname/', safe='/')
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)

    def test_osimportname_edit_post_invalid_reload(self):
        """ test edit view """

        # login testuser
        self.client.login(username='testuser_osimportname', password='SU7QGdCzPMBJd3l9URoS')
        # get object
        osimportname_id = Osimportname.objects.get(osimportname_name='osimportname_1').osimportname_id
        # create post data
        data_dict = {}
        # get response
        response = self.client.post('/osimportname/' + str(osimportname_id) + '/edit/', data_dict)
        # compare
        self.assertEqual(response.status_code, 200)

    def test_osimportname_edit_post_invalid_template(self):
        """ test edit view """

        # login testuser
        self.client.login(username='testuser_osimportname', password='SU7QGdCzPMBJd3l9URoS')
        # get object
        osimportname_id = Osimportname.objects.get(osimportname_name='osimportname_1').osimportname_id
        # create post data
        data_dict = {}
        # get response
        response = self.client.post('/osimportname/' + str(osimportname_id) + '/edit/', data_dict)
        # compare
        self.assertTemplateUsed(response, 'dfirtrack_main/osimportname/osimportname_edit.html')
