from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone
from dfirtrack_main.models import Analysisstatus, System, Systemhistory, Systemstatus

class SystemhistoryModelTestCase(TestCase):
    """ systemhistory model tests """

    @classmethod
    def setUpTestData(cls):

        # create user
        test_user = User.objects.create_user(username='testuser_systemhistory', password='CE3IxsFuIVqOmj6pFqsU')

        # create objects
        systemstatus_1 = Systemstatus.objects.create(systemstatus_name='systemstatus_1')
        Systemstatus.objects.create(systemstatus_name='systemstatus_2')

        # create objects
        analysisstatus_1 = Analysisstatus.objects.create(analysisstatus_name='analysisstatus_1')
        Analysisstatus.objects.create(analysisstatus_name='analysisstatus_2')

        # create object
        System.objects.create(
            system_name='system_1',
            analysisstatus = analysisstatus_1,
            systemstatus = systemstatus_1,
            system_modify_time = timezone.now(),
            system_created_by_user_id = test_user,
            system_modified_by_user_id = test_user,
        )

    def test_systemhistory_systemstatus_update(self):
        """ test systemhistory systemstatus """

        # get object
        system_1 = System.objects.get(system_name='system_1')
        # get object
        systemstatus_2 = Systemstatus.objects.get(systemstatus_name='systemstatus_2')
        # change systemstatus
        system_1.systemstatus = systemstatus_2
        # execute save method
        system_1.save()
        # get last systemhistory entry
        systemhistory_1 = Systemhistory.objects.filter(system=system_1.system_id).order_by('-systemhistory_id')[0]
        # compare
        self.assertEqual(str(systemhistory_1.systemhistory_type), 'Systemstatus')
        self.assertEqual(str(systemhistory_1.systemhistory_old_value), 'systemstatus_1')
        self.assertEqual(str(systemhistory_1.systemhistory_new_value), 'systemstatus_2')

    def test_systemhistory_analysisstatus_update(self):
        """ test systemhistory analysisstatus """

        # get object
        system_1 = System.objects.get(system_name='system_1')
        # get object
        analysisstatus_2 = Analysisstatus.objects.get(analysisstatus_name='analysisstatus_2')
        # change analysisstatus
        system_1.analysisstatus = analysisstatus_2
        # execute save method
        system_1.save()
        # get last systemhistory entry
        systemhistory_1 = Systemhistory.objects.filter(system=system_1.system_id).order_by('-systemhistory_id')[0]
        # compare
        self.assertEqual(str(systemhistory_1.systemhistory_type), 'Analysisstatus')
        self.assertEqual(str(systemhistory_1.systemhistory_old_value), 'analysisstatus_1')
        self.assertEqual(str(systemhistory_1.systemhistory_new_value), 'analysisstatus_2')

    def test_systemhistory_analysisstatus_clear(self):
        """ test systemhistory analysisstatus """

        # get object
        system_1 = System.objects.get(system_name='system_1')
        # clear analysisstatus
        system_1.analysisstatus = None
        # execute save method
        system_1.save()
        # get last systemhistory entry
        systemhistory_1 = Systemhistory.objects.filter(system=system_1.system_id).order_by('-systemhistory_id')[0]
        # compare
        self.assertEqual(str(systemhistory_1.systemhistory_type), 'Analysisstatus')
        self.assertEqual(str(systemhistory_1.systemhistory_old_value), 'analysisstatus_1')
        self.assertEqual(str(systemhistory_1.systemhistory_new_value), 'No analysisstatus')
