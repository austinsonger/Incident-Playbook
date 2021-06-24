from django.contrib.auth.models import User
from django.test import TestCase
from dfirtrack_artifacts.models import Artifacttype
import urllib.parse

class ArtifacttypeAPIViewTestCase(TestCase):
    """ artifacttype API view tests """

    @classmethod
    def setUpTestData(cls):

        # create object
        Artifacttype.objects.create(artifacttype_name='artifacttype_api_1')
        # create user
        User.objects.create_user(username='testuser_artifacttype_api', password='bYicpcLzwAvz66D1FbhF')

    def test_artifacttype_list_api_unauthorized(self):
        """ unauthorized access is forbidden"""

        # get response
        response = self.client.get('/api/artifacttype/')
        # compare
        self.assertEqual(response.status_code, 401)

    def test_artifacttype_list_api_method_get(self):
        """ GET is allowed """

        # login testuser
        self.client.login(username='testuser_artifacttype_api', password='bYicpcLzwAvz66D1FbhF')
        # get response
        response = self.client.get('/api/artifacttype/')
        # compare
        self.assertEqual(response.status_code, 200)

    def test_artifacttype_list_api_method_post(self):
        """ POST is allowed """

        # login testuser
        self.client.login(username='testuser_artifacttype_api', password='bYicpcLzwAvz66D1FbhF')
        # create POST string
        poststring = {"artifacttype_name": "artifacttype_api_2"}
        # get response
        response = self.client.post('/api/artifacttype/', data=poststring)
        # compare
        self.assertEqual(response.status_code, 201)

    def test_artifacttype_list_api_redirect(self):
        """ test redirect with appending slash """

        # login testuser
        self.client.login(username='testuser_artifacttype_api', password='bYicpcLzwAvz66D1FbhF')
        # create url
        destination = urllib.parse.quote('/api/artifacttype/', safe='/')
        # get response
        response = self.client.get('/api/artifacttype', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=301, target_status_code=200)

    def test_artifacttype_detail_api_unauthorized (self):
        """ unauthorized access is forbidden"""

        # get object
        artifacttype_api_1 = Artifacttype.objects.get(artifacttype_name='artifacttype_api_1')
        # get response
        response = self.client.get('/api/artifacttype/' + str(artifacttype_api_1.artifacttype_id) + '/')
        # compare
        self.assertEqual(response.status_code, 401)

    def test_artifacttype_detail_api_method_get(self):
        """ GET is allowed """

        # get object
        artifacttype_api_1 = Artifacttype.objects.get(artifacttype_name='artifacttype_api_1')
        # login testuser
        self.client.login(username='testuser_artifacttype_api', password='bYicpcLzwAvz66D1FbhF')
        # get response
        response = self.client.get('/api/artifacttype/' + str(artifacttype_api_1.artifacttype_id) + '/')
        # compare
        self.assertEqual(response.status_code, 200)

    def test_artifacttype_detail_api_method_delete(self):
        """ DELETE is forbidden """

        # get object
        artifacttype_api_1 = Artifacttype.objects.get(artifacttype_name='artifacttype_api_1')
        # login testuser
        self.client.login(username='testuser_artifacttype_api', password='bYicpcLzwAvz66D1FbhF')
        # get response
        response = self.client.delete('/api/artifacttype/' + str(artifacttype_api_1.artifacttype_id) + '/')
        # compare
        self.assertEqual(response.status_code, 405)

    def test_artifacttype_detail_api_method_put(self):
        """ PUT is allowed """

        # get object
        artifacttype_api_1 = Artifacttype.objects.get(artifacttype_name='artifacttype_api_1')
        # login testuser
        self.client.login(username='testuser_artifacttype_api', password='bYicpcLzwAvz66D1FbhF')
        # create url
        destination = urllib.parse.quote('/api/artifacttype/' + str(artifacttype_api_1.artifacttype_id) + '/', safe='/')
        # create PUT string
        putstring = {"artifacttype_name": "new_artifacttype_api_1"}
        # get response
        response = self.client.put(destination, data=putstring, content_type='application/json')
        # compare
        self.assertEqual(response.status_code, 200)

    def test_artifacttype_detail_api_redirect(self):
        """ test redirect with appending slash """

        # get object
        artifacttype_api_1 = Artifacttype.objects.get(artifacttype_name='artifacttype_api_1')
        # login testuser
        self.client.login(username='testuser_artifacttype_api', password='bYicpcLzwAvz66D1FbhF')
        # create url
        destination = urllib.parse.quote('/api/artifacttype/' + str(artifacttype_api_1.artifacttype_id) + '/', safe='/')
        # get response
        response = self.client.get('/api/artifacttype/' + str(artifacttype_api_1.artifacttype_id), follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=301, target_status_code=200)
