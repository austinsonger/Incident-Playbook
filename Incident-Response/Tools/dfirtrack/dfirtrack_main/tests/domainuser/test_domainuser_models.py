from django.test import TestCase
from dfirtrack_main.models import Domain, Domainuser

class DomainuserModelTestCase(TestCase):
    """ domainuser model tests """

    @classmethod
    def setUpTestData(cls):

        # create object
        domain_1 = Domain.objects.create(
            domain_name='domain_1',
        )

        # create object
        Domainuser.objects.create(domainuser_name='domainuser_1', domain = domain_1)

    def test_domainuser_string(self):
        """ test string representation """

        # get object
        domainuser_1 = Domainuser.objects.get(domainuser_name='domainuser_1')
        # compare
        self.assertEqual(str(domainuser_1), domainuser_1.domainuser_name + ' (' + str(domainuser_1.domain) + ')')

    def test_domainuser_id_attribute_label(self):
        """ test attribute label """

        # get object
        domainuser_1 = Domainuser.objects.get(domainuser_name='domainuser_1')
        # get label
        field_label = domainuser_1._meta.get_field('domainuser_id').verbose_name
        # compare
        self.assertEqual(field_label, 'domainuser id')

    def test_domainuser_domain_attribute_label(self):
        """ test attribute label """

        # get object
        domainuser_1 = Domainuser.objects.get(domainuser_name='domainuser_1')
        # get label
        field_label = domainuser_1._meta.get_field('domain').verbose_name
        # compare
        self.assertEqual(field_label, 'domain')

    def test_domainuser_system_was_logged_on_attribute_label(self):
        """ test attribute label """

        # get object
        domainuser_1 = Domainuser.objects.get(domainuser_name='domainuser_1')
        # get label
        field_label = domainuser_1._meta.get_field('system_was_logged_on').verbose_name
        # compare
        self.assertEqual(field_label, 'system was logged on')

    def test_domainuser_name_attribute_label(self):
        """ test attribute label """

        # get object
        domainuser_1 = Domainuser.objects.get(domainuser_name='domainuser_1')
        # get label
        field_label = domainuser_1._meta.get_field('domainuser_name').verbose_name
        # compare
        self.assertEqual(field_label, 'domainuser name')

    def test_domainuser_is_domainadmin_attribute_label(self):
        """ test attribute label """

        # get object
        domainuser_1 = Domainuser.objects.get(domainuser_name='domainuser_1')
        # get label
        field_label = domainuser_1._meta.get_field('domainuser_is_domainadmin').verbose_name
        # compare
        self.assertEqual(field_label, 'domainuser is domainadmin')

    def test_domainuser_name_length(self):
        """ test for max length """

        # get object
        domainuser_1 = Domainuser.objects.get(domainuser_name='domainuser_1')
        # get max length
        max_length = domainuser_1._meta.get_field('domainuser_name').max_length
        # compare
        self.assertEqual(max_length, 50)
