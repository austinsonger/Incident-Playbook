from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone
from dfirtrack_main.forms import AnalystmemoForm
from dfirtrack_main.models import System, Systemstatus

class AnalystmemoFormTestCase(TestCase):
    """ analystmemo form tests """

    @classmethod
    def setUpTestData(cls):

        # create user
        test_user = User.objects.create_user(username='testuser_analystmemo', password='i9gekSgVmDKQN7c5dj5p')

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

    def test_analystmemo_note_form_label(self):
        """ test form label """

        # get object
        form = AnalystmemoForm()
        # compare
        self.assertEqual(form.fields['analystmemo_note'].label, 'Analystmemo note (*)')

    def test_analystmemo_system_form_label(self):
        """ test form label """

        # get object
        form = AnalystmemoForm()
        # compare
        self.assertEqual(form.fields['system'].label, 'System (*)')

    def test_analystmemo_form_empty(self):
        """ test minimum form requirements / INVALID """

        # get object
        form = AnalystmemoForm(data = {})
        # compare
        self.assertFalse(form.is_valid())

    def test_analystmemo_note_form_filled(self):
        """ test minimum form requirements / INVALID """

        # get object
        form = AnalystmemoForm(data = {'analystmemo_note': 'lorem ipsum'})
        # compare
        self.assertFalse(form.is_valid())

    def test_analystmemo_system_form_filled(self):
        """ test minimum form requirements / VALID """

        # get foreign key object id
        system_id = System.objects.get(system_name='system_1').system_id
        # get object
        form = AnalystmemoForm(data = {
            'analystmemo_note': 'lorem ipsum',
            'system': system_id,
        })
        # compare
        self.assertTrue(form.is_valid())
