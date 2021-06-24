from django.contrib.auth.models import User
from django.test import TestCase
from dfirtrack_main.models import Serviceprovider
import urllib.parse

class ServiceproviderViewTestCase(TestCase):
    """ serviceprovider view tests """

    @classmethod
    def setUpTestData(cls):

        # create object
        Serviceprovider.objects.create(serviceprovider_name='serviceprovider_1')
        # create user
        User.objects.create_user(username='testuser_serviceprovider', password='KxVbBhKZcvh6IcQUGjr0')

    def test_serviceprovider_list_not_logged_in(self):
        """ test list view """

        # create url
        destination = '/login/?next=' + urllib.parse.quote('/serviceprovider/', safe='')
        # get response
        response = self.client.get('/serviceprovider/', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)

    def test_serviceprovider_list_logged_in(self):
        """ test list view """

        # login testuser
        self.client.login(username='testuser_serviceprovider', password='KxVbBhKZcvh6IcQUGjr0')
        # get response
        response = self.client.get('/serviceprovider/')
        # compare
        self.assertEqual(response.status_code, 200)

    def test_serviceprovider_list_template(self):
        """ test list view """

        # login testuser
        self.client.login(username='testuser_serviceprovider', password='KxVbBhKZcvh6IcQUGjr0')
        # get response
        response = self.client.get('/serviceprovider/')
        # compare
        self.assertTemplateUsed(response, 'dfirtrack_main/serviceprovider/serviceprovider_list.html')

    def test_serviceprovider_list_get_user_context(self):
        """ test list view """

        # login testuser
        self.client.login(username='testuser_serviceprovider', password='KxVbBhKZcvh6IcQUGjr0')
        # get response
        response = self.client.get('/serviceprovider/')
        # compare
        self.assertEqual(str(response.context['user']), 'testuser_serviceprovider')

    def test_serviceprovider_list_redirect(self):
        """ test list view """

        # login testuser
        self.client.login(username='testuser_serviceprovider', password='KxVbBhKZcvh6IcQUGjr0')
        # create url
        destination = urllib.parse.quote('/serviceprovider/', safe='/')
        # get response
        response = self.client.get('/serviceprovider', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=301, target_status_code=200)

    def test_serviceprovider_detail_not_logged_in(self):
        """ test detail view """

        # get object
        serviceprovider_1 = Serviceprovider.objects.get(serviceprovider_name='serviceprovider_1')
        # create url
        destination = '/login/?next=' + urllib.parse.quote('/serviceprovider/' + str(serviceprovider_1.serviceprovider_id) + '/', safe='')
        # get response
        response = self.client.get('/serviceprovider/' + str(serviceprovider_1.serviceprovider_id) + '/', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)

    def test_serviceprovider_detail_logged_in(self):
        """ test detail view """

        # get object
        serviceprovider_1 = Serviceprovider.objects.get(serviceprovider_name='serviceprovider_1')
        # login testuser
        self.client.login(username='testuser_serviceprovider', password='KxVbBhKZcvh6IcQUGjr0')
        # get response
        response = self.client.get('/serviceprovider/' + str(serviceprovider_1.serviceprovider_id) + '/')
        # compare
        self.assertEqual(response.status_code, 200)

    def test_serviceprovider_detail_template(self):
        """ test detail view """

        # get object
        serviceprovider_1 = Serviceprovider.objects.get(serviceprovider_name='serviceprovider_1')
        # login testuser
        self.client.login(username='testuser_serviceprovider', password='KxVbBhKZcvh6IcQUGjr0')
        # get response
        response = self.client.get('/serviceprovider/' + str(serviceprovider_1.serviceprovider_id) + '/')
        # compare
        self.assertTemplateUsed(response, 'dfirtrack_main/serviceprovider/serviceprovider_detail.html')

    def test_serviceprovider_detail_get_user_context(self):
        """ test detail view """

        # get object
        serviceprovider_1 = Serviceprovider.objects.get(serviceprovider_name='serviceprovider_1')
        # login testuser
        self.client.login(username='testuser_serviceprovider', password='KxVbBhKZcvh6IcQUGjr0')
        # get response
        response = self.client.get('/serviceprovider/' + str(serviceprovider_1.serviceprovider_id) + '/')
        # compare
        self.assertEqual(str(response.context['user']), 'testuser_serviceprovider')

    def test_serviceprovider_detail_redirect(self):
        """ test detail view """

        # get object
        serviceprovider_1 = Serviceprovider.objects.get(serviceprovider_name='serviceprovider_1')
        # login testuser
        self.client.login(username='testuser_serviceprovider', password='KxVbBhKZcvh6IcQUGjr0')
        # create url
        destination = urllib.parse.quote('/serviceprovider/' + str(serviceprovider_1.serviceprovider_id) + '/', safe='/')
        # get response
        response = self.client.get('/serviceprovider/' + str(serviceprovider_1.serviceprovider_id), follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=301, target_status_code=200)

    def test_serviceprovider_add_not_logged_in(self):
        """ test add view """

        # create url
        destination = '/login/?next=' + urllib.parse.quote('/serviceprovider/add/', safe='')
        # get response
        response = self.client.get('/serviceprovider/add/', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)

    def test_serviceprovider_add_logged_in(self):
        """ test add view """

        # login testuser
        self.client.login(username='testuser_serviceprovider', password='KxVbBhKZcvh6IcQUGjr0')
        # get response
        response = self.client.get('/serviceprovider/add/')
        # compare
        self.assertEqual(response.status_code, 200)

    def test_serviceprovider_add_template(self):
        """ test add view """

        # login testuser
        self.client.login(username='testuser_serviceprovider', password='KxVbBhKZcvh6IcQUGjr0')
        # get response
        response = self.client.get('/serviceprovider/add/')
        # compare
        self.assertTemplateUsed(response, 'dfirtrack_main/serviceprovider/serviceprovider_add.html')

    def test_serviceprovider_add_get_user_context(self):
        """ test add view """

        # login testuser
        self.client.login(username='testuser_serviceprovider', password='KxVbBhKZcvh6IcQUGjr0')
        # get response
        response = self.client.get('/serviceprovider/add/')
        # compare
        self.assertEqual(str(response.context['user']), 'testuser_serviceprovider')

    def test_serviceprovider_add_redirect(self):
        """ test add view """

        # login testuser
        self.client.login(username='testuser_serviceprovider', password='KxVbBhKZcvh6IcQUGjr0')
        # create url
        destination = urllib.parse.quote('/serviceprovider/add/', safe='/')
        # get response
        response = self.client.get('/serviceprovider/add', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=301, target_status_code=200)

    def test_serviceprovider_add_post_redirect(self):
        """ test add view """

        # login testuser
        self.client.login(username='testuser_serviceprovider', password='KxVbBhKZcvh6IcQUGjr0')
        # create post data
        data_dict = {
            'serviceprovider_name': 'serviceprovider_add_post_test',
        }
        # get response
        response = self.client.post('/serviceprovider/add/', data_dict)
        # get object
        serviceprovider_id = Serviceprovider.objects.get(serviceprovider_name = 'serviceprovider_add_post_test').serviceprovider_id
        # create url
        destination = urllib.parse.quote('/serviceprovider/' + str(serviceprovider_id) + '/', safe='/')
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)

    def test_serviceprovider_add_post_invalid_reload(self):
        """ test add view """

        # login testuser
        self.client.login(username='testuser_serviceprovider', password='KxVbBhKZcvh6IcQUGjr0')
        # create post data
        data_dict = {}
        # get response
        response = self.client.post('/serviceprovider/add/', data_dict)
        # compare
        self.assertEqual(response.status_code, 200)

    def test_serviceprovider_add_post_invalid_template(self):
        """ test add view """

        # login testuser
        self.client.login(username='testuser_serviceprovider', password='KxVbBhKZcvh6IcQUGjr0')
        # create post data
        data_dict = {}
        # get response
        response = self.client.post('/serviceprovider/add/', data_dict)
        # compare
        self.assertTemplateUsed(response, 'dfirtrack_main/serviceprovider/serviceprovider_add.html')

    def test_serviceprovider_add_popup_not_logged_in(self):
        """ test add view """

        # create url
        destination = '/login/?next=' + urllib.parse.quote('/serviceprovider/add_popup/', safe='')
        # get response
        response = self.client.get('/serviceprovider/add_popup/', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)

    def test_serviceprovider_add_popup_logged_in(self):
        """ test add view """

        # login testuser
        self.client.login(username='testuser_serviceprovider', password='KxVbBhKZcvh6IcQUGjr0')
        # get response
        response = self.client.get('/serviceprovider/add_popup/')
        # compare
        self.assertEqual(response.status_code, 200)

    def test_serviceprovider_add_popup_template(self):
        """ test add view """

        # login testuser
        self.client.login(username='testuser_serviceprovider', password='KxVbBhKZcvh6IcQUGjr0')
        # get response
        response = self.client.get('/serviceprovider/add_popup/')
        # compare
        self.assertTemplateUsed(response, 'dfirtrack_main/serviceprovider/serviceprovider_add_popup.html')

    def test_serviceprovider_add_popup_get_user_context(self):
        """ test add view """

        # login testuser
        self.client.login(username='testuser_serviceprovider', password='KxVbBhKZcvh6IcQUGjr0')
        # get response
        response = self.client.get('/serviceprovider/add_popup/')
        # compare
        self.assertEqual(str(response.context['user']), 'testuser_serviceprovider')

    def test_serviceprovider_add_popup_redirect(self):
        """ test add view """

        # login testuser
        self.client.login(username='testuser_serviceprovider', password='KxVbBhKZcvh6IcQUGjr0')
        # create url
        destination = urllib.parse.quote('/serviceprovider/add_popup/', safe='/')
        # get response
        response = self.client.get('/serviceprovider/add_popup', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=301, target_status_code=200)

    def test_serviceprovider_add_popup_post_redirect(self):
        """ test add view """

        # login testuser
        self.client.login(username='testuser_serviceprovider', password='KxVbBhKZcvh6IcQUGjr0')
        # create post data
        data_dict = {
            'serviceprovider_name': 'serviceprovider_add_popup_post_test',
        }
        # get response
        response = self.client.post('/serviceprovider/add_popup/', data_dict)
        # compare
        self.assertEqual(response.status_code, 200)

    def test_serviceprovider_add_popup_post_invalid_reload(self):
        """ test add view """

        # login testuser
        self.client.login(username='testuser_serviceprovider', password='KxVbBhKZcvh6IcQUGjr0')
        # create post data
        data_dict = {}
        # get response
        response = self.client.post('/serviceprovider/add_popup/', data_dict)
        # compare
        self.assertEqual(response.status_code, 200)

    def test_serviceprovider_add_popup_post_invalid_template(self):
        """ test add view """

        # login testuser
        self.client.login(username='testuser_serviceprovider', password='KxVbBhKZcvh6IcQUGjr0')
        # create post data
        data_dict = {}
        # get response
        response = self.client.post('/serviceprovider/add_popup/', data_dict)
        # compare
        self.assertTemplateUsed(response, 'dfirtrack_main/serviceprovider/serviceprovider_add_popup.html')

    def test_serviceprovider_edit_not_logged_in(self):
        """ test edit view """

        # get object
        serviceprovider_1 = Serviceprovider.objects.get(serviceprovider_name='serviceprovider_1')
        # create url
        destination = '/login/?next=' + urllib.parse.quote('/serviceprovider/' + str(serviceprovider_1.serviceprovider_id) + '/edit/', safe='')
        # get response
        response = self.client.get('/serviceprovider/' + str(serviceprovider_1.serviceprovider_id) + '/edit/', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)

    def test_serviceprovider_edit_logged_in(self):
        """ test edit view """

        # get object
        serviceprovider_1 = Serviceprovider.objects.get(serviceprovider_name='serviceprovider_1')
        # login testuser
        self.client.login(username='testuser_serviceprovider', password='KxVbBhKZcvh6IcQUGjr0')
        # get response
        response = self.client.get('/serviceprovider/' + str(serviceprovider_1.serviceprovider_id) + '/edit/')
        # compare
        self.assertEqual(response.status_code, 200)

    def test_serviceprovider_edit_template(self):
        """ test edit view """

        # get object
        serviceprovider_1 = Serviceprovider.objects.get(serviceprovider_name='serviceprovider_1')
        # login testuser
        self.client.login(username='testuser_serviceprovider', password='KxVbBhKZcvh6IcQUGjr0')
        # get response
        response = self.client.get('/serviceprovider/' + str(serviceprovider_1.serviceprovider_id) + '/edit/')
        # compare
        self.assertTemplateUsed(response, 'dfirtrack_main/serviceprovider/serviceprovider_edit.html')

    def test_serviceprovider_edit_get_user_context(self):
        """ test edit view """

        # get object
        serviceprovider_1 = Serviceprovider.objects.get(serviceprovider_name='serviceprovider_1')
        # login testuser
        self.client.login(username='testuser_serviceprovider', password='KxVbBhKZcvh6IcQUGjr0')
        # get response
        response = self.client.get('/serviceprovider/' + str(serviceprovider_1.serviceprovider_id) + '/edit/')
        # compare
        self.assertEqual(str(response.context['user']), 'testuser_serviceprovider')

    def test_serviceprovider_edit_redirect(self):
        """ test edit view """

        # get object
        serviceprovider_1 = Serviceprovider.objects.get(serviceprovider_name='serviceprovider_1')
        # login testuser
        self.client.login(username='testuser_serviceprovider', password='KxVbBhKZcvh6IcQUGjr0')
        # create url
        destination = urllib.parse.quote('/serviceprovider/' + str(serviceprovider_1.serviceprovider_id) + '/edit/', safe='/')
        # get response
        response = self.client.get('/serviceprovider/' + str(serviceprovider_1.serviceprovider_id) + '/edit', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=301, target_status_code=200)

    def test_serviceprovider_edit_post_redirect(self):
        """ test edit view """

        # login testuser
        self.client.login(username='testuser_serviceprovider', password='KxVbBhKZcvh6IcQUGjr0')
        # create object
        serviceprovider_1 = Serviceprovider.objects.create(serviceprovider_name='serviceprovider_edit_post_test_1')
        # create post data
        data_dict = {
            'serviceprovider_name': 'serviceprovider_edit_post_test_2',
        }
        # get response
        response = self.client.post('/serviceprovider/' + str(serviceprovider_1.serviceprovider_id) + '/edit/', data_dict)
        # get object
        serviceprovider_2 = Serviceprovider.objects.get(serviceprovider_name='serviceprovider_edit_post_test_2')
        # create url
        destination = urllib.parse.quote('/serviceprovider/' + str(serviceprovider_2.serviceprovider_id) + '/', safe='/')
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)

    def test_serviceprovider_edit_post_invalid_reload(self):
        """ test edit view """

        # login testuser
        self.client.login(username='testuser_serviceprovider', password='KxVbBhKZcvh6IcQUGjr0')
        # get object
        serviceprovider_id = Serviceprovider.objects.get(serviceprovider_name='serviceprovider_1').serviceprovider_id
        # create post data
        data_dict = {}
        # get response
        response = self.client.post('/serviceprovider/' + str(serviceprovider_id) + '/edit/', data_dict)
        # compare
        self.assertEqual(response.status_code, 200)

    def test_serviceprovider_edit_post_invalid_template(self):
        """ test edit view """

        # login testuser
        self.client.login(username='testuser_serviceprovider', password='KxVbBhKZcvh6IcQUGjr0')
        # get object
        serviceprovider_id = Serviceprovider.objects.get(serviceprovider_name='serviceprovider_1').serviceprovider_id
        # create post data
        data_dict = {}
        # get response
        response = self.client.post('/serviceprovider/' + str(serviceprovider_id) + '/edit/', data_dict)
        # compare
        self.assertTemplateUsed(response, 'dfirtrack_main/serviceprovider/serviceprovider_edit.html')
