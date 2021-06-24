from django.test import TestCase
from dfirtrack_artifacts.models import Artifacttype

class ArtifacttypeModelTestCase(TestCase):
    """ artifacttype model tests """

    @classmethod
    def setUpTestData(cls):

        # create object
        Artifacttype.objects.create(artifacttype_name = 'artifacttype_1')

    def test_artifacttype_string(self):
        """ test string representation """

        # get object
        artifacttype_1 = Artifacttype.objects.get(artifacttype_name='artifacttype_1')
        # compare
        self.assertEqual(str(artifacttype_1), 'artifacttype_1')

    def test_artifacttype_id_attribute_label(self):
        """ test attribute label """

        # get object
        artifacttype_1 = Artifacttype.objects.get(artifacttype_name='artifacttype_1')
        # get label
        field_label = artifacttype_1._meta.get_field('artifacttype_id').verbose_name
        # compare
        self.assertEqual(field_label, 'artifacttype id')

    def test_artifacttype_name_attribute_label(self):
        """ test attribute label """

        # get object
        artifacttype_1 = Artifacttype.objects.get(artifacttype_name='artifacttype_1')
        # get label
        field_label = artifacttype_1._meta.get_field('artifacttype_name').verbose_name
        # compare
        self.assertEqual(field_label, 'artifacttype name')

    def test_artifacttype_note_attribute_label(self):
        """ test attribute label """

        # get object
        artifacttype_1 = Artifacttype.objects.get(artifacttype_name='artifacttype_1')
        # get label
        field_label = artifacttype_1._meta.get_field('artifacttype_note').verbose_name
        # compare
        self.assertEqual(field_label, 'artifacttype note')

    def test_artifacttype_slug_attribute_label(self):
        """ test attribute label """

        # get object
        artifacttype_1 = Artifacttype.objects.get(artifacttype_name='artifacttype_1')
        # get label
        field_label = artifacttype_1._meta.get_field('artifacttype_slug').verbose_name
        # compare
        self.assertEqual(field_label, 'artifacttype slug')

    def test_artifacttype_name_length(self):
        """ test for max length """

        # get object
        artifacttype_1 = Artifacttype.objects.get(artifacttype_name='artifacttype_1')
        # get max length
        max_length = artifacttype_1._meta.get_field('artifacttype_name').max_length
        # compare
        self.assertEqual(max_length, 255)

    def test_artifacttype_slug_length(self):
        """ test for max length """

        # get object
        artifacttype_1 = Artifacttype.objects.get(artifacttype_name='artifacttype_1')
        # get max length
        max_length = artifacttype_1._meta.get_field('artifacttype_slug').max_length
        # compare
        self.assertEqual(max_length, 255)
