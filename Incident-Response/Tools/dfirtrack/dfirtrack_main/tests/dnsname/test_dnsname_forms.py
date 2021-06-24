from django.test import TestCase
from dfirtrack_main.forms import DnsnameForm
from dfirtrack_main.models import Domain

class DnsnameFormTestCase(TestCase):
    """ dnsname form tests """

    @classmethod
    def setUpTestData(cls):

        # create object
        Domain.objects.create(domain_name='domain_1')

    def test_dnsname_domain_form_label(self):
        """ test form label """

        # get object
        form = DnsnameForm()
        # compare
        self.assertEqual(form.fields['domain'].label, 'Domain')

    def test_dnsname_name_form_label(self):
        """ test form label """

        # get object
        form = DnsnameForm()
        # compare
        self.assertEqual(form.fields['dnsname_name'].label, 'DNS name (*)')

    def test_dnsname_note_form_label(self):
        """ test form label """

        # get object
        form = DnsnameForm()
        # compare
        self.assertEqual(form.fields['dnsname_note'].label, 'Note')

    def test_dnsname_form_empty(self):
        """ test minimum form requirements / INVALID """

        # get object
        form = DnsnameForm(data = {})
        # compare
        self.assertFalse(form.is_valid())

    def test_dnsname_name_form_filled(self):
        """ test minimum form requirements / VALID """

        # get object
        form = DnsnameForm(data = {'dnsname_name': 'dnsname_1'})
        # compare
        self.assertTrue(form.is_valid())

    def test_dnsname_domain_form_filled(self):
        """ test additional form content """

        # get foreign key object id
        domain_id = Domain.objects.get(domain_name='domain_1').domain_id
        # get object
        form = DnsnameForm(data = {
            'dnsname_name': 'dnsname_1',
            'domain': domain_id,
        })
        # compare
        self.assertTrue(form.is_valid())

    def test_dnsname_note_form_filled(self):
        """ test additional form content """

        # get object
        form = DnsnameForm(data = {
            'dnsname_name': 'dnsname_1',
            'dnsname_note': 'lorem ipsum',
        })
        # compare
        self.assertTrue(form.is_valid())

    def test_dnsname_name_proper_chars(self):
        """ test for max length """

        # get object
        form = DnsnameForm(data = {'dnsname_name': 'dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd'})
        # compare
        self.assertTrue(form.is_valid())

    def test_dnsname_name_too_many_chars(self):
        """ test for max length """

        # get object
        form = DnsnameForm(data = {'dnsname_name': 'ddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd'})
        # compare
        self.assertFalse(form.is_valid())
