from django.test import TestCase
from dfirtrack_main.forms import LocationForm

class LocationFormTestCase(TestCase):
    """ location form tests """

    def test_location_name_form_label(self):
        """ test form label """

        # get object
        form = LocationForm()
        # compare
        self.assertEqual(form.fields['location_name'].label, 'Location name (*)')

    def test_location_note_form_label(self):
        """ test form label """

        # get object
        form = LocationForm()
        # compare
        self.assertEqual(form.fields['location_note'].label, 'Location note')

    def test_location_form_empty(self):
        """ test minimum form requirements / INVALID """

        # get object
        form = LocationForm(data = {})
        # compare
        self.assertFalse(form.is_valid())

    def test_location_name_form_filled(self):
        """ test minimum form requirements / VALID """

        # get object
        form = LocationForm(data = {'location_name': 'location_1'})
        # compare
        self.assertTrue(form.is_valid())

    def test_location_note_form_filled(self):
        """ test additional form content """

        # get object
        form = LocationForm(data = {
            'location_name': 'location_1',
            'location_note': 'lorem ipsum',
        })
        # compare
        self.assertTrue(form.is_valid())

    def test_location_name_proper_chars(self):
        """ test for max length """

        # get object
        form = LocationForm(data = {'location_name': 'llllllllllllllllllllllllllllllllllllllllllllllllll'})
        # compare
        self.assertTrue(form.is_valid())

    def test_location_name_too_many_chars(self):
        """ test for max length """

        # get object
        form = LocationForm(data = {'location_name': 'lllllllllllllllllllllllllllllllllllllllllllllllllll'})
        # compare
        self.assertFalse(form.is_valid())
