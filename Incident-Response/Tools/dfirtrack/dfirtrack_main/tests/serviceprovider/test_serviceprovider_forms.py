from django.test import TestCase
from dfirtrack_main.forms import ServiceproviderForm

class ServiceproviderFormTestCase(TestCase):
    """ serviceprovider form tests """

    def test_serviceprovider_name_form_label(self):
        """ test form label """

        # get object
        form = ServiceproviderForm()
        # compare
        self.assertEqual(form.fields['serviceprovider_name'].label, 'Serviceprovider name (*)')

    def test_serviceprovider_note_form_label(self):
        """ test form label """

        # get object
        form = ServiceproviderForm()
        # compare
        self.assertEqual(form.fields['serviceprovider_note'].label, 'Serviceprovider note')

    def test_serviceprovider_form_empty(self):
        """ test minimum form requirements / INVALID """

        # get object
        form = ServiceproviderForm(data = {})
        # compare
        self.assertFalse(form.is_valid())

    def test_serviceprovider_name_form_filled(self):
        """ test minimum form requirements / VALID """

        # get object
        form = ServiceproviderForm(data = {
            'serviceprovider_name': 'serviceprovider_1',
        })
        # compare
        self.assertTrue(form.is_valid())

    def test_serviceprovider_note_form_filled(self):
        """ test additional form content """

        # get object
        form = ServiceproviderForm(data = {
            'serviceprovider_name': 'serviceprovider_1',
            'serviceprovider_note': 'lorem ipsum',
        })
        # compare
        self.assertTrue(form.is_valid())

    def test_serviceprovider_name_proper_chars(self):
        """ test for max length """

        # get object
        form = ServiceproviderForm(data = {'serviceprovider_name': 'ssssssssssssssssssssssssssssssssssssssssssssssssss'})
        # compare
        self.assertTrue(form.is_valid())

    def test_serviceprovider_name_too_many_chars(self):
        """ test for max length """

        # get object
        form = ServiceproviderForm(data = {'serviceprovider_name': 'sssssssssssssssssssssssssssssssssssssssssssssssssss'})
        # compare
        self.assertFalse(form.is_valid())
