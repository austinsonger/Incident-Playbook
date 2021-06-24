from django.contrib.auth.models import User
from django.test import TestCase
from dfirtrack_artifacts.models import Artifactpriority
import urllib.parse

class ArtifactpriorityViewTestCase(TestCase):
    """ artifactpriority view tests """

    @classmethod
    def setUpTestData(cls):

        # create object
        Artifactpriority.objects.create(artifactpriority_name='artifactpriority_1')
        # create user
        User.objects.create_user(username='testuser_artifactpriority', password='mkE62cflomdYPRAdyvcR')

    def test_artifactpriority_list_not_logged_in(self):
        """ test list view """

        # create url
        destination = '/login/?next=' + urllib.parse.quote('/artifacts/artifactpriority/', safe='')
        # get response
        response = self.client.get('/artifacts/artifactpriority/', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)

    def test_artifactpriority_list_logged_in(self):
        """ test list view """

        # login testuser
        self.client.login(username='testuser_artifactpriority', password='mkE62cflomdYPRAdyvcR')
        # get response
        response = self.client.get('/artifacts/artifactpriority/')
        # compare
        self.assertEqual(response.status_code, 200)

    def test_artifactpriority_list_template(self):
        """ test list view """

        # login testuser
        self.client.login(username='testuser_artifactpriority', password='mkE62cflomdYPRAdyvcR')
        # get response
        response = self.client.get('/artifacts/artifactpriority/')
        # compare
        self.assertTemplateUsed(response, 'dfirtrack_artifacts/artifactpriority/artifactpriority_list.html')

    def test_artifactpriority_list_get_user_context(self):
        """ test list view """

        # login testuser
        self.client.login(username='testuser_artifactpriority', password='mkE62cflomdYPRAdyvcR')
        # get response
        response = self.client.get('/artifacts/artifactpriority/')
        # compare
        self.assertEqual(str(response.context['user']), 'testuser_artifactpriority')

    def test_artifactpriority_list_redirect(self):
        """ test list view """

        # login testuser
        self.client.login(username='testuser_artifactpriority', password='mkE62cflomdYPRAdyvcR')
        # create url
        destination = urllib.parse.quote('/artifacts/artifactpriority/', safe='/')
        # get response
        response = self.client.get('/artifacts/artifactpriority', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=301, target_status_code=200)

    def test_artifactpriority_detail_not_logged_in(self):
        """ test detail view """

        # get object
        artifactpriority_1 = Artifactpriority.objects.get(artifactpriority_name='artifactpriority_1')
        # create url
        destination = '/login/?next=' + urllib.parse.quote('/artifacts/artifactpriority/detail/' + str(artifactpriority_1.artifactpriority_id) + '/', safe='')
        # get response
        response = self.client.get('/artifacts/artifactpriority/detail/' + str(artifactpriority_1.artifactpriority_id) + '/', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)

    def test_artifactpriority_detail_logged_in(self):
        """ test detail view """

        # get object
        artifactpriority_1 = Artifactpriority.objects.get(artifactpriority_name='artifactpriority_1')
        # login testuser
        self.client.login(username='testuser_artifactpriority', password='mkE62cflomdYPRAdyvcR')
        # get response
        response = self.client.get('/artifacts/artifactpriority/detail/' + str(artifactpriority_1.artifactpriority_id) + '/')
        # compare
        self.assertEqual(response.status_code, 200)

    def test_artifactpriority_detail_template(self):
        """ test detail view """

        # get object
        artifactpriority_1 = Artifactpriority.objects.get(artifactpriority_name='artifactpriority_1')
        # login testuser
        self.client.login(username='testuser_artifactpriority', password='mkE62cflomdYPRAdyvcR')
        # get response
        response = self.client.get('/artifacts/artifactpriority/detail/' + str(artifactpriority_1.artifactpriority_id) + '/')
        # compare
        self.assertTemplateUsed(response, 'dfirtrack_artifacts/artifactpriority/artifactpriority_detail.html')

    def test_artifactpriority_detail_get_user_context(self):
        """ test detail view """

        # get object
        artifactpriority_1 = Artifactpriority.objects.get(artifactpriority_name='artifactpriority_1')
        # login testuser
        self.client.login(username='testuser_artifactpriority', password='mkE62cflomdYPRAdyvcR')
        # get response
        response = self.client.get('/artifacts/artifactpriority/detail/' + str(artifactpriority_1.artifactpriority_id) + '/')
        # compare
        self.assertEqual(str(response.context['user']), 'testuser_artifactpriority')

    def test_artifactpriority_detail_redirect(self):
        """ test list view """

        # get object
        artifactpriority_1 = Artifactpriority.objects.get(artifactpriority_name='artifactpriority_1')
        # login testuser
        self.client.login(username='testuser_artifactpriority', password='mkE62cflomdYPRAdyvcR')
        # create url
        destination = urllib.parse.quote('/artifacts/artifactpriority/detail/' + str(artifactpriority_1.artifactpriority_id) + '/', safe='/')
        # get response
        response = self.client.get('/artifacts/artifactpriority/detail/' + str(artifactpriority_1.artifactpriority_id), follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=301, target_status_code=200)
