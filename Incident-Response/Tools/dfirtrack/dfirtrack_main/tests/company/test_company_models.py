from django.test import TestCase
from dfirtrack_main.models import Company

class CompanyModelTestCase(TestCase):
    """ company model tests """

    @classmethod
    def setUpTestData(cls):

        # create object
        Company.objects.create(company_name='company_1')

    def test_company_string(self):
        """ test string representation """

        # get object
        company_1 = Company.objects.get(company_name='company_1')
        # compare
        self.assertEqual(str(company_1), 'company_1')

    def test_company_id_attribute_label(self):
        """ test attribute label """

        # get object
        company_1 = Company.objects.get(company_name='company_1')
        # get label
        field_label = company_1._meta.get_field('company_id').verbose_name
        # compare
        self.assertEqual(field_label, 'company id')

    def test_company_division_attribute_label(self):
        """ test attribute label """

        # get object
        company_1 = Company.objects.get(company_name='company_1')
        # get label
        field_label = company_1._meta.get_field('division').verbose_name
        # compare
        self.assertEqual(field_label, 'division')

    def test_company_name_attribute_label(self):
        """ test attribute label """

        # get object
        company_1 = Company.objects.get(company_name='company_1')
        # get label
        field_label = company_1._meta.get_field('company_name').verbose_name
        # compare
        self.assertEqual(field_label, 'company name')

    def test_company_note_attribute_label(self):
        """ test attribute label """

        # get object
        company_1 = Company.objects.get(company_name='company_1')
        # get label
        field_label = company_1._meta.get_field('company_note').verbose_name
        # compare
        self.assertEqual(field_label, 'company note')

    def test_company_name_length(self):
        """ test for max length """

        # get object
        company_1 = Company.objects.get(company_name='company_1')
        # get max length
        max_length = company_1._meta.get_field('company_name').max_length
        # compare
        self.assertEqual(max_length, 50)
