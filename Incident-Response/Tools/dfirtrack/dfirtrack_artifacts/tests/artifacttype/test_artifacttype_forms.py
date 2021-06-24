from django.test import TestCase
from dfirtrack_artifacts.forms import ArtifacttypeForm

class ArtifacttypeFormTestCase(TestCase):
    """ artifacttype form tests """

    def test_artifacttype_name_form_label(self):
        """ test form label """

        # get object
        form = ArtifacttypeForm()
        # compare
        self.assertEqual(form.fields['artifacttype_name'].label, 'Artifacttype name (*)')

    def test_artifacttype_note_form_label(self):
        """ test form label """

        # get object
        form = ArtifacttypeForm()
        # compare
        self.assertEqual(form.fields['artifacttype_note'].label, 'Artifacttype note')

    def test_artifacttype_form_empty(self):
        """ test minimum form requirements / INVALID """

        # get object
        form = ArtifacttypeForm(data = {})
        # compare
        self.assertFalse(form.is_valid())

    def test_artifacttype_name_form_filled(self):
        """ test minimum form requirements / VALID """

        # get object
        form = ArtifacttypeForm(data = {'artifacttype_name': 'artifacttype_1'})
        # compare
        self.assertTrue(form.is_valid())

    def test_artifacttype_note_form_filled(self):
        """ test additional form content """

        # get object
        form = ArtifacttypeForm(data = {
            'artifacttype_name': 'artifacttype_1',
            'artifacttype_note': 'lorem ipsum',
        })
        # compare
        self.assertTrue(form.is_valid())

    def test_artifacttype_name_proper_chars(self):
        """ test for max length """

        # get object
        form = ArtifacttypeForm(data = {'artifacttype_name': 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'})
        # compare
        self.assertTrue(form.is_valid())

    def test_artifacttype_name_too_many_chars(self):
        """ test for max length """

        # get object
        form = ArtifacttypeForm(data = {'artifacttype_name': 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'})
        # compare
        self.assertFalse(form.is_valid())
