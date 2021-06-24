from django.contrib.auth.models import User
from django.test import TestCase
from dfirtrack_main.models import Contact
import urllib.parse

class ContactViewTestCase(TestCase):
    """ contact view tests """

    @classmethod
    def setUpTestData(cls):

        # create object
        Contact.objects.create(contact_name='contact_1', contact_email='contact_1@example.org')
        # create user
        User.objects.create_user(username='testuser_contact', password='BeQNeJYsIpvJzFi0t5YW')

    def test_contact_list_not_logged_in(self):
        """ test list view """

        # create url
        destination = '/login/?next=' + urllib.parse.quote('/contact/', safe='')
        # get response
        response = self.client.get('/contact/', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)

    def test_contact_list_logged_in(self):
        """ test list view """

        # login testuser
        self.client.login(username='testuser_contact', password='BeQNeJYsIpvJzFi0t5YW')
        # get response
        response = self.client.get('/contact/')
        # compare
        self.assertEqual(response.status_code, 200)

    def test_contact_list_template(self):
        """ test list view """

        # login testuser
        self.client.login(username='testuser_contact', password='BeQNeJYsIpvJzFi0t5YW')
        # get response
        response = self.client.get('/contact/')
        # compare
        self.assertTemplateUsed(response, 'dfirtrack_main/contact/contact_list.html')

    def test_contact_list_get_user_context(self):
        """ test list view """

        # login testuser
        self.client.login(username='testuser_contact', password='BeQNeJYsIpvJzFi0t5YW')
        # get response
        response = self.client.get('/contact/')
        # compare
        self.assertEqual(str(response.context['user']), 'testuser_contact')

    def test_contact_list_redirect(self):
        """ test list view """

        # login testuser
        self.client.login(username='testuser_contact', password='BeQNeJYsIpvJzFi0t5YW')
        # create url
        destination = urllib.parse.quote('/contact/', safe='/')
        # get response
        response = self.client.get('/contact', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=301, target_status_code=200)

    def test_contact_detail_not_logged_in(self):
        """ test detail view """

        # get object
        contact_1 = Contact.objects.get(contact_name='contact_1')
        # create url
        destination = '/login/?next=' + urllib.parse.quote('/contact/' + str(contact_1.contact_id) + '/', safe='')
        # get response
        response = self.client.get('/contact/' + str(contact_1.contact_id) + '/', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)

    def test_contact_detail_logged_in(self):
        """ test detail view """

        # get object
        contact_1 = Contact.objects.get(contact_name='contact_1')
        # login testuser
        self.client.login(username='testuser_contact', password='BeQNeJYsIpvJzFi0t5YW')
        # get response
        response = self.client.get('/contact/' + str(contact_1.contact_id) + '/')
        # compare
        self.assertEqual(response.status_code, 200)

    def test_contact_detail_template(self):
        """ test detail view """

        # get object
        contact_1 = Contact.objects.get(contact_name='contact_1')
        # login testuser
        self.client.login(username='testuser_contact', password='BeQNeJYsIpvJzFi0t5YW')
        # get response
        response = self.client.get('/contact/' + str(contact_1.contact_id) + '/')
        # compare
        self.assertTemplateUsed(response, 'dfirtrack_main/contact/contact_detail.html')

    def test_contact_detail_get_user_context(self):
        """ test detail view """

        # get object
        contact_1 = Contact.objects.get(contact_name='contact_1')
        # login testuser
        self.client.login(username='testuser_contact', password='BeQNeJYsIpvJzFi0t5YW')
        # get response
        response = self.client.get('/contact/' + str(contact_1.contact_id) + '/')
        # compare
        self.assertEqual(str(response.context['user']), 'testuser_contact')

    def test_contact_detail_redirect(self):
        """ test detail view """

        # get object
        contact_1 = Contact.objects.get(contact_name='contact_1')
        # login testuser
        self.client.login(username='testuser_contact', password='BeQNeJYsIpvJzFi0t5YW')
        # create url
        destination = urllib.parse.quote('/contact/' + str(contact_1.contact_id) + '/', safe='/')
        # get response
        response = self.client.get('/contact/' + str(contact_1.contact_id), follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=301, target_status_code=200)

    def test_contact_add_not_logged_in(self):
        """ test add view """

        # create url
        destination = '/login/?next=' + urllib.parse.quote('/contact/add/', safe='')
        # get response
        response = self.client.get('/contact/add/', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)

    def test_contact_add_logged_in(self):
        """ test add view """

        # login testuser
        self.client.login(username='testuser_contact', password='BeQNeJYsIpvJzFi0t5YW')
        # get response
        response = self.client.get('/contact/add/')
        # compare
        self.assertEqual(response.status_code, 200)

    def test_contact_add_template(self):
        """ test add view """

        # login testuser
        self.client.login(username='testuser_contact', password='BeQNeJYsIpvJzFi0t5YW')
        # get response
        response = self.client.get('/contact/add/')
        # compare
        self.assertTemplateUsed(response, 'dfirtrack_main/contact/contact_add.html')

    def test_contact_add_get_user_context(self):
        """ test add view """

        # login testuser
        self.client.login(username='testuser_contact', password='BeQNeJYsIpvJzFi0t5YW')
        # get response
        response = self.client.get('/contact/add/')
        # compare
        self.assertEqual(str(response.context['user']), 'testuser_contact')

    def test_contact_add_redirect(self):
        """ test add view """

        # login testuser
        self.client.login(username='testuser_contact', password='BeQNeJYsIpvJzFi0t5YW')
        # create url
        destination = urllib.parse.quote('/contact/add/', safe='/')
        # get response
        response = self.client.get('/contact/add', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=301, target_status_code=200)

    def test_contact_add_post_redirect(self):
        """ test add view """

        # login testuser
        self.client.login(username='testuser_contact', password='BeQNeJYsIpvJzFi0t5YW')
        # create post data
        data_dict = {
            'contact_name': 'contact_add_post_test',
            'contact_email': 'john.doe@example.org',
        }
        # get response
        response = self.client.post('/contact/add/', data_dict)
        # get object
        contact_id = Contact.objects.get(contact_name = 'contact_add_post_test').contact_id
        # create url
        destination = urllib.parse.quote('/contact/' + str(contact_id) + '/', safe='/')
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)

    def test_contact_add_post_invalid_reload(self):
        """ test add view """

        # login testuser
        self.client.login(username='testuser_contact', password='BeQNeJYsIpvJzFi0t5YW')
        # create post data
        data_dict = {}
        # get response
        response = self.client.post('/contact/add/', data_dict)
        # compare
        self.assertEqual(response.status_code, 200)

    def test_contact_add_post_invalid_template(self):
        """ test add view """

        # login testuser
        self.client.login(username='testuser_contact', password='BeQNeJYsIpvJzFi0t5YW')
        # create post data
        data_dict = {}
        # get response
        response = self.client.post('/contact/add/', data_dict)
        # compare
        self.assertTemplateUsed(response, 'dfirtrack_main/contact/contact_add.html')

    def test_contact_add_popup_not_logged_in(self):
        """ test add view """

        # create url
        destination = '/login/?next=' + urllib.parse.quote('/contact/add_popup/', safe='')
        # get response
        response = self.client.get('/contact/add_popup/', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)

    def test_contact_add_popup_logged_in(self):
        """ test add view """

        # login testuser
        self.client.login(username='testuser_contact', password='BeQNeJYsIpvJzFi0t5YW')
        # get response
        response = self.client.get('/contact/add_popup/')
        # compare
        self.assertEqual(response.status_code, 200)

    def test_contact_add_popup_template(self):
        """ test add view """

        # login testuser
        self.client.login(username='testuser_contact', password='BeQNeJYsIpvJzFi0t5YW')
        # get response
        response = self.client.get('/contact/add_popup/')
        # compare
        self.assertTemplateUsed(response, 'dfirtrack_main/contact/contact_add_popup.html')

    def test_contact_add_popup_get_user_context(self):
        """ test add view """

        # login testuser
        self.client.login(username='testuser_contact', password='BeQNeJYsIpvJzFi0t5YW')
        # get response
        response = self.client.get('/contact/add_popup/')
        # compare
        self.assertEqual(str(response.context['user']), 'testuser_contact')

    def test_contact_add_popup_redirect(self):
        """ test add view """

        # login testuser
        self.client.login(username='testuser_contact', password='BeQNeJYsIpvJzFi0t5YW')
        # create url
        destination = urllib.parse.quote('/contact/add_popup/', safe='/')
        # get response
        response = self.client.get('/contact/add_popup', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=301, target_status_code=200)

    def test_contact_add_popup_post_redirect(self):
        """ test add view """

        # login testuser
        self.client.login(username='testuser_contact', password='BeQNeJYsIpvJzFi0t5YW')
        # create post data
        data_dict = {
            'contact_name': 'contact_add_popup_post_test',
            'contact_email': 'john.doe@example.org',
        }
        # get response
        response = self.client.post('/contact/add_popup/', data_dict)
        # compare
        self.assertEqual(response.status_code, 200)

    def test_contact_add_popup_post_invalid_reload(self):
        """ test add view """

        # login testuser
        self.client.login(username='testuser_contact', password='BeQNeJYsIpvJzFi0t5YW')
        # create post data
        data_dict = {}
        # get response
        response = self.client.post('/contact/add_popup/', data_dict)
        # compare
        self.assertEqual(response.status_code, 200)

    def test_contact_add_popup_post_invalid_template(self):
        """ test add view """

        # login testuser
        self.client.login(username='testuser_contact', password='BeQNeJYsIpvJzFi0t5YW')
        # create post data
        data_dict = {}
        # get response
        response = self.client.post('/contact/add_popup/', data_dict)
        # compare
        self.assertTemplateUsed(response, 'dfirtrack_main/contact/contact_add_popup.html')

    def test_contact_edit_not_logged_in(self):
        """ test edit view """

        # get object
        contact_1 = Contact.objects.get(contact_name='contact_1')
        # create url
        destination = '/login/?next=' + urllib.parse.quote('/contact/' + str(contact_1.contact_id) + '/edit/', safe='')
        # get response
        response = self.client.get('/contact/' + str(contact_1.contact_id) + '/edit/', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)

    def test_contact_edit_logged_in(self):
        """ test edit view """

        # get object
        contact_1 = Contact.objects.get(contact_name='contact_1')
        # login testuser
        self.client.login(username='testuser_contact', password='BeQNeJYsIpvJzFi0t5YW')
        # get response
        response = self.client.get('/contact/' + str(contact_1.contact_id) + '/edit/')
        # compare
        self.assertEqual(response.status_code, 200)

    def test_contact_edit_template(self):
        """ test edit view """

        # get object
        contact_1 = Contact.objects.get(contact_name='contact_1')
        # login testuser
        self.client.login(username='testuser_contact', password='BeQNeJYsIpvJzFi0t5YW')
        # get response
        response = self.client.get('/contact/' + str(contact_1.contact_id) + '/edit/')
        # compare
        self.assertTemplateUsed(response, 'dfirtrack_main/contact/contact_edit.html')

    def test_contact_edit_get_user_context(self):
        """ test edit view """

        # get object
        contact_1 = Contact.objects.get(contact_name='contact_1')
        # login testuser
        self.client.login(username='testuser_contact', password='BeQNeJYsIpvJzFi0t5YW')
        # get response
        response = self.client.get('/contact/' + str(contact_1.contact_id) + '/edit/')
        # compare
        self.assertEqual(str(response.context['user']), 'testuser_contact')

    def test_contact_edit_redirect(self):
        """ test edit view """

        # get object
        contact_1 = Contact.objects.get(contact_name='contact_1')
        # login testuser
        self.client.login(username='testuser_contact', password='BeQNeJYsIpvJzFi0t5YW')
        # create url
        destination = urllib.parse.quote('/contact/' + str(contact_1.contact_id) + '/edit/', safe='/')
        # get response
        response = self.client.get('/contact/' + str(contact_1.contact_id) + '/edit', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=301, target_status_code=200)

    def test_contact_edit_post_redirect(self):
        """ test edit view """

        # login testuser
        self.client.login(username='testuser_contact', password='BeQNeJYsIpvJzFi0t5YW')
        # create object
        contact_1 = Contact.objects.create(
            contact_name='contact_edit_post_test_1',
            contact_email='john.doe@example.org',
        )
        # create post data
        data_dict = {
            'contact_name': 'contact_edit_post_test_2',
            'contact_email': 'john.doe@example.org',
        }
        # get response
        response = self.client.post('/contact/' + str(contact_1.contact_id) + '/edit/', data_dict)
        # get object
        contact_2 = Contact.objects.get(contact_name='contact_edit_post_test_2')
        # create url
        destination = urllib.parse.quote('/contact/' + str(contact_2.contact_id) + '/', safe='/')
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)

    def test_contact_edit_post_invalid_reload(self):
        """ test edit view """

        # login testuser
        self.client.login(username='testuser_contact', password='BeQNeJYsIpvJzFi0t5YW')
        # get object
        contact_id = Contact.objects.get(contact_name='contact_1').contact_id
        # create post data
        data_dict = {}
        # get response
        response = self.client.post('/contact/' + str(contact_id) + '/edit/', data_dict)
        # compare
        self.assertEqual(response.status_code, 200)

    def test_contact_edit_post_invalid_template(self):
        """ test edit view """

        # login testuser
        self.client.login(username='testuser_contact', password='BeQNeJYsIpvJzFi0t5YW')
        # get object
        contact_id = Contact.objects.get(contact_name='contact_1').contact_id
        # create post data
        data_dict = {}
        # get response
        response = self.client.post('/contact/' + str(contact_id) + '/edit/', data_dict)
        # compare
        self.assertTemplateUsed(response, 'dfirtrack_main/contact/contact_edit.html')
