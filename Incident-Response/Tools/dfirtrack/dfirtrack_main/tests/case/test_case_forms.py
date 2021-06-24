from django.test import TestCase
from dfirtrack_main.forms import CaseForm

class CaseFormTestCase(TestCase):
    """ case form tests """

    def test_case_name_form_label(self):
        """ test form label """

        # get object
        form = CaseForm()
        # compare
        self.assertEqual(form.fields['case_name'].label, 'Case name (*)')

    def test_case_is_incident_form_label(self):
        """ test form label """

        # get object
        form = CaseForm()
        # compare
        self.assertEqual(form.fields['case_is_incident'].label, 'Case is incident')

    def test_case_form_empty(self):
        """ test minimum form requirements / INVALID """

        # get object
        form = CaseForm(data = {})
        # compare
        self.assertFalse(form.is_valid())

    def test_case_name_form_filled(self):
        """ test minimum form requirements / VALID """

        # get object
        form = CaseForm(data = {'case_name': 'case_1'})
        # compare
        self.assertTrue(form.is_valid())

    def test_case_name_proper_chars(self):
        """ test for max length """

        # get object
        form = CaseForm(data = {'case_name': 'dddddddddddddddddddddddddddddddddddddddddddddddddd'})
        # compare
        self.assertTrue(form.is_valid())

    def test_case_name_too_many_chars(self):
        """ test for max length """

        # get object
        form = CaseForm(data = {'case_name': 'ddddddddddddddddddddddddddddddddddddddddddddddddddd'})
        # compare
        self.assertFalse(form.is_valid())
