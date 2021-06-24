from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone
from dfirtrack_artifacts.forms import ArtifactForm
from dfirtrack_artifacts.models import Artifactpriority, Artifactstatus, Artifacttype
from dfirtrack_main.models import Case, System, Systemstatus

class ArtifactFormTestCase(TestCase):
    """ artifact form tests """

    @classmethod
    def setUpTestData(cls):

        # create user
        test_user = User.objects.create_user(username='testuser_artifact', password='zpdfNMmo3vYrkHrrL6EU')

        # create object
        Artifactpriority.objects.create(artifactpriority_name='artifactpriority_1')

        # create object
        Artifactstatus.objects.create(artifactstatus_name='artifactstatus_1')

        # create object
        Artifacttype.objects.create(artifacttype_name='artifacttype_1')

        # create object
        Case.objects.create(
            case_name = 'case_1',
            case_is_incident = True,
            case_created_by_user_id = test_user,
        )

        # create object
        systemstatus_1 = Systemstatus.objects.create(systemstatus_name='systemstatus_1')

        # create object
        System.objects.create(
            system_name='system_1',
            systemstatus = systemstatus_1,
            system_modify_time = timezone.now(),
            system_created_by_user_id = test_user,
            system_modified_by_user_id = test_user,
        )

    def test_artifact_name_form_label(self):
        """ test form label """

        # get object
        form = ArtifactForm()
        # compare
        self.assertEqual(form.fields['artifact_name'].label, 'Artifact name (*)')

    def test_artifact_artifactpriority_form_label(self):
        """ test form label """

        # get object
        form = ArtifactForm()
        # compare
        self.assertEqual(form.fields['artifactpriority'].label, 'Artifactpriority (*)')

    def test_artifact_artifactstatus_form_label(self):
        """ test form label """

        # get object
        form = ArtifactForm()
        # compare
        self.assertEqual(form.fields['artifactstatus'].label, 'Artifactstatus (*)')

    def test_artifact_artifacttype_form_label(self):
        """ test form label """

        # get object
        form = ArtifactForm()
        # compare
        self.assertEqual(form.fields['artifacttype'].label, 'Artifacttype (*)')

    def test_artifact_source_path_form_label(self):
        """ test form label """

        # get object
        form = ArtifactForm()
        # compare
        self.assertEqual(form.fields['artifact_source_path'].label, 'Artifact source path')

    def test_artifact_system_form_label(self):
        """ test form label """

        # get object
        form = ArtifactForm()
        # compare
        self.assertEqual(form.fields['system'].label, 'System (*)')

    def test_artifact_case_form_label(self):
        """ test form label """

        # get object
        form = ArtifactForm()
        # compare
        self.assertEqual(form.fields['case'].label, 'Case')

    def test_artifact_md5_form_label(self):
        """ test form label """

        # get object
        form = ArtifactForm()
        # compare
        self.assertEqual(form.fields['artifact_md5'].label, 'MD5')

    def test_artifact_sha1_form_label(self):
        """ test form label """

        # get object
        form = ArtifactForm()
        # compare
        self.assertEqual(form.fields['artifact_sha1'].label, 'SHA1')

    def test_artifact_sha256_form_label(self):
        """ test form label """

        # get object
        form = ArtifactForm()
        # compare
        self.assertEqual(form.fields['artifact_sha256'].label, 'SHA256')

    def test_artifact_note_analysisresult_form_label(self):
        """ test form label """

        # get object
        form = ArtifactForm()
        # compare
        self.assertEqual(form.fields['artifact_note_analysisresult'].label, 'Analysis result')

    def test_artifact_note_external_form_label(self):
        """ test form label """

        # get object
        form = ArtifactForm()
        # compare
        self.assertEqual(form.fields['artifact_note_external'].label, 'External note')

    def test_artifact_note_internal_form_label(self):
        """ test form label """

        # get object
        form = ArtifactForm()
        # compare
        self.assertEqual(form.fields['artifact_note_internal'].label, 'Internal note')

    def test_artifact_form_empty(self):
        """ test minimum form requirements / INVALID """

        # get object
        form = ArtifactForm(data = {})
        # compare
        self.assertFalse(form.is_valid())

    def test_artifact_name_form_filled(self):
        """ test minimum form requirements / INVALID """

        # get object
        form = ArtifactForm(data = {
            'artifact_name': 'artifact_1',
        })
        # compare
        self.assertFalse(form.is_valid())

    def test_artifact_artifactpriority_form_filled(self):
        """ test minimum form requirements / INVALID """

        # get object
        artifactpriority_id = Artifactpriority.objects.get(artifactpriority_name='artifactpriority_1').artifactpriority_id
        # get object
        form = ArtifactForm(data = {
            'artifact_name': 'artifact_1',
            'artifactpriority': artifactpriority_id,
        })
        # compare
        self.assertFalse(form.is_valid())

    def test_artifact_artifactstatus_form_filled(self):
        """ test minimum form requirements / INVALID """

        # get object
        artifactpriority_id = Artifactpriority.objects.get(artifactpriority_name='artifactpriority_1').artifactpriority_id
        # get object
        artifactstatus_id = Artifactstatus.objects.get(artifactstatus_name='artifactstatus_1').artifactstatus_id
        # get object
        form = ArtifactForm(data = {
            'artifact_name': 'artifact_1',
            'artifactpriority': artifactpriority_id,
            'artifactstatus': artifactstatus_id,
        })
        # compare
        self.assertFalse(form.is_valid())

    def test_artifact_artifacttype_form_filled(self):
        """ test minimum form requirements / INVALID """

        # get object
        artifactpriority_id = Artifactpriority.objects.get(artifactpriority_name='artifactpriority_1').artifactpriority_id
        # get object
        artifactstatus_id = Artifactstatus.objects.get(artifactstatus_name='artifactstatus_1').artifactstatus_id
        # get object
        artifacttype_id = Artifacttype.objects.get(artifacttype_name='artifacttype_1').artifacttype_id
        # get object
        form = ArtifactForm(data = {
            'artifact_name': 'artifact_1',
            'artifactpriority': artifactpriority_id,
            'artifactstatus': artifactstatus_id,
            'artifacttype': artifacttype_id,
        })
        # compare
        self.assertFalse(form.is_valid())

    def test_artifact_system_form_filled(self):
        """ test minimum form requirements / VALID """

        # get object
        artifactpriority_id = Artifactpriority.objects.get(artifactpriority_name='artifactpriority_1').artifactpriority_id
        # get object
        artifactstatus_id = Artifactstatus.objects.get(artifactstatus_name='artifactstatus_1').artifactstatus_id
        # get object
        artifacttype_id = Artifacttype.objects.get(artifacttype_name='artifacttype_1').artifacttype_id
        # get object
        system_id = System.objects.get(system_name='system_1').system_id
        # get object
        form = ArtifactForm(data = {
            'artifact_name': 'artifact_1',
            'artifactpriority': artifactpriority_id,
            'artifactstatus': artifactstatus_id,
            'artifacttype': artifacttype_id,
            'system': system_id,
        })
        # compare
        self.assertTrue(form.is_valid())

    def test_artifact_source_path_form_filled(self):
        """ test additional form content """

        # get object
        artifactpriority_id = Artifactpriority.objects.get(artifactpriority_name='artifactpriority_1').artifactpriority_id
        # get object
        artifactstatus_id = Artifactstatus.objects.get(artifactstatus_name='artifactstatus_1').artifactstatus_id
        # get object
        artifacttype_id = Artifacttype.objects.get(artifacttype_name='artifacttype_1').artifacttype_id
        # get object
        system_id = System.objects.get(system_name='system_1').system_id
        # get object
        form = ArtifactForm(data = {
            'artifact_name': 'artifact_1',
            'artifactpriority': artifactpriority_id,
            'artifactstatus': artifactstatus_id,
            'artifacttype': artifacttype_id,
            'system': system_id,
            'artifact_source_path': 'C:\Windows\foo\bar',
        })
        # compare
        self.assertTrue(form.is_valid())

    def test_artifact_case_form_filled(self):
        """ test additional form content """

        # get object
        artifactpriority_id = Artifactpriority.objects.get(artifactpriority_name='artifactpriority_1').artifactpriority_id
        # get object
        artifactstatus_id = Artifactstatus.objects.get(artifactstatus_name='artifactstatus_1').artifactstatus_id
        # get object
        artifacttype_id = Artifacttype.objects.get(artifacttype_name='artifacttype_1').artifacttype_id
        # get object
        case_id = Case.objects.get(case_name='case_1').case_id
        # get object
        system_id = System.objects.get(system_name='system_1').system_id
        # get object
        form = ArtifactForm(data = {
            'artifact_name': 'artifact_1',
            'artifactpriority': artifactpriority_id,
            'artifactstatus': artifactstatus_id,
            'artifacttype': artifacttype_id,
            'system': system_id,
            'case': case_id,
        })
        # compare
        self.assertTrue(form.is_valid())

    def test_artifact_requested_time_form_filled(self):
        """ test additional form content """

        # get object
        artifactpriority_id = Artifactpriority.objects.get(artifactpriority_name='artifactpriority_1').artifactpriority_id
        # get object
        artifactstatus_id = Artifactstatus.objects.get(artifactstatus_name='artifactstatus_1').artifactstatus_id
        # get object
        artifacttype_id = Artifacttype.objects.get(artifacttype_name='artifacttype_1').artifacttype_id
        # get object
        system_id = System.objects.get(system_name='system_1').system_id
        # get object
        form = ArtifactForm(data = {
            'artifact_name': 'artifact_1',
            'artifactpriority': artifactpriority_id,
            'artifactstatus': artifactstatus_id,
            'artifacttype': artifacttype_id,
            'system': system_id,
            'artifact_requested_time': timezone.now(),
        })
        # compare
        self.assertTrue(form.is_valid())

    def test_artifact_acquisiton_time_form_filled(self):
        """ test additional form content """

        # get object
        artifactpriority_id = Artifactpriority.objects.get(artifactpriority_name='artifactpriority_1').artifactpriority_id
        # get object
        artifactstatus_id = Artifactstatus.objects.get(artifactstatus_name='artifactstatus_1').artifactstatus_id
        # get object
        artifacttype_id = Artifacttype.objects.get(artifacttype_name='artifacttype_1').artifacttype_id
        # get object
        system_id = System.objects.get(system_name='system_1').system_id
        # get object
        form = ArtifactForm(data = {
            'artifact_name': 'artifact_1',
            'artifactpriority': artifactpriority_id,
            'artifactstatus': artifactstatus_id,
            'artifacttype': artifacttype_id,
            'system': system_id,
            'artifact_acquisiton_time': timezone.now(),
        })
        # compare
        self.assertTrue(form.is_valid())

    def test_artifact_md5_form_filled(self):
        """ test additional form content """

        # get object
        artifactpriority_id = Artifactpriority.objects.get(artifactpriority_name='artifactpriority_1').artifactpriority_id
        # get object
        artifactstatus_id = Artifactstatus.objects.get(artifactstatus_name='artifactstatus_1').artifactstatus_id
        # get object
        artifacttype_id = Artifacttype.objects.get(artifacttype_name='artifacttype_1').artifacttype_id
        # get object
        system_id = System.objects.get(system_name='system_1').system_id
        # get object
        form = ArtifactForm(data = {
            'artifact_name': 'artifact_1',
            'artifactpriority': artifactpriority_id,
            'artifactstatus': artifactstatus_id,
            'artifacttype': artifacttype_id,
            'system': system_id,
            'artifact_md5': 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
        })
        # compare
        self.assertTrue(form.is_valid())

    def test_artifact_sha1_form_filled(self):
        """ test additional form content """

        # get object
        artifactpriority_id = Artifactpriority.objects.get(artifactpriority_name='artifactpriority_1').artifactpriority_id
        # get object
        artifactstatus_id = Artifactstatus.objects.get(artifactstatus_name='artifactstatus_1').artifactstatus_id
        # get object
        artifacttype_id = Artifacttype.objects.get(artifacttype_name='artifacttype_1').artifacttype_id
        # get object
        system_id = System.objects.get(system_name='system_1').system_id
        # get object
        form = ArtifactForm(data = {
            'artifact_name': 'artifact_1',
            'artifactpriority': artifactpriority_id,
            'artifactstatus': artifactstatus_id,
            'artifacttype': artifacttype_id,
            'system': system_id,
            'artifact_sha1': 'bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb',
        })
        # compare
        self.assertTrue(form.is_valid())

    def test_artifact_sha256_form_filled(self):
        """ test additional form content """

        # get object
        artifactpriority_id = Artifactpriority.objects.get(artifactpriority_name='artifactpriority_1').artifactpriority_id
        # get object
        artifactstatus_id = Artifactstatus.objects.get(artifactstatus_name='artifactstatus_1').artifactstatus_id
        # get object
        artifacttype_id = Artifacttype.objects.get(artifacttype_name='artifacttype_1').artifacttype_id
        # get object
        system_id = System.objects.get(system_name='system_1').system_id
        # get object
        form = ArtifactForm(data = {
            'artifact_name': 'artifact_1',
            'artifactpriority': artifactpriority_id,
            'artifactstatus': artifactstatus_id,
            'artifacttype': artifacttype_id,
            'system': system_id,
            'artifact_sha256': 'cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc',
        })
        # compare
        self.assertTrue(form.is_valid())

    def test_artifact_note_analysisresult_form_filled(self):
        """ test additional form content """

        # get object
        artifactpriority_id = Artifactpriority.objects.get(artifactpriority_name='artifactpriority_1').artifactpriority_id
        # get object
        artifactstatus_id = Artifactstatus.objects.get(artifactstatus_name='artifactstatus_1').artifactstatus_id
        # get object
        artifacttype_id = Artifacttype.objects.get(artifacttype_name='artifacttype_1').artifacttype_id
        # get object
        system_id = System.objects.get(system_name='system_1').system_id
        # get object
        form = ArtifactForm(data = {
            'artifact_name': 'artifact_1',
            'artifactpriority': artifactpriority_id,
            'artifactstatus': artifactstatus_id,
            'artifacttype': artifacttype_id,
            'system': system_id,
            'artifact_note_analysisresult': 'this is a note for analysis results - export considered',
        })
        # compare
        self.assertTrue(form.is_valid())

    def test_artifact_note_external_form_filled(self):
        """ test additional form content """

        # get object
        artifactpriority_id = Artifactpriority.objects.get(artifactpriority_name='artifactpriority_1').artifactpriority_id
        # get object
        artifactstatus_id = Artifactstatus.objects.get(artifactstatus_name='artifactstatus_1').artifactstatus_id
        # get object
        artifacttype_id = Artifacttype.objects.get(artifacttype_name='artifacttype_1').artifacttype_id
        # get object
        system_id = System.objects.get(system_name='system_1').system_id
        # get object
        form = ArtifactForm(data = {
            'artifact_name': 'artifact_1',
            'artifactpriority': artifactpriority_id,
            'artifactstatus': artifactstatus_id,
            'artifacttype': artifacttype_id,
            'system': system_id,
            'artifact_note_external': 'this is a note for external usage - export considered',
        })
        # compare
        self.assertTrue(form.is_valid())

    def test_artifact_note_internal_form_filled(self):
        """ test additional form content """

        # get object
        artifactpriority_id = Artifactpriority.objects.get(artifactpriority_name='artifactpriority_1').artifactpriority_id
        # get object
        artifactstatus_id = Artifactstatus.objects.get(artifactstatus_name='artifactstatus_1').artifactstatus_id
        # get object
        artifacttype_id = Artifacttype.objects.get(artifacttype_name='artifacttype_1').artifacttype_id
        # get object
        system_id = System.objects.get(system_name='system_1').system_id
        # get object
        form = ArtifactForm(data = {
            'artifact_name': 'artifact_1',
            'artifactpriority': artifactpriority_id,
            'artifactstatus': artifactstatus_id,
            'artifacttype': artifacttype_id,
            'system': system_id,
            'artifact_note_internal': 'this is a note for internal usage - no export intended',
        })
        # compare
        self.assertTrue(form.is_valid())

    """
    the length of the following attributes is not tested at the moment due to their enormous numbers
    * artifact_name
    * artifact_source_path
    * artifact_storage_path
    """

    def test_artifact_md5_proper_chars(self):
        """ test for max length """

        # get object
        artifactpriority_id = Artifactpriority.objects.get(artifactpriority_name='artifactpriority_1').artifactpriority_id
        # get object
        artifactstatus_id = Artifactstatus.objects.get(artifactstatus_name='artifactstatus_1').artifactstatus_id
        # get object
        artifacttype_id = Artifacttype.objects.get(artifacttype_name='artifacttype_1').artifacttype_id
        # get object
        system_id = System.objects.get(system_name='system_1').system_id
        # get object
        form = ArtifactForm(data = {
            'artifact_name': 'artifact_1',
            'artifactpriority': artifactpriority_id,
            'artifactstatus': artifactstatus_id,
            'artifacttype': artifacttype_id,
            'system': system_id,
            'artifact_md5': 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
        })
        # compare
        self.assertTrue(form.is_valid())

    def test_artifact_md5_hexadecimal_chars(self):
        """ test for hexadecimal characters """

        # get object
        artifactpriority_id = Artifactpriority.objects.get(artifactpriority_name='artifactpriority_1').artifactpriority_id
        # get object
        artifactstatus_id = Artifactstatus.objects.get(artifactstatus_name='artifactstatus_1').artifactstatus_id
        # get object
        artifacttype_id = Artifacttype.objects.get(artifacttype_name='artifacttype_1').artifacttype_id
        # get object
        system_id = System.objects.get(system_name='system_1').system_id
        # get object
        form = ArtifactForm(data = {
            'artifact_name': 'artifact_1',
            'artifactpriority': artifactpriority_id,
            'artifactstatus': artifactstatus_id,
            'artifacttype': artifacttype_id,
            'system': system_id,
            'artifact_md5': 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
        })
        # compare
        self.assertFalse(form.is_valid())

    def test_artifact_md5_too_many_chars(self):
        """ test for max length """

        # get object
        artifactpriority_id = Artifactpriority.objects.get(artifactpriority_name='artifactpriority_1').artifactpriority_id
        # get object
        artifactstatus_id = Artifactstatus.objects.get(artifactstatus_name='artifactstatus_1').artifactstatus_id
        # get object
        artifacttype_id = Artifacttype.objects.get(artifacttype_name='artifacttype_1').artifacttype_id
        # get object
        system_id = System.objects.get(system_name='system_1').system_id
        # get object
        form = ArtifactForm(data = {
            'artifact_name': 'artifact_1',
            'artifactpriority': artifactpriority_id,
            'artifactstatus': artifactstatus_id,
            'artifacttype': artifacttype_id,
            'system': system_id,
            'artifact_md5': 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
        })
        # compare
        self.assertFalse(form.is_valid())

    def test_artifact_md5_too_less_chars(self):
        """ test for min length """

        # get object
        artifactpriority_id = Artifactpriority.objects.get(artifactpriority_name='artifactpriority_1').artifactpriority_id
        # get object
        artifactstatus_id = Artifactstatus.objects.get(artifactstatus_name='artifactstatus_1').artifactstatus_id
        # get object
        artifacttype_id = Artifacttype.objects.get(artifacttype_name='artifacttype_1').artifacttype_id
        # get object
        system_id = System.objects.get(system_name='system_1').system_id
        # get object
        form = ArtifactForm(data = {
            'artifact_name': 'artifact_1',
            'artifactpriority': artifactpriority_id,
            'artifactstatus': artifactstatus_id,
            'artifacttype': artifacttype_id,
            'system': system_id,
            'artifact_md5': 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
        })
        # compare
        self.assertFalse(form.is_valid())

    def test_artifact_sha1_proper_chars(self):
        """ test for max length """

        # get object
        artifactpriority_id = Artifactpriority.objects.get(artifactpriority_name='artifactpriority_1').artifactpriority_id
        # get object
        artifactstatus_id = Artifactstatus.objects.get(artifactstatus_name='artifactstatus_1').artifactstatus_id
        # get object
        artifacttype_id = Artifacttype.objects.get(artifacttype_name='artifacttype_1').artifacttype_id
        # get object
        system_id = System.objects.get(system_name='system_1').system_id
        # get object
        form = ArtifactForm(data = {
            'artifact_name': 'artifact_1',
            'artifactpriority': artifactpriority_id,
            'artifactstatus': artifactstatus_id,
            'artifacttype': artifacttype_id,
            'system': system_id,
            'artifact_sha1': 'bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb',
        })
        # compare
        self.assertTrue(form.is_valid())

    def test_artifact_sha1_hexadecimal_chars(self):
        """ test for hexadecimal characters """

        # get object
        artifactpriority_id = Artifactpriority.objects.get(artifactpriority_name='artifactpriority_1').artifactpriority_id
        # get object
        artifactstatus_id = Artifactstatus.objects.get(artifactstatus_name='artifactstatus_1').artifactstatus_id
        # get object
        artifacttype_id = Artifacttype.objects.get(artifacttype_name='artifacttype_1').artifacttype_id
        # get object
        system_id = System.objects.get(system_name='system_1').system_id
        # get object
        form = ArtifactForm(data = {
            'artifact_name': 'artifact_1',
            'artifactpriority': artifactpriority_id,
            'artifactstatus': artifactstatus_id,
            'artifacttype': artifacttype_id,
            'system': system_id,
            'artifact_sha1': 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
        })
        # compare
        self.assertFalse(form.is_valid())

    def test_artifact_sha1_too_many_chars(self):
        """ test for max length """

        # get object
        artifactpriority_id = Artifactpriority.objects.get(artifactpriority_name='artifactpriority_1').artifactpriority_id
        # get object
        artifactstatus_id = Artifactstatus.objects.get(artifactstatus_name='artifactstatus_1').artifactstatus_id
        # get object
        artifacttype_id = Artifacttype.objects.get(artifacttype_name='artifacttype_1').artifacttype_id
        # get object
        system_id = System.objects.get(system_name='system_1').system_id
        # get object
        form = ArtifactForm(data = {
            'artifact_name': 'artifact_1',
            'artifactpriority': artifactpriority_id,
            'artifactstatus': artifactstatus_id,
            'artifacttype': artifacttype_id,
            'system': system_id,
            'artifact_sha1': 'bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb',
        })
        # compare
        self.assertFalse(form.is_valid())

    def test_artifact_sha1_too_less_chars(self):
        """ test for min length """

        # get object
        artifactpriority_id = Artifactpriority.objects.get(artifactpriority_name='artifactpriority_1').artifactpriority_id
        # get object
        artifactstatus_id = Artifactstatus.objects.get(artifactstatus_name='artifactstatus_1').artifactstatus_id
        # get object
        artifacttype_id = Artifacttype.objects.get(artifacttype_name='artifacttype_1').artifacttype_id
        # get object
        system_id = System.objects.get(system_name='system_1').system_id
        # get object
        form = ArtifactForm(data = {
            'artifact_name': 'artifact_1',
            'artifactpriority': artifactpriority_id,
            'artifactstatus': artifactstatus_id,
            'artifacttype': artifacttype_id,
            'system': system_id,
            'artifact_sha1': 'bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb',
        })
        # compare
        self.assertFalse(form.is_valid())

    def test_artifact_sha256_proper_chars(self):
        """ test for max length """

        # get object
        artifactpriority_id = Artifactpriority.objects.get(artifactpriority_name='artifactpriority_1').artifactpriority_id
        # get object
        artifactstatus_id = Artifactstatus.objects.get(artifactstatus_name='artifactstatus_1').artifactstatus_id
        # get object
        artifacttype_id = Artifacttype.objects.get(artifacttype_name='artifacttype_1').artifacttype_id
        # get object
        system_id = System.objects.get(system_name='system_1').system_id
        # get object
        form = ArtifactForm(data = {
            'artifact_name': 'artifact_1',
            'artifactpriority': artifactpriority_id,
            'artifactstatus': artifactstatus_id,
            'artifacttype': artifacttype_id,
            'system': system_id,
            'artifact_sha256': 'cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc',
        })
        # compare
        self.assertTrue(form.is_valid())

    def test_artifact_sha256_hexadecimal_chars(self):
        """ test for hexadecimal characters """

        # get object
        artifactpriority_id = Artifactpriority.objects.get(artifactpriority_name='artifactpriority_1').artifactpriority_id
        # get object
        artifactstatus_id = Artifactstatus.objects.get(artifactstatus_name='artifactstatus_1').artifactstatus_id
        # get object
        artifacttype_id = Artifacttype.objects.get(artifacttype_name='artifacttype_1').artifacttype_id
        # get object
        system_id = System.objects.get(system_name='system_1').system_id
        # get object
        form = ArtifactForm(data = {
            'artifact_name': 'artifact_1',
            'artifactpriority': artifactpriority_id,
            'artifactstatus': artifactstatus_id,
            'artifacttype': artifacttype_id,
            'system': system_id,
            'artifact_sha256': 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
        })
        # compare
        self.assertFalse(form.is_valid())

    def test_artifact_sha256_too_many_chars(self):
        """ test for max length """

        # get object
        artifactpriority_id = Artifactpriority.objects.get(artifactpriority_name='artifactpriority_1').artifactpriority_id
        # get object
        artifactstatus_id = Artifactstatus.objects.get(artifactstatus_name='artifactstatus_1').artifactstatus_id
        # get object
        artifacttype_id = Artifacttype.objects.get(artifacttype_name='artifacttype_1').artifacttype_id
        # get object
        system_id = System.objects.get(system_name='system_1').system_id
        # get object
        form = ArtifactForm(data = {
            'artifact_name': 'artifact_1',
            'artifactpriority': artifactpriority_id,
            'artifactstatus': artifactstatus_id,
            'artifacttype': artifacttype_id,
            'system': system_id,
            'artifact_sha256': 'ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc',
        })
        # compare
        self.assertFalse(form.is_valid())

    def test_artifact_sha256_too_less_chars(self):
        """ test for min length """

        # get object
        artifactpriority_id = Artifactpriority.objects.get(artifactpriority_name='artifactpriority_1').artifactpriority_id
        # get object
        artifactstatus_id = Artifactstatus.objects.get(artifactstatus_name='artifactstatus_1').artifactstatus_id
        # get object
        artifacttype_id = Artifacttype.objects.get(artifacttype_name='artifacttype_1').artifacttype_id
        # get object
        system_id = System.objects.get(system_name='system_1').system_id
        # get object
        form = ArtifactForm(data = {
            'artifact_name': 'artifact_1',
            'artifactpriority': artifactpriority_id,
            'artifactstatus': artifactstatus_id,
            'artifacttype': artifacttype_id,
            'system': system_id,
            'artifact_sha256': 'ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc',
        })
        # compare
        self.assertFalse(form.is_valid())
