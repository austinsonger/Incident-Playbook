from django.contrib.auth.models import User
from django.test import TestCase
from dfirtrack_main.models import Company
import urllib.parse

class CompanyViewTestCase(TestCase):
    """ company view tests """

    @classmethod
    def setUpTestData(cls):

        # create object
        Company.objects.create(company_name='company_1')
        # create user
        User.objects.create_user(username='testuser_company', password='MbJfulGWGKeqceBtN9Mi')

    def test_company_list_not_logged_in(self):
        """ test list view """

        # create url
        destination = '/login/?next=' + urllib.parse.quote('/company/', safe='')
        # get response
        response = self.client.get('/company/', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)

    def test_company_list_logged_in(self):
        """ test list view """

        # login testuser
        self.client.login(username='testuser_company', password='MbJfulGWGKeqceBtN9Mi')
        # get response
        response = self.client.get('/company/')
        # compare
        self.assertEqual(response.status_code, 200)

    def test_company_list_template(self):
        """ test list view """

        # login testuser
        self.client.login(username='testuser_company', password='MbJfulGWGKeqceBtN9Mi')
        # get response
        response = self.client.get('/company/')
        # compare
        self.assertTemplateUsed(response, 'dfirtrack_main/company/company_list.html')

    def test_company_list_get_user_context(self):
        """ test list view """

        # login testuser
        self.client.login(username='testuser_company', password='MbJfulGWGKeqceBtN9Mi')
        # get response
        response = self.client.get('/company/')
        # compare
        self.assertEqual(str(response.context['user']), 'testuser_company')

    def test_company_list_redirect(self):
        """ test list view """

        # login testuser
        self.client.login(username='testuser_company', password='MbJfulGWGKeqceBtN9Mi')
        # create url
        destination = urllib.parse.quote('/company/', safe='/')
        # get response
        response = self.client.get('/company', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=301, target_status_code=200)

    def test_company_detail_not_logged_in(self):
        """ test detail view """

        # get object
        company_1 = Company.objects.get(company_name='company_1')
        # create url
        destination = '/login/?next=' + urllib.parse.quote('/company/' + str(company_1.company_id) + '/', safe='')
        # get response
        response = self.client.get('/company/' + str(company_1.company_id) + '/', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)

    def test_company_detail_logged_in(self):
        """ test detail view """

        # get object
        company_1 = Company.objects.get(company_name='company_1')
        # login testuser
        self.client.login(username='testuser_company', password='MbJfulGWGKeqceBtN9Mi')
        # get response
        response = self.client.get('/company/' + str(company_1.company_id) + '/')
        # compare
        self.assertEqual(response.status_code, 200)

    def test_company_detail_template(self):
        """ test detail view """

        # get object
        company_1 = Company.objects.get(company_name='company_1')
        # login testuser
        self.client.login(username='testuser_company', password='MbJfulGWGKeqceBtN9Mi')
        # get response
        response = self.client.get('/company/' + str(company_1.company_id) + '/')
        # compare
        self.assertTemplateUsed(response, 'dfirtrack_main/company/company_detail.html')

    def test_company_detail_get_user_context(self):
        """ test detail view """

        # get object
        company_1 = Company.objects.get(company_name='company_1')
        # login testuser
        self.client.login(username='testuser_company', password='MbJfulGWGKeqceBtN9Mi')
        # get response
        response = self.client.get('/company/' + str(company_1.company_id) + '/')
        # compare
        self.assertEqual(str(response.context['user']), 'testuser_company')

    def test_company_detail_redirect(self):
        """ test detail view """

        # get object
        company_1 = Company.objects.get(company_name='company_1')
        # login testuser
        self.client.login(username='testuser_company', password='MbJfulGWGKeqceBtN9Mi')
        # create url
        destination = urllib.parse.quote('/company/' + str(company_1.company_id) + '/', safe='/')
        # get response
        response = self.client.get('/company/' + str(company_1.company_id), follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=301, target_status_code=200)

    def test_company_add_not_logged_in(self):
        """ test add view """

        # create url
        destination = '/login/?next=' + urllib.parse.quote('/company/add/', safe='')
        # get response
        response = self.client.get('/company/add/', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)

    def test_company_add_logged_in(self):
        """ test add view """

        # login testuser
        self.client.login(username='testuser_company', password='MbJfulGWGKeqceBtN9Mi')
        # get response
        response = self.client.get('/company/add/')
        # compare
        self.assertEqual(response.status_code, 200)

    def test_company_add_template(self):
        """ test add view """

        # login testuser
        self.client.login(username='testuser_company', password='MbJfulGWGKeqceBtN9Mi')
        # get response
        response = self.client.get('/company/add/')
        # compare
        self.assertTemplateUsed(response, 'dfirtrack_main/company/company_add.html')

    def test_company_add_get_user_context(self):
        """ test add view """

        # login testuser
        self.client.login(username='testuser_company', password='MbJfulGWGKeqceBtN9Mi')
        # get response
        response = self.client.get('/company/add/')
        # compare
        self.assertEqual(str(response.context['user']), 'testuser_company')

    def test_company_add_redirect(self):
        """ test add view """

        # login testuser
        self.client.login(username='testuser_company', password='MbJfulGWGKeqceBtN9Mi')
        # create url
        destination = urllib.parse.quote('/company/add/', safe='/')
        # get response
        response = self.client.get('/company/add', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=301, target_status_code=200)

    def test_company_add_post_redirect(self):
        """ test add view """

        # login testuser
        self.client.login(username='testuser_company', password='MbJfulGWGKeqceBtN9Mi')
        # create post data
        data_dict = {
            'company_name': 'company_add_post_test',
        }
        # get response
        response = self.client.post('/company/add/', data_dict)
        # get object
        company_id = Company.objects.get(company_name = 'company_add_post_test').company_id
        # create url
        destination = urllib.parse.quote('/company/' + str(company_id) + '/', safe='/')
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)

    def test_company_add_post_invalid_reload(self):
        """ test add view """

        # login testuser
        self.client.login(username='testuser_company', password='MbJfulGWGKeqceBtN9Mi')
        # create post data
        data_dict = {}
        # get response
        response = self.client.post('/company/add/', data_dict)
        # compare
        self.assertEqual(response.status_code, 200)

    def test_company_add_post_invalid_template(self):
        """ test add view """

        # login testuser
        self.client.login(username='testuser_company', password='MbJfulGWGKeqceBtN9Mi')
        # create post data
        data_dict = {}
        # get response
        response = self.client.post('/company/add/', data_dict)
        # compare
        self.assertTemplateUsed(response, 'dfirtrack_main/company/company_add.html')

    def test_company_add_popup_not_logged_in(self):
        """ test add view """

        # create url
        destination = '/login/?next=' + urllib.parse.quote('/company/add_popup/', safe='')
        # get response
        response = self.client.get('/company/add_popup/', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)

    def test_company_add_popup_logged_in(self):
        """ test add view """

        # login testuser
        self.client.login(username='testuser_company', password='MbJfulGWGKeqceBtN9Mi')
        # get response
        response = self.client.get('/company/add_popup/')
        # compare
        self.assertEqual(response.status_code, 200)

    def test_company_add_popup_template(self):
        """ test add view """

        # login testuser
        self.client.login(username='testuser_company', password='MbJfulGWGKeqceBtN9Mi')
        # get response
        response = self.client.get('/company/add_popup/')
        # compare
        self.assertTemplateUsed(response, 'dfirtrack_main/company/company_add_popup.html')

    def test_company_add_popup_get_user_context(self):
        """ test add view """

        # login testuser
        self.client.login(username='testuser_company', password='MbJfulGWGKeqceBtN9Mi')
        # get response
        response = self.client.get('/company/add_popup/')
        # compare
        self.assertEqual(str(response.context['user']), 'testuser_company')

    def test_company_add_popup_redirect(self):
        """ test add view """

        # login testuser
        self.client.login(username='testuser_company', password='MbJfulGWGKeqceBtN9Mi')
        # create url
        destination = urllib.parse.quote('/company/add_popup/', safe='/')
        # get response
        response = self.client.get('/company/add_popup', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=301, target_status_code=200)

    def test_company_add_popup_post_redirect(self):
        """ test add view """

        # login testuser
        self.client.login(username='testuser_company', password='MbJfulGWGKeqceBtN9Mi')
        # create post data
        data_dict = {
            'company_name': 'company_add_popup_post_test',
        }
        # get response
        response = self.client.post('/company/add_popup/', data_dict)
        # compare
        self.assertEqual(response.status_code, 200)

    def test_company_add_popup_post_invalid_reload(self):
        """ test add view """

        # login testuser
        self.client.login(username='testuser_company', password='MbJfulGWGKeqceBtN9Mi')
        # create post data
        data_dict = {}
        # get response
        response = self.client.post('/company/add_popup/', data_dict)
        # compare
        self.assertEqual(response.status_code, 200)

    def test_company_add_popup_post_invalid_template(self):
        """ test add view """

        # login testuser
        self.client.login(username='testuser_company', password='MbJfulGWGKeqceBtN9Mi')
        # create post data
        data_dict = {}
        # get response
        response = self.client.post('/company/add_popup/', data_dict)
        # compare
        self.assertTemplateUsed(response, 'dfirtrack_main/company/company_add_popup.html')

    def test_company_edit_not_logged_in(self):
        """ test edit view """

        # get object
        company_1 = Company.objects.get(company_name='company_1')
        # create url
        destination = '/login/?next=' + urllib.parse.quote('/company/' + str(company_1.company_id) + '/edit/', safe='')
        # get response
        response = self.client.get('/company/' + str(company_1.company_id) + '/edit/', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)

    def test_company_edit_logged_in(self):
        """ test edit view """

        # get object
        company_1 = Company.objects.get(company_name='company_1')
        # login testuser
        self.client.login(username='testuser_company', password='MbJfulGWGKeqceBtN9Mi')
        # get response
        response = self.client.get('/company/' + str(company_1.company_id) + '/edit/')
        # compare
        self.assertEqual(response.status_code, 200)

    def test_company_edit_template(self):
        """ test edit view """

        # get object
        company_1 = Company.objects.get(company_name='company_1')
        # login testuser
        self.client.login(username='testuser_company', password='MbJfulGWGKeqceBtN9Mi')
        # get response
        response = self.client.get('/company/' + str(company_1.company_id) + '/edit/')
        # compare
        self.assertTemplateUsed(response, 'dfirtrack_main/company/company_edit.html')

    def test_company_edit_get_user_context(self):
        """ test edit view """

        # get object
        company_1 = Company.objects.get(company_name='company_1')
        # login testuser
        self.client.login(username='testuser_company', password='MbJfulGWGKeqceBtN9Mi')
        # get response
        response = self.client.get('/company/' + str(company_1.company_id) + '/edit/')
        # compare
        self.assertEqual(str(response.context['user']), 'testuser_company')

    def test_company_edit_redirect(self):
        """ test edit view """

        # get object
        company_1 = Company.objects.get(company_name='company_1')
        # login testuser
        self.client.login(username='testuser_company', password='MbJfulGWGKeqceBtN9Mi')
        # create url
        destination = urllib.parse.quote('/company/' + str(company_1.company_id) + '/edit/', safe='/')
        # get response
        response = self.client.get('/company/' + str(company_1.company_id) + '/edit', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=301, target_status_code=200)

    def test_company_edit_post_redirect(self):
        """ test edit view """

        # login testuser
        self.client.login(username='testuser_company', password='MbJfulGWGKeqceBtN9Mi')
        # create object
        company_1 = Company.objects.create(company_name='company_edit_post_test_1')
        # create post data
        data_dict = {
            'company_name': 'company_edit_post_test_2',
        }
        # get response
        response = self.client.post('/company/' + str(company_1.company_id) + '/edit/', data_dict)
        # get object
        company_2 = Company.objects.get(company_name='company_edit_post_test_2')
        # create url
        destination = urllib.parse.quote('/company/' + str(company_2.company_id) + '/', safe='/')
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)

    def test_company_edit_post_invalid_reload(self):
        """ test edit view """

        # login testuser
        self.client.login(username='testuser_company', password='MbJfulGWGKeqceBtN9Mi')
        # get object
        company_id = Company.objects.get(company_name='company_1').company_id
        # create post data
        data_dict = {}
        # get response
        response = self.client.post('/company/' + str(company_id) + '/edit/', data_dict)
        # compare
        self.assertEqual(response.status_code, 200)

    def test_company_edit_post_invalid_template(self):
        """ test edit view """

        # login testuser
        self.client.login(username='testuser_company', password='MbJfulGWGKeqceBtN9Mi')
        # get object
        company_id = Company.objects.get(company_name='company_1').company_id
        # create post data
        data_dict = {}
        # get response
        response = self.client.post('/company/' + str(company_id) + '/edit/', data_dict)
        # compare
        self.assertTemplateUsed(response, 'dfirtrack_main/company/company_edit.html')
