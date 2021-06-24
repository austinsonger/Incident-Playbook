from django.test import TestCase
from dfirtrack_main.forms import ReasonForm

class ReasonFormTestCase(TestCase):
    """ reason form tests """

    def test_reason_name_form_label(self):
        """ test form label """

        # get object
        form = ReasonForm()
        # compare
        self.assertEqual(form.fields['reason_name'].label, 'Reason name (*)')

    def test_reason_note_form_label(self):
        """ test form label """

        # get object
        form = ReasonForm()
        # compare
        self.assertEqual(form.fields['reason_note'].label, 'Reason note')

    def test_reason_form_empty(self):
        """ test minimum form requirements / INVALID """

        # get object
        form = ReasonForm(data = {})
        # compare
        self.assertFalse(form.is_valid())

    def test_reason_name_form_filled(self):
        """ test minimum form requirements / VALID """

        # get object
        form = ReasonForm(data = {'reason_name': 'reason_1'})
        # compare
        self.assertTrue(form.is_valid())

    def test_reason_note_form_filled(self):
        """ test additional form content """

        # get object
        form = ReasonForm(data = {
            'reason_name': 'reason_1',
            'reason_note': 'lorem ipsum',
        })
        # compare
        self.assertTrue(form.is_valid())

    def test_reason_name_proper_chars(self):
        """ test for max length """

        # get object
        form = ReasonForm(data = {'reason_name': 'rrrrrrrrrrrrrrrrrrrrrrrrrrrrrr'})
        # compare
        self.assertTrue(form.is_valid())

    def test_reason_name_too_many_chars(self):
        """ test for max length """

        # get object
        form = ReasonForm(data = {'reason_name': 'rrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr'})
        # compare
        self.assertFalse(form.is_valid())
