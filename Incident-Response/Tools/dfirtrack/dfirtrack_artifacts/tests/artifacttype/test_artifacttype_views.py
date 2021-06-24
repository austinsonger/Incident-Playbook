from django.contrib.auth.models import User
from django.test import TestCase
from dfirtrack_artifacts.models import Artifacttype
import urllib.parse

class ArtifacttypeViewTestCase(TestCase):
    """ artifacttype view tests """

    @classmethod
    def setUpTestData(cls):

        # create object
        Artifacttype.objects.create(artifacttype_name='artifacttype_1')
        # create user
        User.objects.create_user(username='testuser_artifacttype', password='5HxLPaA1wWbphTcd2C3S')

    def test_artifacttype_list_not_logged_in(self):
        """ test list view """

        # create url
        destination = '/login/?next=' + urllib.parse.quote('/artifacts/artifacttype/', safe='')
        # get response
        response = self.client.get('/artifacts/artifacttype/', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)

    def test_artifacttype_list_logged_in(self):
        """ test list view """

        # login testuser
        self.client.login(username='testuser_artifacttype', password='5HxLPaA1wWbphTcd2C3S')
        # get response
        response = self.client.get('/artifacts/artifacttype/')
        # compare
        self.assertEqual(response.status_code, 200)

    def test_artifacttype_list_template(self):
        """ test list view """

        # login testuser
        self.client.login(username='testuser_artifacttype', password='5HxLPaA1wWbphTcd2C3S')
        # get response
        response = self.client.get('/artifacts/artifacttype/')
        # compare
        self.assertTemplateUsed(response, 'dfirtrack_artifacts/artifacttype/artifacttype_list.html')

    def test_artifacttype_list_get_user_context(self):
        """ test list view """

        # login testuser
        self.client.login(username='testuser_artifacttype', password='5HxLPaA1wWbphTcd2C3S')
        # get response
        response = self.client.get('/artifacts/artifacttype/')
        # compare
        self.assertEqual(str(response.context['user']), 'testuser_artifacttype')

    def test_artifacttype_list_redirect(self):
        """ test list view """

        # login testuser
        self.client.login(username='testuser_artifacttype', password='5HxLPaA1wWbphTcd2C3S')
        # create url
        destination = urllib.parse.quote('/artifacts/artifacttype/', safe='/')
        # get response
        response = self.client.get('/artifacts/artifacttype', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=301, target_status_code=200)

    def test_artifacttype_detail_not_logged_in(self):
        """ test detail view """

        # get object
        artifacttype_1 = Artifacttype.objects.get(artifacttype_name='artifacttype_1')
        # create url
        destination = '/login/?next=' + urllib.parse.quote('/artifacts/artifacttype/detail/' + str(artifacttype_1.artifacttype_id) + '/', safe='')
        # get response
        response = self.client.get('/artifacts/artifacttype/detail/' + str(artifacttype_1.artifacttype_id) + '/', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)

    def test_artifacttype_detail_logged_in(self):
        """ test detail view """

        # get object
        artifacttype_1 = Artifacttype.objects.get(artifacttype_name='artifacttype_1')
        # login testuser
        self.client.login(username='testuser_artifacttype', password='5HxLPaA1wWbphTcd2C3S')
        # get response
        response = self.client.get('/artifacts/artifacttype/detail/' + str(artifacttype_1.artifacttype_id) + '/')
        # compare
        self.assertEqual(response.status_code, 200)

    def test_artifacttype_detail_template(self):
        """ test detail view """

        # get object
        artifacttype_1 = Artifacttype.objects.get(artifacttype_name='artifacttype_1')
        # login testuser
        self.client.login(username='testuser_artifacttype', password='5HxLPaA1wWbphTcd2C3S')
        # get response
        response = self.client.get('/artifacts/artifacttype/detail/' + str(artifacttype_1.artifacttype_id) + '/')
        # compare
        self.assertTemplateUsed(response, 'dfirtrack_artifacts/artifacttype/artifacttype_detail.html')

    def test_artifacttype_detail_get_user_context(self):
        """ test detail view """

        # get object
        artifacttype_1 = Artifacttype.objects.get(artifacttype_name='artifacttype_1')
        # login testuser
        self.client.login(username='testuser_artifacttype', password='5HxLPaA1wWbphTcd2C3S')
        # get response
        response = self.client.get('/artifacts/artifacttype/detail/' + str(artifacttype_1.artifacttype_id) + '/')
        # compare
        self.assertEqual(str(response.context['user']), 'testuser_artifacttype')

    def test_artifacttype_detail_redirect(self):
        """ test detail view """

        # get object
        artifacttype_1 = Artifacttype.objects.get(artifacttype_name='artifacttype_1')
        # login testuser
        self.client.login(username='testuser_artifacttype', password='5HxLPaA1wWbphTcd2C3S')
        # create url
        destination = urllib.parse.quote('/artifacts/artifacttype/detail/' + str(artifacttype_1.artifacttype_id) + '/', safe='/')
        # get response
        response = self.client.get('/artifacts/artifacttype/detail/' + str(artifacttype_1.artifacttype_id), follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=301, target_status_code=200)

    def test_artifacttype_create_not_logged_in(self):
        """ test create view """

        # create url
        destination = '/login/?next=' + urllib.parse.quote('/artifacts/artifacttype/create/', safe='')
        # get response
        response = self.client.get('/artifacts/artifacttype/create/', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)

    def test_artifacttype_create_logged_in(self):
        """ test create view """

        # login testuser
        self.client.login(username='testuser_artifacttype', password='5HxLPaA1wWbphTcd2C3S')
        # get response
        response = self.client.get('/artifacts/artifacttype/create/')
        # compare
        self.assertEqual(response.status_code, 200)

    def test_artifacttype_create_template(self):
        """ test create view """

        # login testuser
        self.client.login(username='testuser_artifacttype', password='5HxLPaA1wWbphTcd2C3S')
        # get response
        response = self.client.get('/artifacts/artifacttype/create/')
        # compare
        self.assertTemplateUsed(response, 'dfirtrack_artifacts/artifacttype/artifacttype_add.html')

    def test_artifacttype_create_get_user_context(self):
        """ test create view """

        # login testuser
        self.client.login(username='testuser_artifacttype', password='5HxLPaA1wWbphTcd2C3S')
        # get response
        response = self.client.get('/artifacts/artifacttype/create/')
        # compare
        self.assertEqual(str(response.context['user']), 'testuser_artifacttype')

    def test_artifacttype_create_redirect(self):
        """ test create view """

        # login testuser
        self.client.login(username='testuser_artifacttype', password='5HxLPaA1wWbphTcd2C3S')
        # create url
        destination = urllib.parse.quote('/artifacts/artifacttype/create/', safe='/')
        # get response
        response = self.client.get('/artifacts/artifacttype/create', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=301, target_status_code=200)

    def test_artifacttype_create_post_redirect(self):
        """ test create view """

        # login testuser
        self.client.login(username='testuser_artifacttype', password='5HxLPaA1wWbphTcd2C3S')
        # create post data
        data_dict = {
            'artifacttype_name': 'artifacttype_create_post_test',
        }
        # get response
        response = self.client.post('/artifacts/artifacttype/create/', data_dict)
        # get artifacttype
        artifacttype_id = Artifacttype.objects.get(artifacttype_name = 'artifacttype_create_post_test').artifacttype_id
        # create url
        destination = urllib.parse.quote('/artifacts/artifacttype/detail/' + str(artifacttype_id) + '/', safe='/')
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)

    def test_artifacttype_create_post_invalid_reload(self):
        """ test create view """

        # login testuser
        self.client.login(username='testuser_artifacttype', password='5HxLPaA1wWbphTcd2C3S')
        # create post data
        data_dict = {}
        # get response
        response = self.client.post('/artifacts/artifacttype/create/', data_dict)
        # compare
        self.assertEqual(response.status_code, 200)

    def test_artifacttype_create_post_invalid_template(self):
        """ test create view """

        # login testuser
        self.client.login(username='testuser_artifacttype', password='5HxLPaA1wWbphTcd2C3S')
        # create post data
        data_dict = {}
        # get response
        response = self.client.post('/artifacts/artifacttype/create/', data_dict)
        # compare
        self.assertTemplateUsed(response, 'dfirtrack_artifacts/artifacttype/artifacttype_add.html')

    def test_artifacttype_update_not_logged_in(self):
        """ test update view """

        # get object
        artifacttype_1 = Artifacttype.objects.get(artifacttype_name='artifacttype_1')
        # create url
        destination = '/login/?next=' + urllib.parse.quote('/artifacts/artifacttype/update/' + str(artifacttype_1.artifacttype_id) + '/', safe='')
        # get response
        response = self.client.get('/artifacts/artifacttype/update/' + str(artifacttype_1.artifacttype_id) + '/', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)

    def test_artifacttype_update_logged_in(self):
        """ test update view """

        # get object
        artifacttype_1 = Artifacttype.objects.get(artifacttype_name='artifacttype_1')
        # login testuser
        self.client.login(username='testuser_artifacttype', password='5HxLPaA1wWbphTcd2C3S')
        # get response
        response = self.client.get('/artifacts/artifacttype/update/' + str(artifacttype_1.artifacttype_id) + '/')
        # compare
        self.assertEqual(response.status_code, 200)

    def test_artifacttype_update_template(self):
        """ test update view """

        # get object
        artifacttype_1 = Artifacttype.objects.get(artifacttype_name='artifacttype_1')
        # login testuser
        self.client.login(username='testuser_artifacttype', password='5HxLPaA1wWbphTcd2C3S')
        # get response
        response = self.client.get('/artifacts/artifacttype/update/' + str(artifacttype_1.artifacttype_id) + '/')
        # compare
        self.assertTemplateUsed(response, 'dfirtrack_artifacts/artifacttype/artifacttype_edit.html')

    def test_artifacttype_update_get_user_context(self):
        """ test update view """

        # get object
        artifacttype_1 = Artifacttype.objects.get(artifacttype_name='artifacttype_1')
        # login testuser
        self.client.login(username='testuser_artifacttype', password='5HxLPaA1wWbphTcd2C3S')
        # get response
        response = self.client.get('/artifacts/artifacttype/update/' + str(artifacttype_1.artifacttype_id) + '/')
        # compare
        self.assertEqual(str(response.context['user']), 'testuser_artifacttype')

    def test_artifacttype_update_redirect(self):
        """ test update view """

        # get object
        artifacttype_1 = Artifacttype.objects.get(artifacttype_name='artifacttype_1')
        # login testuser
        self.client.login(username='testuser_artifacttype', password='5HxLPaA1wWbphTcd2C3S')
        # create url
        destination = urllib.parse.quote('/artifacts/artifacttype/update/' + str(artifacttype_1.artifacttype_id) + '/', safe='/')
        # get response
        response = self.client.get('/artifacts/artifacttype/update/' + str(artifacttype_1.artifacttype_id), follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=301, target_status_code=200)

    def test_artifacttype_update_post_redirect(self):
        """ test update view """

        # login testuser
        self.client.login(username='testuser_artifacttype', password='5HxLPaA1wWbphTcd2C3S')
        # create object
        artifacttype_id = Artifacttype.objects.create(artifacttype_name = 'artifacttype_update_post_test_1').artifacttype_id
        # create post data
        data_dict = {
            'artifacttype_name': 'artifacttype_update_post_test_2',
        }
        # get response
        response = self.client.post('/artifacts/artifacttype/update/' + str(artifacttype_id) + '/', data_dict)
        # create url
        destination = urllib.parse.quote('/artifacts/artifacttype/detail/' + str(artifacttype_id) + '/', safe='/')
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)

    def test_artifacttype_update_post_invalid_reload(self):
        """ test update view """

        # login testuser
        self.client.login(username='testuser_artifacttype', password='5HxLPaA1wWbphTcd2C3S')
        # get object
        artifacttype_id = Artifacttype.objects.get(artifacttype_name='artifacttype_1').artifacttype_id
        # create post data
        data_dict = {}
        # get response
        response = self.client.post('/artifacts/artifacttype/update/' + str(artifacttype_id) + '/', data_dict)
        # compare
        self.assertEqual(response.status_code, 200)

    def test_artifacttype_update_post_invalid_template(self):
        """ test update view """

        # login testuser
        self.client.login(username='testuser_artifacttype', password='5HxLPaA1wWbphTcd2C3S')
        # get object
        artifacttype_id = Artifacttype.objects.get(artifacttype_name='artifacttype_1').artifacttype_id
        # create post data
        data_dict = {}
        # get response
        response = self.client.post('/artifacts/artifacttype/update/' + str(artifacttype_id) + '/', data_dict)
        # compare
        self.assertTemplateUsed(response, 'dfirtrack_artifacts/artifacttype/artifacttype_edit.html')
