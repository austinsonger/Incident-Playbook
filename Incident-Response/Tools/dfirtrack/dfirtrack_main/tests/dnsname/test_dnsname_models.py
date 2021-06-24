from django.test import TestCase
from dfirtrack_main.models import Dnsname

class DnsnameModelTestCase(TestCase):
    """ dnsname model tests """

    @classmethod
    def setUpTestData(cls):

        # create object
        Dnsname.objects.create(dnsname_name='dnsname_1')

    def test_dnsname_string(self):
        """ test string representation """

        # get object
        dnsname_1 = Dnsname.objects.get(dnsname_name='dnsname_1')
        # compare
        self.assertEqual(str(dnsname_1), 'dnsname_1')

    def test_dnsname_id_attribute_label(self):
        """ test attribute label """

        # get object
        dnsname_1 = Dnsname.objects.get(dnsname_name='dnsname_1')
        # get label
        field_label = dnsname_1._meta.get_field('dnsname_id').verbose_name
        # compare
        self.assertEqual(field_label, 'dnsname id')

    def test_dnsname_domain_attribute_label(self):
        """ test attribute label """

        # get object
        dnsname_1 = Dnsname.objects.get(dnsname_name='dnsname_1')
        # get label
        field_label = dnsname_1._meta.get_field('domain').verbose_name
        # compare
        self.assertEqual(field_label, 'domain')

    def test_dnsname_name_attribute_label(self):
        """ test attribute label """

        # get object
        dnsname_1 = Dnsname.objects.get(dnsname_name='dnsname_1')
        # get label
        field_label = dnsname_1._meta.get_field('dnsname_name').verbose_name
        # compare
        self.assertEqual(field_label, 'dnsname name')

    def test_dnsname_note_attribute_label(self):
        """ test attribute label """

        # get object
        dnsname_1 = Dnsname.objects.get(dnsname_name='dnsname_1')
        # get label
        field_label = dnsname_1._meta.get_field('dnsname_note').verbose_name
        # compare
        self.assertEqual(field_label, 'dnsname note')

    def test_dnsname_name_length(self):
        """ test for max length """

        # get object
        dnsname_1 = Dnsname.objects.get(dnsname_name='dnsname_1')
        # get max length
        max_length = dnsname_1._meta.get_field('dnsname_name').max_length
        # compare
        self.assertEqual(max_length, 100)
