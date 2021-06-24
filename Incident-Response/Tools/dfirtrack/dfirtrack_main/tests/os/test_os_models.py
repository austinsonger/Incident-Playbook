from django.test import TestCase
from dfirtrack_main.models import Os

class OsModelTestCase(TestCase):
    """ os model tests """

    @classmethod
    def setUpTestData(cls):

        # create object
        Os.objects.create(os_name='os_1')

    def test_os_string(self):
        """ test string representation """

        # get object
        os_1 = Os.objects.get(os_name='os_1')
        # compare
        self.assertEqual(str(os_1), 'os_1')

    def test_os_id_attribute_label(self):
        """ test attribute label """

        # get object
        os_1 = Os.objects.get(os_name='os_1')
        # get label
        field_label = os_1._meta.get_field('os_id').verbose_name
        # compare
        self.assertEqual(field_label, 'os id')

    def test_os_name_attribute_label(self):
        """ test attribute label """

        # get object
        os_1 = Os.objects.get(os_name='os_1')
        # get label
        field_label = os_1._meta.get_field('os_name').verbose_name
        # compare
        self.assertEqual(field_label, 'os name')

    def test_os_name_length(self):
        """ test for max length """

        # get object
        os_1 = Os.objects.get(os_name='os_1')
        # get max length
        max_length = os_1._meta.get_field('os_name').max_length
        # compare
        self.assertEqual(max_length, 30)
