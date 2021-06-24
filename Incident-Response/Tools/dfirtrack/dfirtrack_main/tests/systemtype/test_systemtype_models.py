from django.test import TestCase
from dfirtrack_main.models import Systemtype

class SystemtypeModelTestCase(TestCase):
    """ systemtype model tests """

    @classmethod
    def setUpTestData(cls):

        # create object
        Systemtype.objects.create(systemtype_name='systemtype_1')

    def test_systemtype_string(self):
        """ test string representation """

        # get object
        systemtype_1 = Systemtype.objects.get(systemtype_name='systemtype_1')
        # compare
        self.assertEqual(str(systemtype_1), 'systemtype_1')

    def test_systemtype_id_attribute_label(self):
        """ test attribute label """

        # get object
        systemtype_1 = Systemtype.objects.get(systemtype_name='systemtype_1')
        # get label
        field_label = systemtype_1._meta.get_field('systemtype_id').verbose_name
        # compare
        self.assertEqual(field_label, 'systemtype id')

    def test_systemtype_name_attribute_label(self):
        """ test attribute label """

        # get object
        systemtype_1 = Systemtype.objects.get(systemtype_name='systemtype_1')
        # get label
        field_label = systemtype_1._meta.get_field('systemtype_name').verbose_name
        # compare
        self.assertEqual(field_label, 'systemtype name')

    def test_systemtype_name_length(self):
        """ test for max length """

        # get object
        systemtype_1 = Systemtype.objects.get(systemtype_name='systemtype_1')
        # get max length
        max_length = systemtype_1._meta.get_field('systemtype_name').max_length
        # compare
        self.assertEqual(max_length, 50)
