from django.test import TestCase
from dfirtrack_main.forms import TasknameForm

class TasknameFormTestCase(TestCase):
    """ taskname form tests """

    def test_taskname_name_form_label(self):
        """ test form label """

        # get object
        form = TasknameForm()
        # compare
        self.assertEqual(form.fields['taskname_name'].label, 'Taskname (*)')

    def test_taskname_form_empty(self):
        """ test minimum form requirements / INVALID """

        # get object
        form = TasknameForm(data = {})
        # compare
        self.assertFalse(form.is_valid())

    def test_taskname_name_form_filled(self):
        """ test minimum form requirements / VALID """

        # get object
        form = TasknameForm(data = {'taskname_name': 'taskname_1'})
        # compare
        self.assertTrue(form.is_valid())

    def test_taskname_name_proper_chars(self):
        """ test for max length """

        # get object
        form = TasknameForm(data = {'taskname_name': 'tttttttttttttttttttttttttttttttttttttttttttttttttt'})
        # compare
        self.assertTrue(form.is_valid())

    def test_taskname_name_too_many_chars(self):
        """ test for max length """

        # get object
        form = TasknameForm(data = {'taskname_name': 'ttttttttttttttttttttttttttttttttttttttttttttttttttt'})
        # compare
        self.assertFalse(form.is_valid())
