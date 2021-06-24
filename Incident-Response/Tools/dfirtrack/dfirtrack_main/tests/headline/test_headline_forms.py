from django.test import TestCase
from dfirtrack_main.forms import HeadlineForm

class HeadlineFormTestCase(TestCase):
    """ headline form tests """

    def test_headline_name_form_label(self):
        """ test form label """

        # get object
        form = HeadlineForm()
        # compare
        self.assertEqual(form.fields['headline_name'].label, 'Headline (*)')

    def test_headline_form_empty(self):
        """ test minimum form requirements / INVALID """

        # get object
        form = HeadlineForm(data = {})
        # compare
        self.assertFalse(form.is_valid())

    def test_headline_name_form_filled(self):
        """ test minimum form requirements / VALID """

        # get object
        form = HeadlineForm(data = {'headline_name': 'headline_1'})
        # compare
        self.assertTrue(form.is_valid())

    def test_headline_name_proper_chars(self):
        """ test for max length """

        # get object
        form = HeadlineForm(data = {'headline_name': 'hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh'})
        # compare
        self.assertTrue(form.is_valid())

    def test_headline_name_too_many_chars(self):
        """ test for max length """

        # get object
        form = HeadlineForm(data = {'headline_name': 'hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh'})
        # compare
        self.assertFalse(form.is_valid())
