from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone
from dfirtrack_main.models import Analysisstatus, System, Systemstatus

class SystemStatusUpdateModelTestCase(TestCase):
    """ system status update model tests """

    @classmethod
    def setUpTestData(cls):

        # create user
        test_user = User.objects.create_user(username='testuser_system_status_update', password='f8j9lbHVduc5MTw4gqbz')

        # create objects
        systemstatus_1 = Systemstatus.objects.create(systemstatus_name='systemstatus_1')
        Systemstatus.objects.create(systemstatus_name='systemstatus_2')

        # create objects
        analysisstatus_1 = Analysisstatus.objects.create(analysisstatus_name='analysisstatus_1')
        Analysisstatus.objects.create(analysisstatus_name='analysisstatus_2')

        # create object
        System.objects.create(
            system_name='system_1',
            systemstatus = systemstatus_1,
            system_modify_time = timezone.now(),
            system_created_by_user_id = test_user,
            system_modified_by_user_id = test_user,
        )

        # create object
        System.objects.create(
            system_name='system_2',
            analysisstatus = analysisstatus_1,
            systemstatus = systemstatus_1,
            system_modify_time = timezone.now(),
            system_created_by_user_id = test_user,
            system_modified_by_user_id = test_user,
        )

    def test_system_systemstatus_initial(self):
        """ test update status """

        # get object
        system_1 = System.objects.get(system_name='system_1')
        # compare
        self.assertEqual(str(system_1.previous_systemstatus), 'systemstatus_1')

    def test_system_systemstatus_update(self):
        """ test update status """

        # get object
        system_1 = System.objects.get(system_name='system_1')
        # get object
        systemstatus_2 = Systemstatus.objects.get(systemstatus_name='systemstatus_2')
        # change systemstatus
        system_1.systemstatus = systemstatus_2
        # execute save method
        system_1.save()
        # compare
        self.assertEqual(str(system_1.previous_systemstatus), 'systemstatus_2')

    def test_system_analysisstatus_initial_empty(self):
        """ test update status """

        # get object
        system_1 = System.objects.get(system_name='system_1')
        # compare
        self.assertEqual(str(system_1.previous_analysisstatus), 'None')

    def test_system_analysisstatus_initial_filled(self):
        """ test update status """

        # get object
        system_2 = System.objects.get(system_name='system_2')
        # compare
        self.assertEqual(str(system_2.previous_analysisstatus), 'analysisstatus_1')

    def test_system_analysisstatus_update(self):
        """ test update status """

        # get object
        system_2 = System.objects.get(system_name='system_2')
        # get object
        analysisstatus_2 = Analysisstatus.objects.get(analysisstatus_name='analysisstatus_2')
        # change analysisstatus
        system_2.analysisstatus = analysisstatus_2
        # execute save method
        system_2.save()
        # compare
        self.assertEqual(str(system_2.previous_analysisstatus), 'analysisstatus_2')

    def test_system_analysisstatus_clear(self):
        """ test update status """

        # get object
        system_2 = System.objects.get(system_name='system_2')
        # clear analysisstatus
        system_2.analysisstatus = None
        # execute save method
        system_2.save()
        # compare
        self.assertEqual(str(system_2.previous_analysisstatus), 'None')
