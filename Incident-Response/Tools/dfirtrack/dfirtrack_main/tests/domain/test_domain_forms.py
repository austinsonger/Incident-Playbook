from django.test import TestCase
from dfirtrack_main.forms import DomainForm

class DomainFormTestCase(TestCase):
    """ domain form tests """

    def test_domain_name_form_label(self):
        """ test form label """

        # get object
        form = DomainForm()
        # compare
        self.assertEqual(form.fields['domain_name'].label, 'Domain name (*)')

    def test_domain_note_form_label(self):
        """ test form label """

        # get object
        form = DomainForm()
        # compare
        self.assertEqual(form.fields['domain_note'].label, 'Domain note')

    def test_domain_form_empty(self):
        """ test minimum form requirements / INVALID """

        # get object
        form = DomainForm(data = {})
        # compare
        self.assertFalse(form.is_valid())

    def test_domain_name_form_filled(self):
        """ test minimum form requirements / VALID """

        # get object
        form = DomainForm(data = {'domain_name': 'domain_1'})
        # compare
        self.assertTrue(form.is_valid())

    def test_domain_note_form_filled(self):
        """ test additional form content """

        # get object
        form = DomainForm(data = {
            'domain_name': 'domain_1',
            'domain_note': 'lorem ipsum',
        })
        # compare
        self.assertTrue(form.is_valid())

    def test_domain_name_proper_chars(self):
        """ test for max length """

        # get object
        form = DomainForm(data = {'domain_name': 'dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd'})
        # compare
        self.assertTrue(form.is_valid())

    def test_domain_name_too_many_chars(self):
        """ test for max length """

        # get object
        form = DomainForm(data = {'domain_name': 'ddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd'})
        # compare
        self.assertFalse(form.is_valid())
