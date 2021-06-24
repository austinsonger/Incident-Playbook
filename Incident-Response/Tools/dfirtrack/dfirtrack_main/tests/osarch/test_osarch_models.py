from django.test import TestCase
from dfirtrack_main.models import Osarch

class OsarchModelTestCase(TestCase):
    """ osarch model tests """

    @classmethod
    def setUpTestData(cls):

        # create object
        Osarch.objects.create(osarch_name='osarch_1')

    def test_osarch_string(self):
        """ test string representation """

        # get object
        osarch_1 = Osarch.objects.get(osarch_name='osarch_1')
        # compare
        self.assertEqual(str(osarch_1), 'osarch_1')

    def test_osarch_id_attribute_label(self):
        """ test attribute label """

        # get object
        osarch_1 = Osarch.objects.get(osarch_name='osarch_1')
        # get label
        field_label = osarch_1._meta.get_field('osarch_id').verbose_name
        # compare
        self.assertEqual(field_label, 'osarch id')

    def test_osarch_name_attribute_label(self):
        """ test attribute label """

        # get object
        osarch_1 = Osarch.objects.get(osarch_name='osarch_1')
        # get label
        field_label = osarch_1._meta.get_field('osarch_name').verbose_name
        # compare
        self.assertEqual(field_label, 'osarch name')

    def test_osarch_name_length(self):
        """ test for max length """

        # get object
        osarch_1 = Osarch.objects.get(osarch_name='osarch_1')
        # get max length
        max_length = osarch_1._meta.get_field('osarch_name').max_length
        # compare
        self.assertEqual(max_length, 10)
