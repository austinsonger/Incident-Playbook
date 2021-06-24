from django.contrib.auth.models import User
from django.test import TestCase
from dfirtrack_artifacts.models import Artifactstatus
import urllib.parse

class ArtifactstatusViewTestCase(TestCase):
    """ artifactstatus view tests """

    @classmethod
    def setUpTestData(cls):

        # create object
        Artifactstatus.objects.create(artifactstatus_name='artifactstatus_1')
        # create user
        User.objects.create_user(username='testuser_artifactstatus', password='mkE62cflomdYPRAdyvcR')

    def test_artifactstatus_list_not_logged_in(self):
        """ test list view """

        # create url
        destination = '/login/?next=' + urllib.parse.quote('/artifacts/artifactstatus/', safe='')
        # get response
        response = self.client.get('/artifacts/artifactstatus/', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)

    def test_artifactstatus_list_logged_in(self):
        """ test list view """

        # login testuser
        self.client.login(username='testuser_artifactstatus', password='mkE62cflomdYPRAdyvcR')
        # get response
        response = self.client.get('/artifacts/artifactstatus/')
        # compare
        self.assertEqual(response.status_code, 200)

    def test_artifactstatus_list_template(self):
        """ test list view """

        # login testuser
        self.client.login(username='testuser_artifactstatus', password='mkE62cflomdYPRAdyvcR')
        # get response
        response = self.client.get('/artifacts/artifactstatus/')
        # compare
        self.assertTemplateUsed(response, 'dfirtrack_artifacts/artifactstatus/artifactstatus_list.html')

    def test_artifactstatus_list_get_user_context(self):
        """ test list view """

        # login testuser
        self.client.login(username='testuser_artifactstatus', password='mkE62cflomdYPRAdyvcR')
        # get response
        response = self.client.get('/artifacts/artifactstatus/')
        # compare
        self.assertEqual(str(response.context['user']), 'testuser_artifactstatus')

    def test_artifactstatus_list_redirect(self):
        """ test list view """

        # login testuser
        self.client.login(username='testuser_artifactstatus', password='mkE62cflomdYPRAdyvcR')
        # create url
        destination = urllib.parse.quote('/artifacts/artifactstatus/', safe='/')
        # get response
        response = self.client.get('/artifacts/artifactstatus', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=301, target_status_code=200)

    def test_artifactstatus_detail_not_logged_in(self):
        """ test detail view """

        # get object
        artifactstatus_1 = Artifactstatus.objects.get(artifactstatus_name='artifactstatus_1')
        # create url
        destination = '/login/?next=' + urllib.parse.quote('/artifacts/artifactstatus/detail/' + str(artifactstatus_1.artifactstatus_id) + '/', safe='')
        # get response
        response = self.client.get('/artifacts/artifactstatus/detail/' + str(artifactstatus_1.artifactstatus_id) + '/', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)

    def test_artifactstatus_detail_logged_in(self):
        """ test detail view """

        # get object
        artifactstatus_1 = Artifactstatus.objects.get(artifactstatus_name='artifactstatus_1')
        # login testuser
        self.client.login(username='testuser_artifactstatus', password='mkE62cflomdYPRAdyvcR')
        # get response
        response = self.client.get('/artifacts/artifactstatus/detail/' + str(artifactstatus_1.artifactstatus_id) + '/')
        # compare
        self.assertEqual(response.status_code, 200)

    def test_artifactstatus_detail_template(self):
        """ test detail view """

        # get object
        artifactstatus_1 = Artifactstatus.objects.get(artifactstatus_name='artifactstatus_1')
        # login testuser
        self.client.login(username='testuser_artifactstatus', password='mkE62cflomdYPRAdyvcR')
        # get response
        response = self.client.get('/artifacts/artifactstatus/detail/' + str(artifactstatus_1.artifactstatus_id) + '/')
        # compare
        self.assertTemplateUsed(response, 'dfirtrack_artifacts/artifactstatus/artifactstatus_detail.html')

    def test_artifactstatus_detail_get_user_context(self):
        """ test detail view """

        # get object
        artifactstatus_1 = Artifactstatus.objects.get(artifactstatus_name='artifactstatus_1')
        # login testuser
        self.client.login(username='testuser_artifactstatus', password='mkE62cflomdYPRAdyvcR')
        # get response
        response = self.client.get('/artifacts/artifactstatus/detail/' + str(artifactstatus_1.artifactstatus_id) + '/')
        # compare
        self.assertEqual(str(response.context['user']), 'testuser_artifactstatus')

    def test_artifactstatus_detail_redirect(self):
        """ test list view """

        # get object
        artifactstatus_1 = Artifactstatus.objects.get(artifactstatus_name='artifactstatus_1')
        # login testuser
        self.client.login(username='testuser_artifactstatus', password='mkE62cflomdYPRAdyvcR')
        # create url
        destination = urllib.parse.quote('/artifacts/artifactstatus/detail/' + str(artifactstatus_1.artifactstatus_id) + '/', safe='/')
        # get response
        response = self.client.get('/artifacts/artifactstatus/detail/' + str(artifactstatus_1.artifactstatus_id), follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=301, target_status_code=200)
