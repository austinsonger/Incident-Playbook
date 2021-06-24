from django.contrib.auth.models import User
from django.test import TestCase
from dfirtrack_artifacts.models import Artifactstatus
import urllib.parse

class ArtifactstatusAPIViewTestCase(TestCase):
    """ artifactstatus API view tests """

    @classmethod
    def setUpTestData(cls):

        # create object
        Artifactstatus.objects.create(artifactstatus_name='artifactstatus_api_1')
        # create user
        User.objects.create_user(username='testuser_artifactstatus_api', password='aCTVRIdJ4cyVSkYiJKrM')

    def test_artifactstatus_list_api_unauthorized(self):
        """ unauthorized access is forbidden"""

        # get response
        response = self.client.get('/api/artifactstatus/')
        # compare
        self.assertEqual(response.status_code, 401)

    def test_artifactstatus_list_api_method_get(self):
        """ GET is allowed """

        # login testuser
        self.client.login(username='testuser_artifactstatus_api', password='aCTVRIdJ4cyVSkYiJKrM')
        # get response
        response = self.client.get('/api/artifactstatus/')
        # compare
        self.assertEqual(response.status_code, 200)

    def test_artifactstatus_list_api_method_post(self):
        """ POST is forbidden """

        # login testuser
        self.client.login(username='testuser_artifactstatus_api', password='aCTVRIdJ4cyVSkYiJKrM')
        # create POST string
        poststring = {"artifactstatus_name": "artifactstatus_api_2"}
        # get response
        response = self.client.post('/api/artifactstatus/', data=poststring)
        # compare
        self.assertEqual(response.status_code, 405)

    def test_artifactstatus_list_api_redirect(self):
        """ test redirect with appending slash """

        # login testuser
        self.client.login(username='testuser_artifactstatus_api', password='aCTVRIdJ4cyVSkYiJKrM')
        # create url
        destination = urllib.parse.quote('/api/artifactstatus/', safe='/')
        # get response
        response = self.client.get('/api/artifactstatus', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=301, target_status_code=200)

    def test_artifactstatus_detail_api_unauthorized (self):
        """ unauthorized access is forbidden"""

        # get object
        artifactstatus_api_1 = Artifactstatus.objects.get(artifactstatus_name='artifactstatus_api_1')
        # get response
        response = self.client.get('/api/artifactstatus/' + str(artifactstatus_api_1.artifactstatus_id) + '/')
        # compare
        self.assertEqual(response.status_code, 401)

    def test_artifactstatus_detail_api_method_get(self):
        """ GET is allowed """

        # get object
        artifactstatus_api_1 = Artifactstatus.objects.get(artifactstatus_name='artifactstatus_api_1')
        # login testuser
        self.client.login(username='testuser_artifactstatus_api', password='aCTVRIdJ4cyVSkYiJKrM')
        # get response
        response = self.client.get('/api/artifactstatus/' + str(artifactstatus_api_1.artifactstatus_id) + '/')
        # compare
        self.assertEqual(response.status_code, 200)

    def test_artifactstatus_detail_api_method_delete(self):
        """ DELETE is forbidden """

        # get object
        artifactstatus_api_1 = Artifactstatus.objects.get(artifactstatus_name='artifactstatus_api_1')
        # login testuser
        self.client.login(username='testuser_artifactstatus_api', password='aCTVRIdJ4cyVSkYiJKrM')
        # get response
        response = self.client.delete('/api/artifactstatus/' + str(artifactstatus_api_1.artifactstatus_id) + '/')
        # compare
        self.assertEqual(response.status_code, 405)

    def test_artifactstatus_detail_api_method_put(self):
        """ PUT is forbidden """

        # get object
        artifactstatus_api_1 = Artifactstatus.objects.get(artifactstatus_name='artifactstatus_api_1')
        # login testuser
        self.client.login(username='testuser_artifactstatus_api', password='aCTVRIdJ4cyVSkYiJKrM')
        # create url
        destination = urllib.parse.quote('/api/artifactstatus/' + str(artifactstatus_api_1.artifactstatus_id) + '/', safe='/')
        # create PUT string
        putstring = {"artifactstatus_name": "new_artifactstatus_api_1"}
        # get response
        response = self.client.put(destination, data=putstring, content_type='application/json')
        # compare
        self.assertEqual(response.status_code, 405)

    def test_artifactstatus_detail_api_redirect(self):
        """ test redirect with appending slash """

        # get object
        artifactstatus_api_1 = Artifactstatus.objects.get(artifactstatus_name='artifactstatus_api_1')
        # login testuser
        self.client.login(username='testuser_artifactstatus_api', password='aCTVRIdJ4cyVSkYiJKrM')
        # create url
        destination = urllib.parse.quote('/api/artifactstatus/' + str(artifactstatus_api_1.artifactstatus_id) + '/', safe='/')
        # get response
        response = self.client.get('/api/artifactstatus/' + str(artifactstatus_api_1.artifactstatus_id), follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=301, target_status_code=200)
