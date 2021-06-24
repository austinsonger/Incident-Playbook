from django.test import TestCase
from dfirtrack_main.forms import ContactForm

class ContactFormTestCase(TestCase):
    """ contact form tests """

    def test_contact_name_form_label(self):
        """ test form label """

        # get object
        form = ContactForm()
        # compare
        self.assertEqual(form.fields['contact_name'].label, 'Contact name (*)')

    def test_contact_phone_form_label(self):
        """ test form label """

        # get object
        form = ContactForm()
        # compare
        self.assertEqual(form.fields['contact_phone'].label, 'Contact phone')

    def test_contact_email_form_label(self):
        """ test form label """

        # get object
        form = ContactForm()
        # compare
        self.assertEqual(form.fields['contact_email'].label, 'Contact email (*)')

    def test_contact_note_form_label(self):
        """ test form label """

        # get object
        form = ContactForm()
        # compare
        self.assertEqual(form.fields['contact_note'].label, 'Contact note')

    def test_contact_form_empty(self):
        """ test minimum form requirements / INVALID """

        # get object
        form = ContactForm(data = {})
        # compare
        self.assertFalse(form.is_valid())

    def test_contact_name_form_filled(self):
        """ test minimum form requirements / INVALID """

        # get object
        form = ContactForm(data = {'contact_name': 'contact_1'})
        # compare
        self.assertFalse(form.is_valid())

    def test_contact_email_form_filled(self):
        """ test minimum form requirements / VALID """

        # get object
        form = ContactForm(data = {
            'contact_name': 'contact_1',
            'contact_email': 'contact_1@example.org',
        })
        # compare
        self.assertTrue(form.is_valid())

    def test_contact_phone_form_filled(self):
        """ test additional form content """

        # get object
        form = ContactForm(data = {
            'contact_name': 'contact_1',
            'contact_email': 'contact_1@example.org',
            'contact_phone': '0123456789',
        })
        # compare
        self.assertTrue(form.is_valid())

    def test_contact_note_form_filled(self):
        """ test additional form content """

        # get object
        form = ContactForm(data = {
            'contact_name': 'contact_1',
            'contact_email': 'contact_1@example.org',
            'contact_note': 'lorem ipsum',
        })
        # compare
        self.assertTrue(form.is_valid())

    def test_contact_name_proper_chars(self):
        """ test for max length """

        # get object
        form = ContactForm(data = {
            'contact_name': 'cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc',
            'contact_email': 'contact_1@example.org'
        })
        # compare
        self.assertTrue(form.is_valid())

    def test_contact_name_too_many_chars(self):
        """ test for max length """

        # get object
        form = ContactForm(data = {
            'contact_name': 'ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc',
            'contact_email': 'contact_1@example.org'
        })
        # compare
        self.assertFalse(form.is_valid())

    def test_contact_phone_proper_chars(self):
        """ test for max length """

        # get object
        form = ContactForm(data = {
            'contact_name': 'contact_1',
            'contact_phone': 'cccccccccccccccccccccccccccccccccccccccccccccccccc',
            'contact_email': 'contact_1@example.org'
        })
        # compare
        self.assertTrue(form.is_valid())

    def test_contact_phone_too_many_chars(self):
        """ test for max length """

        # get object
        form = ContactForm(data = {
            'contact_name': 'contact_1',
            'contact_phone': 'ccccccccccccccccccccccccccccccccccccccccccccccccccc',
            'contact_email': 'contact_1@example.org'
        })
        # compare
        self.assertFalse(form.is_valid())

    def test_contact_email_proper_chars(self):
        """ test for max length """

        # get object
        form = ContactForm(data = {
            'contact_name': 'contact_1',
            'contact_email': 'cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc'
        })
        # compare
        self.assertTrue(form.is_valid())

    def test_contact_email_too_many_chars(self):
        """ test for max length """

        # get object
        form = ContactForm(data = {
            'contact_name': 'contact_1',
            'contact_email': 'ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc'
        })
        # compare
        self.assertFalse(form.is_valid())
