from django.test import TestCase
from dfirtrack_main.models import Location

class LocationModelTestCase(TestCase):
    """ location model tests """

    @classmethod
    def setUpTestData(cls):

        # create object
        Location.objects.create(location_name='location_1')

    def test_location_string(self):
        """ test string representation """

        # get object
        location_1 = Location.objects.get(location_name='location_1')
        # compare
        self.assertEqual(str(location_1), 'location_1')

    def test_location_id_attribute_label(self):
        """ test attribute label """

        # get object
        location_1 = Location.objects.get(location_name='location_1')
        # get label
        field_label = location_1._meta.get_field('location_id').verbose_name
        # compare
        self.assertEqual(field_label, 'location id')

    def test_location_name_attribute_label(self):
        """ test attribute label """

        # get object
        location_1 = Location.objects.get(location_name='location_1')
        # get label
        field_label = location_1._meta.get_field('location_name').verbose_name
        # compare
        self.assertEqual(field_label, 'location name')

    def test_location_note_attribute_label(self):
        """ test attribute label """

        # get object
        location_1 = Location.objects.get(location_name='location_1')
        # get label
        field_label = location_1._meta.get_field('location_note').verbose_name
        # compare
        self.assertEqual(field_label, 'location note')

    def test_location_name_length(self):
        """ test for max length """

        # get object
        location_1 = Location.objects.get(location_name='location_1')
        # get max length
        max_length = location_1._meta.get_field('location_name').max_length
        # compare
        self.assertEqual(max_length, 50)
