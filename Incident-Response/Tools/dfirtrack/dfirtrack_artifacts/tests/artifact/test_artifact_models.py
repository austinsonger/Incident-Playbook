from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone
from dfirtrack_artifacts.models import Artifact, Artifactpriority, Artifactstatus, Artifacttype
from dfirtrack.config import EVIDENCE_PATH
from dfirtrack_main.models import System, Systemstatus
import os

class ArtifactModelTestCase(TestCase):
    """ artifact model tests """

    @classmethod
    def setUpTestData(cls):

        # create user
        test_user = User.objects.create_user(username='testuser_artifact', password='dfIlDYMVqsRnLjpUR9EL')

        # create object
        systemstatus_1 = Systemstatus.objects.create(systemstatus_name='systemstatus_1')

        # create object
        system_1 = System.objects.create(
            system_name='system_1',
            systemstatus = systemstatus_1,
            system_modify_time = timezone.now(),
            system_created_by_user_id = test_user,
            system_modified_by_user_id = test_user,
        )

        # create object
        artifactpriority_1 = Artifactpriority.objects.create(artifactpriority_name='artifactpriority_1')

        # create object
        artifactstatus_1 = Artifactstatus.objects.create(artifactstatus_name='artifactstatus_1')

        # create object
        artifacttype_1 = Artifacttype.objects.create(artifacttype_name='artifacttype_1')

        # create object
        Artifact.objects.create(
            artifact_name = 'artifact_1',
            artifactpriority = artifactpriority_1,
            artifactstatus = artifactstatus_1,
            artifacttype = artifacttype_1,
            artifact_created_by_user_id = test_user,
            artifact_modified_by_user_id = test_user,
            system = system_1,
        )

    def test_artifact_string(self):
        """ test string representation """

        # get object
        artifact_1 = Artifact.objects.get(artifact_name='artifact_1')
        # get object id
        artifact_id = artifact_1.artifact_id
        # get foreign key object id
        system_id = artifact_1.system.system_id
        # compare
        self.assertEqual(str(artifact_1), 'Artifact ' + str(artifact_id) + ' ([' + str(system_id) + '] system_1)')

    def test_artifact_id_attribute_label(self):
        """ test attribute label """

        # get object
        artifact_1 = Artifact.objects.get(artifact_name='artifact_1')
        # get label
        field_label = artifact_1._meta.get_field('artifact_id').verbose_name
        # compare
        self.assertEqual(field_label, 'artifact id')

    def test_artifact_artifactpriority_attribute_label(self):
        """ test attribute label """

        # get object
        artifact_1 = Artifact.objects.get(artifact_name='artifact_1')
        # get label
        field_label = artifact_1._meta.get_field('artifactpriority').verbose_name
        # compare
        self.assertEqual(field_label, 'artifactpriority')

    def test_artifact_artifactstatus_attribute_label(self):
        """ test attribute label """

        # get object
        artifact_1 = Artifact.objects.get(artifact_name='artifact_1')
        # get label
        field_label = artifact_1._meta.get_field('artifactstatus').verbose_name
        # compare
        self.assertEqual(field_label, 'artifactstatus')

    def test_artifact_artifacttype_attribute_label(self):
        """ test attribute label """

        # get object
        artifact_1 = Artifact.objects.get(artifact_name='artifact_1')
        # get label
        field_label = artifact_1._meta.get_field('artifacttype').verbose_name
        # compare
        self.assertEqual(field_label, 'artifacttype')

    def test_artifact_case_attribute_label(self):
        """ test attribute label """

        # get object
        artifact_1 = Artifact.objects.get(artifact_name='artifact_1')
        # get label
        field_label = artifact_1._meta.get_field('case').verbose_name
        # compare
        self.assertEqual(field_label, 'case')

    def test_artifact_system_attribute_label(self):
        """ test attribute label """

        # get object
        artifact_1 = Artifact.objects.get(artifact_name='artifact_1')
        # get label
        field_label = artifact_1._meta.get_field('system').verbose_name
        # compare
        self.assertEqual(field_label, 'system')

    def test_artifact_acquisition_time_attribute_label(self):
        """ test attribute label """

        # get object
        artifact_1 = Artifact.objects.get(artifact_name='artifact_1')
        # get label
        field_label = artifact_1._meta.get_field('artifact_acquisition_time').verbose_name
        # compare
        self.assertEqual(field_label, 'artifact acquisition time')

    def test_artifact_md5_attribute_label(self):
        """ test attribute label """

        # get object
        artifact_1 = Artifact.objects.get(artifact_name='artifact_1')
        # get label
        field_label = artifact_1._meta.get_field('artifact_md5').verbose_name
        # compare
        self.assertEqual(field_label, 'artifact md5')

    def test_artifact_name_attribute_label(self):
        """ test attribute label """

        # get object
        artifact_1 = Artifact.objects.get(artifact_name='artifact_1')
        # get label
        field_label = artifact_1._meta.get_field('artifact_name').verbose_name
        # compare
        self.assertEqual(field_label, 'artifact name')

    def test_artifact_note_analysisresult_attribute_label(self):
        """ test attribute label """

        # get object
        artifact_1 = Artifact.objects.get(artifact_name='artifact_1')
        # get label
        field_label = artifact_1._meta.get_field('artifact_note_analysisresult').verbose_name
        # compare
        self.assertEqual(field_label, 'artifact note analysisresult')

    def test_artifact_note_external_attribute_label(self):
        """ test attribute label """

        # get object
        artifact_1 = Artifact.objects.get(artifact_name='artifact_1')
        # get label
        field_label = artifact_1._meta.get_field('artifact_note_external').verbose_name
        # compare
        self.assertEqual(field_label, 'artifact note external')

    def test_artifact_note_internal_attribute_label(self):
        """ test attribute label """

        # get object
        artifact_1 = Artifact.objects.get(artifact_name='artifact_1')
        # get label
        field_label = artifact_1._meta.get_field('artifact_note_internal').verbose_name
        # compare
        self.assertEqual(field_label, 'artifact note internal')

    def test_artifact_requested_time_attribute_label(self):
        """ test attribute label """

        # get object
        artifact_1 = Artifact.objects.get(artifact_name='artifact_1')
        # get label
        field_label = artifact_1._meta.get_field('artifact_requested_time').verbose_name
        # compare
        self.assertEqual(field_label, 'artifact requested time')

    def test_artifact_sha1_attribute_label(self):
        """ test attribute label """

        # get object
        artifact_1 = Artifact.objects.get(artifact_name='artifact_1')
        # get label
        field_label = artifact_1._meta.get_field('artifact_sha1').verbose_name
        # compare
        self.assertEqual(field_label, 'artifact sha1')

    def test_artifact_sha256_attribute_label(self):
        """ test attribute label """

        # get object
        artifact_1 = Artifact.objects.get(artifact_name='artifact_1')
        # get label
        field_label = artifact_1._meta.get_field('artifact_sha256').verbose_name
        # compare
        self.assertEqual(field_label, 'artifact sha256')

    def test_artifact_slug_attribute_label(self):
        """ test attribute label """

        # get object
        artifact_1 = Artifact.objects.get(artifact_name='artifact_1')
        # get label
        field_label = artifact_1._meta.get_field('artifact_slug').verbose_name
        # compare
        self.assertEqual(field_label, 'artifact slug')

    def test_artifact_storage_path_attribute_label(self):
        """ test attribute label """

        # get object
        artifact_1 = Artifact.objects.get(artifact_name='artifact_1')
        # get label
        field_label = artifact_1._meta.get_field('artifact_storage_path').verbose_name
        # compare
        self.assertEqual(field_label, 'artifact storage path')

    def test_artifact_uuid_attribute_label(self):
        """ test attribute label """

        # get object
        artifact_1 = Artifact.objects.get(artifact_name='artifact_1')
        # get label
        field_label = artifact_1._meta.get_field('artifact_uuid').verbose_name
        # compare
        self.assertEqual(field_label, 'artifact uuid')

    def test_artifact_create_time_attribute_label(self):
        """ test attribute label """

        # get object
        artifact_1 = Artifact.objects.get(artifact_name='artifact_1')
        # get label
        field_label = artifact_1._meta.get_field('artifact_create_time').verbose_name
        # compare
        self.assertEqual(field_label, 'artifact create time')

    def test_artifact_modify_time_attribute_label(self):
        """ test attribute label """

        # get object
        artifact_1 = Artifact.objects.get(artifact_name='artifact_1')
        # get label
        field_label = artifact_1._meta.get_field('artifact_modify_time').verbose_name
        # compare
        self.assertEqual(field_label, 'artifact modify time')

    def test_artifact_created_by_user_id_attribute_label(self):
        """ test attribute label """

        # get object
        artifact_1 = Artifact.objects.get(artifact_name='artifact_1')
        # get label
        field_label = artifact_1._meta.get_field('artifact_created_by_user_id').verbose_name
        # compare
        self.assertEqual(field_label, 'artifact created by user id')

    def test_artifact_modified_by_user_id_attribute_label(self):
        """ test attribute label """

        # get object
        artifact_1 = Artifact.objects.get(artifact_name='artifact_1')
        # get label
        field_label = artifact_1._meta.get_field('artifact_modified_by_user_id').verbose_name
        # compare
        self.assertEqual(field_label, 'artifact modified by user id')

    def test_artifact_md5_length(self):
        """ test for max length """

        # get object
        artifact_1 = Artifact.objects.get(artifact_name='artifact_1')
        # get max length
        max_length = artifact_1._meta.get_field('artifact_md5').max_length
        # compare
        self.assertEqual(max_length, 32)

    def test_artifact_name_length(self):
        """ test for max length """

        # get object
        artifact_1 = Artifact.objects.get(artifact_name='artifact_1')
        # get max length
        max_length = artifact_1._meta.get_field('artifact_name').max_length
        # compare
        self.assertEqual(max_length, 4096)

    def test_artifact_sha1_length(self):
        """ test for max length """

        # get object
        artifact_1 = Artifact.objects.get(artifact_name='artifact_1')
        # get max length
        max_length = artifact_1._meta.get_field('artifact_sha1').max_length
        # compare
        self.assertEqual(max_length, 40)

    def test_artifact_sha256_length(self):
        """ test for max length """

        # get object
        artifact_1 = Artifact.objects.get(artifact_name='artifact_1')
        # get max length
        max_length = artifact_1._meta.get_field('artifact_sha256').max_length
        # compare
        self.assertEqual(max_length, 64)

    def test_artifact_storage_path(self):
        """ test storage path """

        # get object
        artifact_uuid = Artifact.objects.get(artifact_name = 'artifact_1').artifact_uuid
        system_uuid = System.objects.get(system_name = 'system_1').system_uuid
        artifacttype_name = Artifacttype.objects.get(artifacttype_name = 'artifacttype_1').artifacttype_name
        # build path
        artifact_storage_path = (EVIDENCE_PATH + '/' + str(system_uuid) + '/' + artifacttype_name + '/' + str(artifact_uuid))
        # compare
        self.assertTrue(os.path.exists(artifact_storage_path))
