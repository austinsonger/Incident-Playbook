from django.test import TestCase
from dfirtrack_main.forms import SystemtypeForm

class SystemtypeFormTestCase(TestCase):
    """ systemtype form tests """

    def test_systemtype_name_form_label(self):
        """ test form label """

        # get object
        form = SystemtypeForm()
        # compare
        self.assertEqual(form.fields['systemtype_name'].label, 'Systemtype name (*)')

    def test_systemtype_form_empty(self):
        """ test minimum form requirements / INVALID """

        # get object
        form = SystemtypeForm(data = {})
        # compare
        self.assertFalse(form.is_valid())

    def test_systemtype_name_form_filled(self):
        """ test minimum form requirements / VALID """

        # get object
        form = SystemtypeForm(data = {'systemtype_name': 'systemtype_1'})
        # compare
        self.assertTrue(form.is_valid())

    def test_systemtype_name_proper_chars(self):
        """ test for max length """

        # get object
        form = SystemtypeForm(data = {'systemtype_name': 'ssssssssssssssssssssssssssssssssssssssssssssssssss'})
        # compare
        self.assertTrue(form.is_valid())

    def test_systemtype_name_too_many_chars(self):
        """ test for max length """

        # get object
        form = SystemtypeForm(data = {'systemtype_name': 'sssssssssssssssssssssssssssssssssssssssssssssssssss'})
        # compare
        self.assertFalse(form.is_valid())
