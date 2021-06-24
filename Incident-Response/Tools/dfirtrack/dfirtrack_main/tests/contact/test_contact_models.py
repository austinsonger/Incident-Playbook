from django.test import TestCase
from dfirtrack_main.models import Contact

class ContactModelTestCase(TestCase):
    """ contact model tests """

    @classmethod
    def setUpTestData(cls):

        # create object
        Contact.objects.create(contact_name='contact_1', contact_email='contact_1@example.org')

    def test_contact_string(self):
        """ test string representation """

        # get object
        contact_1 = Contact.objects.get(contact_name='contact_1')
        # compare
        self.assertEqual(str(contact_1), 'contact_1')

    def test_contact_id_attribute_label(self):
        """ test attribute label """

        # get object
        contact_1 = Contact.objects.get(contact_name='contact_1')
        # get label
        field_label = contact_1._meta.get_field('contact_id').verbose_name
        # compare
        self.assertEqual(field_label, 'contact id')

    def test_contact_name_attribute_label(self):
        """ test attribute label """

        # get object
        contact_1 = Contact.objects.get(contact_name='contact_1')
        # get label
        field_label = contact_1._meta.get_field('contact_name').verbose_name
        # compare
        self.assertEqual(field_label, 'contact name')

    def test_contact_phone_attribute_label(self):
        """ test attribute label """

        # get object
        contact_1 = Contact.objects.get(contact_name='contact_1')
        # get label
        field_label = contact_1._meta.get_field('contact_phone').verbose_name
        # compare
        self.assertEqual(field_label, 'contact phone')

    def test_contact_email_attribute_label(self):
        """ test attribute label """

        # get object
        contact_1 = Contact.objects.get(contact_name='contact_1')
        # get label
        field_label = contact_1._meta.get_field('contact_email').verbose_name
        # compare
        self.assertEqual(field_label, 'contact email')

    def test_contact_note_attribute_label(self):
        """ test attribute label """

        # get object
        contact_1 = Contact.objects.get(contact_name='contact_1')
        # get label
        field_label = contact_1._meta.get_field('contact_note').verbose_name
        # compare
        self.assertEqual(field_label, 'contact note')

    def test_contact_name_length(self):
        """ test for max length """

        # get object
        contact_1 = Contact.objects.get(contact_name='contact_1')
        # get max length
        max_length = contact_1._meta.get_field('contact_name').max_length
        # compare
        self.assertEqual(max_length, 100)

    def test_contact_phone_length(self):
        """ test for max length """

        # get object
        contact_1 = Contact.objects.get(contact_name='contact_1')
        # get max length
        max_length = contact_1._meta.get_field('contact_phone').max_length
        # compare
        self.assertEqual(max_length, 50)

    def test_contact_email_length(self):
        """ test for max length """

        # get object
        contact_1 = Contact.objects.get(contact_name='contact_1')
        # get max length
        max_length = contact_1._meta.get_field('contact_email').max_length
        # compare
        self.assertEqual(max_length, 100)
