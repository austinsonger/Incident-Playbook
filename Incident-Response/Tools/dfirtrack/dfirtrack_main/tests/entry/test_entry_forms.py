from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone
from dfirtrack_main.forms import EntryForm
from dfirtrack_main.models import Case, System, Systemstatus

class EntryFormTestCase(TestCase):
    """ entry form tests """

    @classmethod
    def setUpTestData(cls):

        # create user
        test_user = User.objects.create_user(username='testuser_entry', password='z2B7MofdZ4suAn6AYGSo')

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

        # create object
        Case.objects.create(
            case_name = 'case_1',
            case_is_incident = True,
            case_created_by_user_id = test_user,
        )

    def test_entry_time_form_label(self):
        """ test form label """

        # get object
        form = EntryForm()
        # compare
        self.assertEqual(form.fields['entry_time'].label, 'Entry time (for sorting) (YYYY-MM-DD HH:MM:SS) (*)')

    def test_system_form_label(self):
        """ test form label """

        # get object
        form = EntryForm()
        # compare
        self.assertEqual(form.fields['system'].label, 'System (*)')

    def test_entry_sha1_form_label(self):
        """ test form label """

        # get object
        form = EntryForm()
        # compare
        self.assertEqual(form.fields['entry_sha1'].label, 'Entry sha1')

    def test_entry_date_form_label(self):
        """ test form label """

        # get object
        form = EntryForm()
        # compare
        self.assertEqual(form.fields['entry_date'].label, 'Entry date (YYYY-MM-DD)')

    def test_entry_utc_form_label(self):
        """ test form label """

        # get object
        form = EntryForm()
        # compare
        self.assertEqual(form.fields['entry_utc'].label, 'Entry time (for report) (HH:MM:SS)')

    def test_entry_system_form_label(self):
        """ test form label """

        # get object
        form = EntryForm()
        # compare
        self.assertEqual(form.fields['entry_system'].label, 'Entry system (for report)')

    def test_entry_type_form_label(self):
        """ test form label """

        # get object
        form = EntryForm()
        # compare
        self.assertEqual(form.fields['entry_type'].label, 'Entry type')

    def test_entry_content_form_label(self):
        """ test form label """

        # get object
        form = EntryForm()
        # compare
        self.assertEqual(form.fields['entry_content'].label, 'Entry content')

    def test_entry_note_form_label(self):
        """ test form label """

        # get object
        form = EntryForm()
        # compare
        self.assertEqual(form.fields['entry_note'].label, 'Entry note')

    def test_case_form_label(self):
        """ test form label """

        # get object
        form = EntryForm()
        # compare
        self.assertEqual(form.fields['case'].label, 'Case')

    def test_entry_form_empty(self):
        """ test minimum form requirements / INVALID """

        # get object
        form = EntryForm(data = {})
        # compare
        self.assertFalse(form.is_valid())

    def test_entry_time_form_filled(self):
        """ test minimum form requirements / INVALID """

        # get object
        form = EntryForm(data = {
            'entry_time': '2001-02-03 12:34:56',
        })
        # compare
        self.assertFalse(form.is_valid())

    def test_system_form_filled(self):
        """ test minimum form requirements / VALID """

        # get foreign key object id
        system_id = System.objects.get(system_name='system_1').system_id
        # get object
        form = EntryForm(data = {
            'entry_time': '2009-08-07 12:34:56',
            'system': system_id,
        })
        # compare
        self.assertTrue(form.is_valid())

    def test_entry_sha1_form_filled(self):
        """ test additional form content """

        # get foreign key object id
        system_id = System.objects.get(system_name='system_1').system_id
        # get object
        form = EntryForm(data = {
            'entry_time': '2009-08-07 12:34:56',
            'system': system_id,
            'entry_sha1': 'da39a3ee5e6b4b0d3255bfef95601890afd80709',
        })
        # compare
        self.assertTrue(form.is_valid())

    def test_entry_date_form_filled(self):
        """ test additional form content """

        # get foreign key object id
        system_id = System.objects.get(system_name='system_1').system_id
        # get object
        form = EntryForm(data = {
            'entry_time': '2009-08-07 12:34:56',
            'system': system_id,
            'entry_date': '2009-08-07',
        })
        # compare
        self.assertTrue(form.is_valid())

    def test_entry_utc_form_filled(self):
        """ test additional form content """

        # get foreign key object id
        system_id = System.objects.get(system_name='system_1').system_id
        # get object
        form = EntryForm(data = {
            'entry_time': '2009-08-07 12:34:56',
            'system': system_id,
            'entry_utc': '12:34:56',
        })
        # compare
        self.assertTrue(form.is_valid())

    def test_entry_system_form_filled(self):
        """ test additional form content """

        # get foreign key object id
        system_id = System.objects.get(system_name='system_1').system_id
        # get object
        form = EntryForm(data = {
            'entry_time': '2009-08-07 12:34:56',
            'system': system_id,
            'entry_system': 'system_1',
        })
        # compare
        self.assertTrue(form.is_valid())

    def test_entry_type_form_filled(self):
        """ test additional form content """

        # get foreign key object id
        system_id = System.objects.get(system_name='system_1').system_id
        # get object
        form = EntryForm(data = {
            'entry_time': '2009-08-07 12:34:56',
            'system': system_id,
            'entry_type': 'type_1',
        })
        # compare
        self.assertTrue(form.is_valid())

    def test_entry_content_form_filled(self):
        """ test additional form content """

        # get foreign key object id
        system_id = System.objects.get(system_name='system_1').system_id
        # get object
        form = EntryForm(data = {
            'entry_time': '2009-08-07 12:34:56',
            'system': system_id,
            'entry_content': 'lorem ipsum',
        })
        # compare
        self.assertTrue(form.is_valid())

    def test_entry_note_form_filled(self):
        """ test additional form content """

        # get foreign key object id
        system_id = System.objects.get(system_name='system_1').system_id
        # get object
        form = EntryForm(data = {
            'entry_time': '2009-08-07 12:34:56',
            'system': system_id,
            'entry_note': 'lorem ipsum',
        })
        # compare
        self.assertTrue(form.is_valid())

    def test_entry_case_form_filled(self):
        """ test additional form content """

        # get foreign key object id
        case_id = Case.objects.get(case_name='case_1').case_id
        # get foreign key object id
        system_id = System.objects.get(system_name='system_1').system_id
        # get object
        form = EntryForm(data = {
            'entry_time': '2009-08-07 12:34:56',
            'system': system_id,
            'case': case_id,
        })
        # compare
        self.assertTrue(form.is_valid())

    def test_entry_sha1_proper_chars(self):
        """ test for max length """

        # define datetime string
        entry_time_string = '2009-08-07 12:34:56'
        # get foreign key object id
        system_id = System.objects.get(system_name='system_1').system_id
        # get object
        form = EntryForm(data = {
            'entry_time': entry_time_string,
            'system': system_id,
            'entry_sha1': 'ssssssssssssssssssssssssssssssssssssssss',
        })
        # compare
        self.assertTrue(form.is_valid())

    def test_entry_sha1_too_many_chars(self):
        """ test for max length """

        # define datetime string
        entry_time_string = '2009-08-07 12:34:56'
        # get foreign key object id
        system_id = System.objects.get(system_name='system_1').system_id
        # get object
        form = EntryForm(data = {
            'entry_time': entry_time_string,
            'system': system_id,
            'entry_sha1': 'sssssssssssssssssssssssssssssssssssssssss',
        })
        # compare
        self.assertFalse(form.is_valid())

    def test_entry_date_proper_chars(self):
        """ test for max length """

        # define datetime string
        entry_time_string = '2009-08-07 12:34:56'
        # get foreign key object id
        system_id = System.objects.get(system_name='system_1').system_id
        # get object
        form = EntryForm(data = {
            'entry_time': entry_time_string,
            'system': system_id,
            'entry_date': 'dddddddddd',
        })
        # compare
        self.assertTrue(form.is_valid())

    def test_entry_date_too_many_chars(self):
        """ test for max length """

        # define datetime string
        entry_time_string = '2009-08-07 12:34:56'
        # get foreign key object id
        system_id = System.objects.get(system_name='system_1').system_id
        # get object
        form = EntryForm(data = {
            'entry_time': entry_time_string,
            'system': system_id,
            'entry_date': 'ddddddddddd',
        })
        # compare
        self.assertFalse(form.is_valid())

    def test_entry_utc_proper_chars(self):
        """ test for max length """

        # define datetime string
        entry_time_string = '2009-08-07 12:34:56'
        # get foreign key object id
        system_id = System.objects.get(system_name='system_1').system_id
        # get object
        form = EntryForm(data = {
            'entry_time': entry_time_string,
            'system': system_id,
            'entry_utc': 'uuuuuuuu',
        })
        # compare
        self.assertTrue(form.is_valid())

    def test_entry_utc_too_many_chars(self):
        """ test for max length """

        # define datetime string
        entry_time_string = '2009-08-07 12:34:56'
        # get foreign key object id
        system_id = System.objects.get(system_name='system_1').system_id
        # get object
        form = EntryForm(data = {
            'entry_time': entry_time_string,
            'system': system_id,
            'entry_utc': 'uuuuuuuuu',
        })
        # compare
        self.assertFalse(form.is_valid())

    def test_entry_system_proper_chars(self):
        """ test for max length """

        # define datetime string
        entry_time_string = '2009-08-07 12:34:56'
        # get foreign key object id
        system_id = System.objects.get(system_name='system_1').system_id
        # get object
        form = EntryForm(data = {
            'entry_time': entry_time_string,
            'system': system_id,
            'entry_system': 'ssssssssssssssssssssssssssssss',
        })
        # compare
        self.assertTrue(form.is_valid())

    def test_entry_system_too_many_chars(self):
        """ test for max length """

        # define datetime string
        entry_time_string = '2009-08-07 12:34:56'
        # get foreign key object id
        system_id = System.objects.get(system_name='system_1').system_id
        # get object
        form = EntryForm(data = {
            'entry_time': entry_time_string,
            'system': system_id,
            'entry_system': 'sssssssssssssssssssssssssssssss',
        })
        # compare
        self.assertFalse(form.is_valid())

    def test_entry_type_proper_chars(self):
        """ test for max length """

        # define datetime string
        entry_time_string = '2009-08-07 12:34:56'
        # get foreign key object id
        system_id = System.objects.get(system_name='system_1').system_id
        # get object
        form = EntryForm(data = {
            'entry_time': entry_time_string,
            'system': system_id,
            'entry_type': 'tttttttttttttttttttttttttttttt',
        })
        # compare
        self.assertTrue(form.is_valid())

    def test_entry_type_too_many_chars(self):
        """ test for max length """

        # define datetime string
        entry_time_string = '2009-08-07 12:34:56'
        # get foreign key object id
        system_id = System.objects.get(system_name='system_1').system_id
        # get object
        form = EntryForm(data = {
            'entry_time': entry_time_string,
            'system': system_id,
            'entry_type': 'ttttttttttttttttttttttttttttttt',
        })
        # compare
        self.assertFalse(form.is_valid())
