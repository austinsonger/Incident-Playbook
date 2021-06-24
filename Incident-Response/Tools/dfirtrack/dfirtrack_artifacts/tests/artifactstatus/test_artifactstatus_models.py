from django.test import TestCase
from dfirtrack_artifacts.models import Artifactstatus

class ArtifactstatusModelTestCase(TestCase):
    """ artifactstatus model tests """

    @classmethod
    def setUpTestData(cls):

        # create object
        Artifactstatus.objects.create(artifactstatus_name = 'artifactstatus_1')

    def test_artifactstatus_string(self):
        """ test string representation """

        # get object
        artifactstatus_1 = Artifactstatus.objects.get(artifactstatus_name='artifactstatus_1')
        # compare
        self.assertEqual(str(artifactstatus_1), 'artifactstatus_1')

    def test_artifactstatus_id_attribute_label(self):
        """ test attribute label """

        # get object
        artifactstatus_1 = Artifactstatus.objects.get(artifactstatus_name='artifactstatus_1')
        # get label
        field_label = artifactstatus_1._meta.get_field('artifactstatus_id').verbose_name
        # compare
        self.assertEqual(field_label, 'artifactstatus id')

    def test_artifactstatus_name_attribute_label(self):
        """ test attribute label """

        # get object
        artifactstatus_1 = Artifactstatus.objects.get(artifactstatus_name='artifactstatus_1')
        # get label
        field_label = artifactstatus_1._meta.get_field('artifactstatus_name').verbose_name
        # compare
        self.assertEqual(field_label, 'artifactstatus name')

    def test_artifactstatus_note_attribute_label(self):
        """ test attribute label """

        # get object
        artifactstatus_1 = Artifactstatus.objects.get(artifactstatus_name='artifactstatus_1')
        # get label
        field_label = artifactstatus_1._meta.get_field('artifactstatus_note').verbose_name
        # compare
        self.assertEqual(field_label, 'artifactstatus note')

    def test_artifactstatus_slug_attribute_label(self):
        """ test attribute label """

        # get object
        artifactstatus_1 = Artifactstatus.objects.get(artifactstatus_name='artifactstatus_1')
        # get label
        field_label = artifactstatus_1._meta.get_field('artifactstatus_slug').verbose_name
        # compare
        self.assertEqual(field_label, 'artifactstatus slug')

    def test_artifactstatus_name_length(self):
        """ test for max length """

        # get object
        artifactstatus_1 = Artifactstatus.objects.get(artifactstatus_name='artifactstatus_1')
        # get max length
        max_length = artifactstatus_1._meta.get_field('artifactstatus_name').max_length
        # compare
        self.assertEqual(max_length, 255)

    def test_artifactstatus_slug_length(self):
        """ test for max length """

        # get object
        artifactstatus_1 = Artifactstatus.objects.get(artifactstatus_name='artifactstatus_1')
        # get max length
        max_length = artifactstatus_1._meta.get_field('artifactstatus_slug').max_length
        # compare
        self.assertEqual(max_length, 255)
