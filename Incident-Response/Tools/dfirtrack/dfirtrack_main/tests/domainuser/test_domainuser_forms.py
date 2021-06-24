from django.test import TestCase
from dfirtrack_main.forms import DomainuserForm
from dfirtrack_main.models import Domain

class DomainuserFormTestCase(TestCase):
    """ domainuser form tests """

    @classmethod
    def setUpTestData(cls):

        # create object
        Domain.objects.create(
            domain_name='domain_1',
        )

    def test_domainuser_name_form_label(self):
        """ test form label """

        # get object
        form = DomainuserForm()
        # compare
        self.assertEqual(form.fields['domainuser_name'].label, 'Domainuser name (*)')

    def test_domainuser_is_domainadmin_form_label(self):
        """ test form label """

        # get object
        form = DomainuserForm()
        # compare
        self.assertEqual(form.fields['domainuser_is_domainadmin'].label, 'Domainuser is domainadmin')

    def test_domainuser_domain_form_label(self):
        """ test form label """

        # get object
        form = DomainuserForm()
        # compare
        self.assertEqual(form.fields['domain'].label, 'Domain (*)')

    def test_domainuser_system_was_logged_on_form_label(self):
        """ test form label """

        # get object
        form = DomainuserForm()
        # compare
        self.assertEqual(form.fields['system_was_logged_on'].label, 'Systems where this domainuser was logged on')

    def test_domainuser_form_empty(self):
        """ test minimum form requirements / INVALID """

        # get object
        form = DomainuserForm(data = {})
        # compare
        self.assertFalse(form.is_valid())

    def test_domainuser_name_form_filled(self):
        """ test minimum form requirements / INVALID """

        # get object
        form = DomainuserForm(data = {'domainuser_name': 'domainuser_1'})
        # compare
        self.assertFalse(form.is_valid())

    def test_domainuser_domain_form_filled(self):
        """ test minimum form requirements / VALID """

        # get foreign key object id
        domain_id = Domain.objects.get(domain_name='domain_1').domain_id
        # get object
        form = DomainuserForm(data = {
            'domainuser_name': 'domainuser_1',
            'domain': domain_id,
        })
        # compare
        self.assertTrue(form.is_valid())

    def test_domainuser_name_proper_chars(self):
        """ test for max length """

        # get foreign key object id
        domain_id = Domain.objects.get(domain_name='domain_1').domain_id
        # get object
        form = DomainuserForm(data = {
            'domainuser_name': 'dddddddddddddddddddddddddddddddddddddddddddddddddd',
            'domain': domain_id,
        })
        # compare
        self.assertTrue(form.is_valid())

    def test_domainuser_name_too_many_chars(self):
        """ test for max length """

        # get foreign key object id
        domain_id = Domain.objects.get(domain_name='domain_1').domain_id
        # get object
        form = DomainuserForm(data = {
            'domainuser_name': 'ddddddddddddddddddddddddddddddddddddddddddddddddddd',
            'domain': domain_id,
        })
        # compare
        self.assertFalse(form.is_valid())
