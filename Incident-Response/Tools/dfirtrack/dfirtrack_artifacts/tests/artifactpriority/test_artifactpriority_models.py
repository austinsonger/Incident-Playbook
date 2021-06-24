from django.test import TestCase
from dfirtrack_artifacts.models import Artifactpriority

class ArtifactpriorityModelTestCase(TestCase):
    """ artifactpriority model tests """

    @classmethod
    def setUpTestData(cls):

        # create object
        Artifactpriority.objects.create(artifactpriority_name = 'artifactpriority_1')

    def test_artifactpriority_string(self):
        """ test string representation """

        # get object
        artifactpriority_1 = Artifactpriority.objects.get(artifactpriority_name='artifactpriority_1')
        # compare
        self.assertEqual(str(artifactpriority_1), 'artifactpriority_1')

    def test_artifactpriority_id_attribute_label(self):
        """ test attribute label """

        # get object
        artifactpriority_1 = Artifactpriority.objects.get(artifactpriority_name='artifactpriority_1')
        # get label
        field_label = artifactpriority_1._meta.get_field('artifactpriority_id').verbose_name
        # compare
        self.assertEqual(field_label, 'artifactpriority id')

    def test_artifactpriority_name_attribute_label(self):
        """ test attribute label """

        # get object
        artifactpriority_1 = Artifactpriority.objects.get(artifactpriority_name='artifactpriority_1')
        # get label
        field_label = artifactpriority_1._meta.get_field('artifactpriority_name').verbose_name
        # compare
        self.assertEqual(field_label, 'artifactpriority name')

    def test_artifactpriority_note_attribute_label(self):
        """ test attribute label """

        # get object
        artifactpriority_1 = Artifactpriority.objects.get(artifactpriority_name='artifactpriority_1')
        # get label
        field_label = artifactpriority_1._meta.get_field('artifactpriority_note').verbose_name
        # compare
        self.assertEqual(field_label, 'artifactpriority note')

    def test_artifactpriority_slug_attribute_label(self):
        """ test attribute label """

        # get object
        artifactpriority_1 = Artifactpriority.objects.get(artifactpriority_name='artifactpriority_1')
        # get label
        field_label = artifactpriority_1._meta.get_field('artifactpriority_slug').verbose_name
        # compare
        self.assertEqual(field_label, 'artifactpriority slug')

    def test_artifactpriority_name_length(self):
        """ test for max length """

        # get object
        artifactpriority_1 = Artifactpriority.objects.get(artifactpriority_name='artifactpriority_1')
        # get max length
        max_length = artifactpriority_1._meta.get_field('artifactpriority_name').max_length
        # compare
        self.assertEqual(max_length, 255)

    def test_artifactpriority_slug_length(self):
        """ test for max length """

        # get object
        artifactpriority_1 = Artifactpriority.objects.get(artifactpriority_name='artifactpriority_1')
        # get max length
        max_length = artifactpriority_1._meta.get_field('artifactpriority_slug').max_length
        # compare
        self.assertEqual(max_length, 255)
