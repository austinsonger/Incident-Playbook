from django.test import TestCase
from dfirtrack_main.forms import CompanyForm
from dfirtrack_main.models import Division

class CompanyFormTestCase(TestCase):
    """ company form tests """

    @classmethod
    def setUpTestData(cls):

        # create object
        Division.objects.create(division_name='division_1')

    def test_company_name_form_label(self):
        """ test form label """

        # get object
        form = CompanyForm()
        # compare
        self.assertEqual(form.fields['company_name'].label, 'Company name (*)')

    def test_company_division_form_label(self):
        """ test form label """

        # get object
        form = CompanyForm()
        # compare
        self.assertEqual(form.fields['division'].label, 'Division')

    def test_company_note_form_label(self):
        """ test form label """

        # get object
        form = CompanyForm()
        # compare
        self.assertEqual(form.fields['company_note'].label, 'Company note')

    def test_company_form_empty(self):
        """ test minimum form requirements / INVALID """

        # get object
        form = CompanyForm(data = {})
        # compare
        self.assertFalse(form.is_valid())

    def test_company_name_form_filled(self):
        """ test minimum form requirements / VALID """

        # get object
        form = CompanyForm(data = {'company_name': 'company_1'})
        # compare
        self.assertTrue(form.is_valid())

    def test_company_division_form_filled(self):
        """ test additional form content """

        # get foreign key object id
        division_id = Division.objects.get(division_name='division_1').division_id
        # get object
        form = CompanyForm(data = {
            'company_name': 'company_1',
            'division': division_id,
        })
        # compare
        self.assertTrue(form.is_valid())

    def test_company_note_form_filled(self):
        """ test additional form content """

        # get foreign key object id
        division_id = Division.objects.get(division_name='division_1').division_id
        # get object
        form = CompanyForm(data = {
            'company_name': 'company_1',
            'division': division_id,
            'company_note': 'lorem_ipsum',
        })
        # compare
        self.assertTrue(form.is_valid())

    def test_company_name_proper_chars(self):
        """ test for max length """

        # get object
        form = CompanyForm(data = {'company_name': 'cccccccccccccccccccccccccccccccccccccccccccccccccc'})
        # compare
        self.assertTrue(form.is_valid())

    def test_company_name_too_many_chars(self):
        """ test for max length """

        # get object
        form = CompanyForm(data = {'company_name': 'ccccccccccccccccccccccccccccccccccccccccccccccccccc'})
        # compare
        self.assertFalse(form.is_valid())
