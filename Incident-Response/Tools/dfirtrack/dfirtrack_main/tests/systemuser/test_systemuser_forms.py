from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone
from dfirtrack_main.forms import SystemuserForm
from dfirtrack_main.models import System, Systemstatus

class SystemuserFormTestCase(TestCase):
    """ systemuser form tests """

    @classmethod
    def setUpTestData(cls):

        # create user
        test_user = User.objects.create_user(username='testuser_systemuser', password='u6YexpBiCjk1fdx68uHY')

        # create object
        systemstatus_1 = Systemstatus.objects.create(systemstatus_name='systemstatus_1')

        # create object
        System.objects.create(
            system_name='system_1',
            systemstatus = systemstatus_1,
            system_modify_time = timezone.now(),
            system_created_by_user_id = test_user,
            system_modified_by_user_id = test_user,
        )

    def test_systemuser_name_form_label(self):
        """ test form label """

        # get object
        form = SystemuserForm()
        # compare
        self.assertEqual(form.fields['systemuser_name'].label, 'Systemuser name (*)')

    def test_systemuser_lastlogon_time_form_label(self):
        """ test form label """

        # get object
        form = SystemuserForm()
        # compare
        self.assertEqual(form.fields['systemuser_lastlogon_time'].label, 'Last logon time (YYYY-MM-DD HH:MM:SS)')

    def test_systemuser_is_systemadmin_form_label(self):
        """ test form label """

        # get object
        form = SystemuserForm()
        # compare
        self.assertEqual(form.fields['systemuser_is_systemadmin'].label, 'Systemuser is systemadmin')

    def test_systemuser_system_form_label(self):
        """ test form label """

        # get object
        form = SystemuserForm()
        # compare
        self.assertEqual(form.fields['system'].label, 'System (*)')

    def test_systemuser_form_empty(self):
        """ test minimum form requirements / INVALID """

        # get object
        form = SystemuserForm(data = {})
        # compare
        self.assertFalse(form.is_valid())

    def test_systemuser_name_form_filled(self):
        """ test minimum form requirements / INVALID """

        # get object
        form = SystemuserForm(data = {'systemuser_name': 'systemuser_1'})
        # compare
        self.assertFalse(form.is_valid())

    def test_systemuser_system_form_filled(self):
        """ test minimum form requirements / VALID """

        # get foreign key object id
        system_id = System.objects.get(system_name='system_1').system_id
        # get object
        form = SystemuserForm(data = {
            'systemuser_name': 'systemuser_1',
            'system': system_id,
        })
        # compare
        self.assertTrue(form.is_valid())

    def test_systemuser_lastlogon_time_form_filled(self):
        """ test additional form content """

        # get foreign key object id
        system_id = System.objects.get(system_name='system_1').system_id
        # get object
        form = SystemuserForm(data = {
            'systemuser_name': 'systemuser_1',
            'system': system_id,
            'systemuser_lastlogon_time': timezone.now(),
        })
        # compare
        self.assertTrue(form.is_valid())

    def test_systemuser_name_proper_chars(self):
        """ test for max length """

        # get foreign key object id
        system_id = System.objects.get(system_name='system_1').system_id
        # get object
        form = SystemuserForm(data = {
            'systemuser_name': 'ssssssssssssssssssssssssssssssssssssssssssssssssss',
            'system': system_id,
        })
        # compare
        self.assertTrue(form.is_valid())

    def test_systemuser_name_too_many_chars(self):
        """ test for max length """

        # get foreign key object id
        system_id = System.objects.get(system_name='system_1').system_id
        # get object
        form = SystemuserForm(data = {
            'systemuser_name': 'sssssssssssssssssssssssssssssssssssssssssssssssssss',
            'system': system_id,
        })
        # compare
        self.assertFalse(form.is_valid())

    def test_systemuser_lastlogon_formatcheck(self):
        """ test input format """

        # get foreign key object id
        system_id = System.objects.get(system_name='system_1').system_id
        # get object
        form = SystemuserForm(data = {
            'systemuser_name': 'systemuser_1',
            'system': system_id,
            'systemuser_lastlogon_time': 'wrong format',
        })
        # compare
        self.assertFalse(form.is_valid())
