from django.test import TestCase
from dfirtrack_main.forms import DivisionForm

class DivisionFormTestCase(TestCase):
    """ division form tests """

    def test_division_name_label(self):
        """ test form label """

        # get object
        form = DivisionForm()
        # compare
        self.assertEqual(form.fields['division_name'].label, 'Division name (*)')

    def test_division_note_label(self):
        """ test form label """

        # get object
        form = DivisionForm()
        # compare
        self.assertEqual(form.fields['division_note'].label, 'Division note')

    def test_division_form_empty(self):
        """ test minimum form requirements / INVALID """

        # get object
        form = DivisionForm(data = {})
        # compare
        self.assertFalse(form.is_valid())

    def test_division_name_form_filled(self):
        """ test minimum form requirements / VALID """

        # get object
        form = DivisionForm(data = {'division_name': 'division_1'})
        # compare
        self.assertTrue(form.is_valid())

    def test_division_note_form_filled(self):
        """ test additional form content """

        # get object
        form = DivisionForm(data = {
            'division_name': 'division_1',
            'division_note': 'lorem_ipsum',
        })
        # compare
        self.assertTrue(form.is_valid())

    def test_division_name_proper_chars(self):
        """ test for max length """

        # get object
        form = DivisionForm(data = {'division_name': 'dddddddddddddddddddddddddddddddddddddddddddddddddd'})
        # compare
        self.assertTrue(form.is_valid())

    def test_division_name_too_many_chars(self):
        """ test for max length """

        # get object
        form = DivisionForm(data = {'division_name': 'ddddddddddddddddddddddddddddddddddddddddddddddddddd'})
        # compare
        self.assertFalse(form.is_valid())
