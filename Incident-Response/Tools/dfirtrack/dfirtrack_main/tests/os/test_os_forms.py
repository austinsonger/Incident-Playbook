from django.test import TestCase
from dfirtrack_main.forms import OsForm

class OsFormTestCase(TestCase):
    """ os form tests """

    def test_os_name_form_label(self):
        """ test form label """

        # get object
        form = OsForm()
        # compare
        self.assertEqual(form.fields['os_name'].label, 'Os name (*)')

    def test_os_form_empty(self):
        """ test minimum form requirements / INVALID """

        # get object
        form = OsForm(data = {'os_name': ''})
        # compare
        self.assertFalse(form.is_valid())

    def test_os_name_form_filled(self):
        """ test minimum form requirements / VALID """

        # get object
        form = OsForm(data = {'os_name': 'os_1'})
        # compare
        self.assertTrue(form.is_valid())

    def test_os_name_proper_chars(self):
        """ test for max length """

        # get object
        form = OsForm(data = {'os_name': 'oooooooooooooooooooooooooooooo'})
        # compare
        self.assertTrue(form.is_valid())

    def test_os_name_too_many_chars(self):
        """ test for max length """

        # get object
        form = OsForm(data = {'os_name': 'ooooooooooooooooooooooooooooooo'})
        # compare
        self.assertFalse(form.is_valid())
