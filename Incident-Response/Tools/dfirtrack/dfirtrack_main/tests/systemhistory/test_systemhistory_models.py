from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone
from dfirtrack_main.models import System, Systemhistory, Systemstatus

class SystemhistoryModelTestCase(TestCase):
    """ systemhistory model tests """

    @classmethod
    def setUpTestData(cls):

        # create user
        test_user = User.objects.create_user(username='testuser_systemhistory', password='J8yfJRg6ydiEb5dXVHVZ')

        # create object
        systemstatus_1 = Systemstatus.objects.create(systemstatus_name='systemstatus_1')

        # create object
        system_1 = System.objects.create(
            system_name='system_1',
            systemstatus = systemstatus_1,
            system_modify_time = timezone.now(),
            system_created_by_user_id = test_user,
            system_modified_by_user_id = test_user,
        )

        # create object
        Systemhistory.objects.create(
            system = system_1,
            systemhistory_type='systemhistory_type_1',
            systemhistory_old_value='systemhistory_value_2',
            systemhistory_new_value='systemhistory_value_1',
            systemhistory_time = timezone.now(),
        )

    def test_systemhistory_string(self):
        """ test string representation """

        # get object
        system_1 = System.objects.get(system_name='system_1')
        # get object
        systemhistory_1 = Systemhistory.objects.filter(system=system_1.system_id).order_by('-systemhistory_id')[0]
        # compare
        self.assertEqual(str(systemhistory_1), str(systemhistory_1.systemhistory_id))

    def test_systemhistory_id_attribute_label(self):
        """ test attribute label """

        # get object
        system_1 = System.objects.get(system_name='system_1')
        # get object
        systemhistory_1 = Systemhistory.objects.filter(system=system_1.system_id).order_by('-systemhistory_id')[0]
        # get label
        field_label = systemhistory_1._meta.get_field('systemhistory_id').verbose_name
        # compare
        self.assertEqual(field_label, 'systemhistory id')

    def test_systemhistory_system_attribute_label(self):
        """ test attribute label """

        # get object
        system_1 = System.objects.get(system_name='system_1')
        # get object
        systemhistory_1 = Systemhistory.objects.filter(system=system_1.system_id).order_by('-systemhistory_id')[0]
        # get label
        field_label = systemhistory_1._meta.get_field('system').verbose_name
        # compare
        self.assertEqual(field_label, 'system')

    def test_systemhistory_type_attribute_label(self):
        """ test attribute label """

        # get object
        system_1 = System.objects.get(system_name='system_1')
        # get object
        systemhistory_1 = Systemhistory.objects.filter(system=system_1.system_id).order_by('-systemhistory_id')[0]
        # get label
        field_label = systemhistory_1._meta.get_field('systemhistory_type').verbose_name
        # compare
        self.assertEqual(field_label, 'systemhistory type')

    def test_systemhistory_old_value_attribute_label(self):
        """ test attribute label """

        # get object
        system_1 = System.objects.get(system_name='system_1')
        # get object
        systemhistory_1 = Systemhistory.objects.filter(system=system_1.system_id).order_by('-systemhistory_id')[0]
        # get label
        field_label = systemhistory_1._meta.get_field('systemhistory_old_value').verbose_name
        # compare
        self.assertEqual(field_label, 'systemhistory old value')

    def test_systemhistory_new_value_attribute_label(self):
        """ test attribute label """

        # get object
        system_1 = System.objects.get(system_name='system_1')
        # get object
        systemhistory_1 = Systemhistory.objects.filter(system=system_1.system_id).order_by('-systemhistory_id')[0]
        # get label
        field_label = systemhistory_1._meta.get_field('systemhistory_new_value').verbose_name
        # compare
        self.assertEqual(field_label, 'systemhistory new value')

    def test_systemhistory_time_attribute_label(self):
        """ test attribute label """

        # get object
        system_1 = System.objects.get(system_name='system_1')
        # get object
        systemhistory_1 = Systemhistory.objects.filter(system=system_1.system_id).order_by('-systemhistory_id')[0]
        # get label
        field_label = systemhistory_1._meta.get_field('systemhistory_time').verbose_name
        # compare
        self.assertEqual(field_label, 'systemhistory time')

    def test_systemhistory_type_length(self):
        """ test for max length """

        # get object
        system_1 = System.objects.get(system_name='system_1')
        # get object
        systemhistory_1 = Systemhistory.objects.filter(system=system_1.system_id).order_by('-systemhistory_id')[0]
        # get max length
        max_length = systemhistory_1._meta.get_field('systemhistory_type').max_length
        # compare
        self.assertEqual(max_length, 30)

    def test_systemhistory_old_value_length(self):
        """ test for max length """

        # get object
        system_1 = System.objects.get(system_name='system_1')
        # get object
        systemhistory_1 = Systemhistory.objects.filter(system=system_1.system_id).order_by('-systemhistory_id')[0]
        # get max length
        max_length = systemhistory_1._meta.get_field('systemhistory_old_value').max_length
        # compare
        self.assertEqual(max_length, 30)

    def test_systemhistory_new_value_length(self):
        """ test for max length """

        # get object
        system_1 = System.objects.get(system_name='system_1')
        # get object
        systemhistory_1 = Systemhistory.objects.filter(system=system_1.system_id).order_by('-systemhistory_id')[0]
        # get max length
        max_length = systemhistory_1._meta.get_field('systemhistory_new_value').max_length
        # compare
        self.assertEqual(max_length, 30)
