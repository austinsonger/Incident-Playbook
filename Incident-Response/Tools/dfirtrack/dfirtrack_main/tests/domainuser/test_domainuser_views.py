from django.contrib.auth.models import User
from django.test import TestCase
from dfirtrack_main.models import Domain, Domainuser
import urllib.parse

class DomainuserViewTestCase(TestCase):
    """ domainuser view tests """

    @classmethod
    def setUpTestData(cls):

        # create user
        User.objects.create_user(username='testuser_domainuser', password='8fcseQ9rXyG9vNaoECnq')

        # create object
        domain_1 = Domain.objects.create(
            domain_name='domain_1',
        )

        # create object
        Domainuser.objects.create(domainuser_name='domainuser_1', domain = domain_1)

    def test_domainuser_list_not_logged_in(self):
        """ test list view """

        # create url
        destination = '/login/?next=' + urllib.parse.quote('/domainuser/', safe='')
        # get response
        response = self.client.get('/domainuser/', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)

    def test_domainuser_list_logged_in(self):
        """ test list view """

        # login testuser
        self.client.login(username='testuser_domainuser', password='8fcseQ9rXyG9vNaoECnq')
        # get response
        response = self.client.get('/domainuser/')
        # compare
        self.assertEqual(response.status_code, 200)

    def test_domainuser_list_template(self):
        """ test list view """

        # login testuser
        self.client.login(username='testuser_domainuser', password='8fcseQ9rXyG9vNaoECnq')
        # get response
        response = self.client.get('/domainuser/')
        # compare
        self.assertTemplateUsed(response, 'dfirtrack_main/domainuser/domainuser_list.html')

    def test_domainuser_list_get_user_context(self):
        """ test list view """

        # login testuser
        self.client.login(username='testuser_domainuser', password='8fcseQ9rXyG9vNaoECnq')
        # get response
        response = self.client.get('/domainuser/')
        # compare
        self.assertEqual(str(response.context['user']), 'testuser_domainuser')

    def test_domainuser_list_redirect(self):
        """ test list view """

        # login testuser
        self.client.login(username='testuser_domainuser', password='8fcseQ9rXyG9vNaoECnq')
        # create url
        destination = urllib.parse.quote('/domainuser/', safe='/')
        # get response
        response = self.client.get('/domainuser', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=301, target_status_code=200)

    def test_domainuser_detail_not_logged_in(self):
        """ test detail view """

        # get object
        domainuser_1 = Domainuser.objects.get(domainuser_name='domainuser_1')
        # create url
        destination = '/login/?next=' + urllib.parse.quote('/domainuser/' + str(domainuser_1.domainuser_id) + '/', safe='')
        # get response
        response = self.client.get('/domainuser/' + str(domainuser_1.domainuser_id) + '/', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)

    def test_domainuser_detail_logged_in(self):
        """ test detail view """

        # get object
        domainuser_1 = Domainuser.objects.get(domainuser_name='domainuser_1')
        # login testuser
        self.client.login(username='testuser_domainuser', password='8fcseQ9rXyG9vNaoECnq')
        # get response
        response = self.client.get('/domainuser/' + str(domainuser_1.domainuser_id) + '/')
        # compare
        self.assertEqual(response.status_code, 200)

    def test_domainuser_detail_template(self):
        """ test detail view """

        # get object
        domainuser_1 = Domainuser.objects.get(domainuser_name='domainuser_1')
        # login testuser
        self.client.login(username='testuser_domainuser', password='8fcseQ9rXyG9vNaoECnq')
        # get response
        response = self.client.get('/domainuser/' + str(domainuser_1.domainuser_id) + '/')
        # compare
        self.assertTemplateUsed(response, 'dfirtrack_main/domainuser/domainuser_detail.html')

    def test_domainuser_detail_get_user_context(self):
        """ test detail view """

        # get object
        domainuser_1 = Domainuser.objects.get(domainuser_name='domainuser_1')
        # login testuser
        self.client.login(username='testuser_domainuser', password='8fcseQ9rXyG9vNaoECnq')
        # get response
        response = self.client.get('/domainuser/' + str(domainuser_1.domainuser_id) + '/')
        # compare
        self.assertEqual(str(response.context['user']), 'testuser_domainuser')

    def test_domainuser_detail_redirect(self):
        """ test detail view """

        # get object
        domainuser_1 = Domainuser.objects.get(domainuser_name='domainuser_1')
        # login testuser
        self.client.login(username='testuser_domainuser', password='8fcseQ9rXyG9vNaoECnq')
        # create url
        destination = urllib.parse.quote('/domainuser/' + str(domainuser_1.domainuser_id) + '/', safe='/')
        # get response
        response = self.client.get('/domainuser/' + str(domainuser_1.domainuser_id), follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=301, target_status_code=200)

    def test_domainuser_add_not_logged_in(self):
        """ test add view """

        # create url
        destination = '/login/?next=' + urllib.parse.quote('/domainuser/add/', safe='')
        # get response
        response = self.client.get('/domainuser/add/', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)

    def test_domainuser_add_logged_in(self):
        """ test add view """

        # login testuser
        self.client.login(username='testuser_domainuser', password='8fcseQ9rXyG9vNaoECnq')
        # get response
        response = self.client.get('/domainuser/add/')
        # compare
        self.assertEqual(response.status_code, 200)

    def test_domainuser_add_template(self):
        """ test add view """

        # login testuser
        self.client.login(username='testuser_domainuser', password='8fcseQ9rXyG9vNaoECnq')
        # get response
        response = self.client.get('/domainuser/add/')
        # compare
        self.assertTemplateUsed(response, 'dfirtrack_main/domainuser/domainuser_add.html')

    def test_domainuser_add_get_user_context(self):
        """ test add view """

        # login testuser
        self.client.login(username='testuser_domainuser', password='8fcseQ9rXyG9vNaoECnq')
        # get response
        response = self.client.get('/domainuser/add/')
        # compare
        self.assertEqual(str(response.context['user']), 'testuser_domainuser')

    def test_domainuser_add_redirect(self):
        """ test add view """

        # login testuser
        self.client.login(username='testuser_domainuser', password='8fcseQ9rXyG9vNaoECnq')
        # create url
        destination = urllib.parse.quote('/domainuser/add/', safe='/')
        # get response
        response = self.client.get('/domainuser/add', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=301, target_status_code=200)

    def test_domainuser_add_post_redirect(self):
        """ test add view """

        # login testuser
        self.client.login(username='testuser_domainuser', password='8fcseQ9rXyG9vNaoECnq')
        # get object
        domain_id = Domain.objects.get(domain_name = 'domain_1').domain_id
        # create post data
        data_dict = {
            'domainuser_name': 'domainuser_add_post_test',
            'domain': domain_id,
        }
        # get response
        response = self.client.post('/domainuser/add/', data_dict)
        # get object
        domainuser_id = Domainuser.objects.get(domainuser_name = 'domainuser_add_post_test').domainuser_id
        # create url
        destination = urllib.parse.quote('/domainuser/' + str(domainuser_id) + '/', safe='/')
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)

    def test_domainuser_add_post_invalid_reload(self):
        """ test add view """

        # login testuser
        self.client.login(username='testuser_domainuser', password='8fcseQ9rXyG9vNaoECnq')
        # create post data
        data_dict = {}
        # get response
        response = self.client.post('/domainuser/add/', data_dict)
        # compare
        self.assertEqual(response.status_code, 200)

    def test_domainuser_add_post_invalid_template(self):
        """ test add view """

        # login testuser
        self.client.login(username='testuser_domainuser', password='8fcseQ9rXyG9vNaoECnq')
        # create post data
        data_dict = {}
        # get response
        response = self.client.post('/domainuser/add/', data_dict)
        # compare
        self.assertTemplateUsed(response, 'dfirtrack_main/domainuser/domainuser_add.html')

    def test_domainuser_edit_not_logged_in(self):
        """ test edit view """

        # get object
        domainuser_1 = Domainuser.objects.get(domainuser_name='domainuser_1')
        # create url
        destination = '/login/?next=' + urllib.parse.quote('/domainuser/' + str(domainuser_1.domainuser_id) + '/edit/', safe='')
        # get response
        response = self.client.get('/domainuser/' + str(domainuser_1.domainuser_id) + '/edit/', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)

    def test_domainuser_edit_logged_in(self):
        """ test edit view """

        # get object
        domainuser_1 = Domainuser.objects.get(domainuser_name='domainuser_1')
        # login testuser
        self.client.login(username='testuser_domainuser', password='8fcseQ9rXyG9vNaoECnq')
        # get response
        response = self.client.get('/domainuser/' + str(domainuser_1.domainuser_id) + '/edit/')
        # compare
        self.assertEqual(response.status_code, 200)

    def test_domainuser_edit_template(self):
        """ test edit view """

        # get object
        domainuser_1 = Domainuser.objects.get(domainuser_name='domainuser_1')
        # login testuser
        self.client.login(username='testuser_domainuser', password='8fcseQ9rXyG9vNaoECnq')
        # get response
        response = self.client.get('/domainuser/' + str(domainuser_1.domainuser_id) + '/edit/')
        # compare
        self.assertTemplateUsed(response, 'dfirtrack_main/domainuser/domainuser_edit.html')

    def test_domainuser_edit_get_user_context(self):
        """ test edit view """

        # get object
        domainuser_1 = Domainuser.objects.get(domainuser_name='domainuser_1')
        # login testuser
        self.client.login(username='testuser_domainuser', password='8fcseQ9rXyG9vNaoECnq')
        # get response
        response = self.client.get('/domainuser/' + str(domainuser_1.domainuser_id) + '/edit/')
        # compare
        self.assertEqual(str(response.context['user']), 'testuser_domainuser')

    def test_domainuser_edit_redirect(self):
        """ test edit view """

        # get object
        domainuser_1 = Domainuser.objects.get(domainuser_name='domainuser_1')
        # login testuser
        self.client.login(username='testuser_domainuser', password='8fcseQ9rXyG9vNaoECnq')
        # create url
        destination = urllib.parse.quote('/domainuser/' + str(domainuser_1.domainuser_id) + '/edit/', safe='/')
        # get response
        response = self.client.get('/domainuser/' + str(domainuser_1.domainuser_id) + '/edit', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=301, target_status_code=200)

    def test_domainuser_edit_post_redirect(self):
        """ test edit view """

        # login testuser
        self.client.login(username='testuser_domainuser', password='8fcseQ9rXyG9vNaoECnq')
        # get object
        domain_1 = Domain.objects.get(domain_name = 'domain_1')
        # create object
        domainuser_1 = Domainuser.objects.create(
            domainuser_name = 'domainuser_edit_post_test_1',
            domain = domain_1,
        )
        # create post data
        data_dict = {
            'domainuser_name': 'domainuser_edit_post_test_2',
            'domain': domain_1.domain_id,
        }
        # get response
        response = self.client.post('/domainuser/' + str(domainuser_1.domainuser_id) + '/edit/', data_dict)
        # get object
        domainuser_2 = Domainuser.objects.get(domainuser_name='domainuser_edit_post_test_2')
        # create url
        destination = urllib.parse.quote('/domainuser/' + str(domainuser_2.domainuser_id) + '/', safe='/')
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)

    def test_domainuser_edit_post_invalid_reload(self):
        """ test edit view """

        # login testuser
        self.client.login(username='testuser_domainuser', password='8fcseQ9rXyG9vNaoECnq')
        # get object
        domainuser_id = Domainuser.objects.get(domainuser_name='domainuser_1').domainuser_id
        # create post data
        data_dict = {}
        # get response
        response = self.client.post('/domainuser/' + str(domainuser_id) + '/edit/', data_dict)
        # compare
        self.assertEqual(response.status_code, 200)

    def test_domainuser_edit_post_invalid_template(self):
        """ test edit view """

        # login testuser
        self.client.login(username='testuser_domainuser', password='8fcseQ9rXyG9vNaoECnq')
        # get object
        domainuser_id = Domainuser.objects.get(domainuser_name='domainuser_1').domainuser_id
        # create post data
        data_dict = {}
        # get response
        response = self.client.post('/domainuser/' + str(domainuser_id) + '/edit/', data_dict)
        # compare
        self.assertTemplateUsed(response, 'dfirtrack_main/domainuser/domainuser_edit.html')
