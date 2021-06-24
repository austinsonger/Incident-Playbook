from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone
from dfirtrack_artifacts.models import Artifact, Artifactstatus, Artifacttype
from dfirtrack_main.models import Case, System, Systemstatus
import urllib.parse

class ArtifactAPIViewTestCase(TestCase):
    """ artifact API view tests """

    @classmethod
    def setUpTestData(cls):

        # create user
        test_user = User.objects.create_user(username='testuser_artifact_api', password='rQeyaRKd7Lt6D518TTzv')

        # create object
        Case.objects.create(
            case_name = 'case_1',
            case_is_incident = True,
            case_created_by_user_id = test_user,
        )

        # create object
        systemstatus_1 = Systemstatus.objects.create(systemstatus_name='systemstatus_1')

        # create object
        system_1 = System.objects.create(
            system_name = 'system_1',
            systemstatus = systemstatus_1,
            system_modify_time = timezone.now(),
            system_created_by_user_id = test_user,
            system_modified_by_user_id = test_user,
        )

        # create object
        artifactstatus_1 = Artifactstatus.objects.create(artifactstatus_name='artifactstatus_1')

        # create object
        artifacttype_1 = Artifacttype.objects.create(artifacttype_name='artifacttype_1')

        # create object
        Artifact.objects.create(
            artifact_name='artifact_api_1',
            artifactstatus = artifactstatus_1,
            artifacttype = artifacttype_1,
            system = system_1,
            artifact_created_by_user_id = test_user,
            artifact_modified_by_user_id = test_user,
        )

    def test_artifact_list_api_unauthorized(self):
        """ unauthorized access is forbidden"""

        # get response
        response = self.client.get('/api/artifact/')
        # compare
        self.assertEqual(response.status_code, 401)

    def test_artifact_list_api_method_get(self):
        """ GET is allowed """

        # login testuser
        self.client.login(username='testuser_artifact_api', password='rQeyaRKd7Lt6D518TTzv')
        # get response
        response = self.client.get('/api/artifact/')
        # compare
        self.assertEqual(response.status_code, 200)

    def test_artifact_list_api_method_post(self):
        """ POST is allowed """

        # login testuser
        self.client.login(username='testuser_artifact_api', password='rQeyaRKd7Lt6D518TTzv')
        # get user
        test_user_id = User.objects.get(username='testuser_artifact_api').id
        # get object
        artifactstatus_id = Artifactstatus.objects.get(artifactstatus_name='artifactstatus_1').artifactstatus_id
        # get object
        artifacttype_id = Artifacttype.objects.get(artifacttype_name='artifacttype_1').artifacttype_id
        # get object
        system_id = System.objects.get(system_name='system_1').system_id
        # create POST string
        poststring = {
            "artifact_name": "artifact_api_2",
            "artifactstatus": artifactstatus_id,
            "artifacttype": artifacttype_id,
            "system": system_id,
            "artifact_created_by_user_id": test_user_id,
            "artifact_modified_by_user_id": test_user_id,
        }
        # get response
        response = self.client.post('/api/artifact/', data=poststring, content_type='application/json')
        # compare
        self.assertEqual(response.status_code, 201)

    def test_artifact_list_api_method_post_all_id(self):
        """ POST is allowed """

        # login testuser
        self.client.login(username='testuser_artifact_api', password='rQeyaRKd7Lt6D518TTzv')
        # get user
        test_user_id = User.objects.get(username='testuser_artifact_api').id
        # get object
        artifactstatus_id = Artifactstatus.objects.get(artifactstatus_name='artifactstatus_1').artifactstatus_id
        # get object
        artifacttype_id = Artifacttype.objects.get(artifacttype_name='artifacttype_1').artifacttype_id
        # get object
        case_id = Case.objects.get(case_name='case_1').case_id
        # get object
        system_id = System.objects.get(system_name='system_1').system_id
        # create POST string
        poststring = {
            "artifact_name": "artifact_api_3",
            "artifactstatus": artifactstatus_id,
            "artifacttype": artifacttype_id,
            "case": case_id,
            "system": system_id,
            "artifact_md5": "d41d8cd98f00b204e9800998ecf8427e",
            "artifact_sha1": "da39a3ee5e6b4b0d3255bfef95601890afd80709",
            "artifact_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
            "artifact_source_path": "C:\Windows",
            "artifact_acquisition_time": timezone.now().strftime('%Y-%m-%dT%H:%M'),
            "artifact_requested_time": timezone.now().strftime('%Y-%m-%dT%H:%M'),
            "artifact_created_by_user_id": test_user_id,
            "artifact_modified_by_user_id": test_user_id,
        }
        # get response
        response = self.client.post('/api/artifact/', data=poststring, content_type='application/json')
        # compare
        self.assertEqual(response.status_code, 201)

    def test_artifact_list_api_redirect(self):
        """ test redirect with appending slash """

        # login testuser
        self.client.login(username='testuser_artifact_api', password='rQeyaRKd7Lt6D518TTzv')
        # create url
        destination = urllib.parse.quote('/api/artifact/', safe='/')
        # get response
        response = self.client.get('/api/artifact', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=301, target_status_code=200)

    def test_artifact_detail_api_unauthorized (self):
        """ unauthorized access is forbidden"""

        # get object
        artifact_api_1 = Artifact.objects.get(artifact_name='artifact_api_1')
        # get response
        response = self.client.get('/api/artifact/' + str(artifact_api_1.artifact_id) + '/')
        # compare
        self.assertEqual(response.status_code, 401)

    def test_artifact_detail_api_method_get(self):
        """ GET is allowed """

        # get object
        artifact_api_1 = Artifact.objects.get(artifact_name='artifact_api_1')
        # login testuser
        self.client.login(username='testuser_artifact_api', password='rQeyaRKd7Lt6D518TTzv')
        # get response
        response = self.client.get('/api/artifact/' + str(artifact_api_1.artifact_id) + '/')
        # compare
        self.assertEqual(response.status_code, 200)

    def test_artifact_detail_api_method_delete(self):
        """ DELETE is forbidden """

        # get object
        artifact_api_1 = Artifact.objects.get(artifact_name='artifact_api_1')
        # login testuser
        self.client.login(username='testuser_artifact_api', password='rQeyaRKd7Lt6D518TTzv')
        # get response
        response = self.client.delete('/api/artifact/' + str(artifact_api_1.artifact_id) + '/')
        # compare
        self.assertEqual(response.status_code, 405)

    def test_artifact_detail_api_method_put(self):
        """ PUT is allowed """

        # login testuser
        self.client.login(username='testuser_artifact_api', password='rQeyaRKd7Lt6D518TTzv')
        # get user
        test_user_id = User.objects.get(username='testuser_artifact_api').id
        # get object
        artifact_api_1 = Artifact.objects.get(artifact_name='artifact_api_1')
        # get object
        artifactstatus_id = Artifactstatus.objects.get(artifactstatus_name='artifactstatus_1').artifactstatus_id
        # get object
        artifacttype_id = Artifacttype.objects.get(artifacttype_name='artifacttype_1').artifacttype_id
        # get object
        system_id = System.objects.get(system_name='system_1').system_id
        # create url
        destination = urllib.parse.quote('/api/artifact/' + str(artifact_api_1.artifact_id) + '/', safe='/')
        # create PUT string
        putstring = {
            "artifact_name": "new_artifact_api_1",
            "artifactstatus": artifactstatus_id,
            "artifacttype": artifacttype_id,
            "system": system_id,
            "artifact_created_by_user_id": test_user_id,
            "artifact_modified_by_user_id": test_user_id,
        }
        # get response
        response = self.client.put(destination, data=putstring, content_type='application/json')
        # compare
        self.assertEqual(response.status_code, 200)

    def test_artifact_detail_api_method_put_all_id(self):
        """ PUT is allowed """

        # login testuser
        self.client.login(username='testuser_artifact_api', password='rQeyaRKd7Lt6D518TTzv')
        # get user
        test_user_id = User.objects.get(username='testuser_artifact_api').id
        # get object
        artifact_api_1 = Artifact.objects.get(artifact_name='artifact_api_1')
        # get object
        artifactstatus_id = Artifactstatus.objects.get(artifactstatus_name='artifactstatus_1').artifactstatus_id
        # get object
        artifacttype_id = Artifacttype.objects.get(artifacttype_name='artifacttype_1').artifacttype_id
        # get object
        case_id = Case.objects.get(case_name='case_1').case_id
        # get object
        system_id = System.objects.get(system_name='system_1').system_id
        # create url
        destination = urllib.parse.quote('/api/artifact/' + str(artifact_api_1.artifact_id) + '/', safe='/')
        # create PUT string
        putstring = {
            "artifact_name": "new_artifact_api_1",
            "artifactstatus": artifactstatus_id,
            "artifacttype": artifacttype_id,
            "case": case_id,
            "system": system_id,
            "artifact_md5": "d41d8cd98f00b204e9800998ecf8427e",
            "artifact_sha1": "da39a3ee5e6b4b0d3255bfef95601890afd80709",
            "artifact_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
            "artifact_source_path": "C:\Windows",
            "artifact_acquisition_time": timezone.now().strftime('%Y-%m-%dT%H:%M'),
            "artifact_requested_time": timezone.now().strftime('%Y-%m-%dT%H:%M'),
            "artifact_created_by_user_id": test_user_id,
            "artifact_modified_by_user_id": test_user_id,
        }
        # get response
        response = self.client.put(destination, data=putstring, content_type='application/json')
        # compare
        self.assertEqual(response.status_code, 200)

    def test_artifact_detail_api_redirect(self):
        """ test redirect with appending slash """

        # get object
        artifact_api_1 = Artifact.objects.get(artifact_name='artifact_api_1')
        # login testuser
        self.client.login(username='testuser_artifact_api', password='rQeyaRKd7Lt6D518TTzv')
        # create url
        destination = urllib.parse.quote('/api/artifact/' + str(artifact_api_1.artifact_id) + '/', safe='/')
        # get response
        response = self.client.get('/api/artifact/' + str(artifact_api_1.artifact_id), follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=301, target_status_code=200)
