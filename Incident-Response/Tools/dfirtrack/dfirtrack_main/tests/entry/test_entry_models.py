from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone
from dfirtrack_main.models import Entry, System, Systemstatus

class EntryModelTestCase(TestCase):
    """ entry model tests """

    @classmethod
    def setUpTestData(cls):

        # create user
        test_user = User.objects.create_user(username='testuser_entry', password='zmBpopGk6Z6mkbH3Qu43')

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
        Entry.objects.create(
            system = system_1,
            entry_time = timezone.now(),
            entry_sha1 = 'da39a3ee5e6b4b0d3255bfef95601890afd80709',
            entry_created_by_user_id = test_user,
            entry_modified_by_user_id = test_user,
        )

    def test_entry_string(self):
        """ test string representation """

        # get object
        entry_1 = Entry.objects.get(entry_sha1='da39a3ee5e6b4b0d3255bfef95601890afd80709')
        # get object id
        entry_id = entry_1.entry_id
        # compare
        self.assertEqual(str(entry_1), str(entry_id) + ' | ' + str(entry_1.system) + ' | ' + 'da39a3ee5e6b4b0d3255bfef95601890afd80709')

    def test_entry_id_attribute_label(self):
        """ test attribute label """

        # get object
        entry_1 = Entry.objects.get(entry_sha1='da39a3ee5e6b4b0d3255bfef95601890afd80709')
        # get label
        field_label = entry_1._meta.get_field('entry_id').verbose_name
        # compare
        self.assertEqual(field_label, 'entry id')

    def test_system_attribute_label(self):
        """ test attribute label """

        # get object
        entry_1 = Entry.objects.get(entry_sha1='da39a3ee5e6b4b0d3255bfef95601890afd80709')
        # get label
        field_label = entry_1._meta.get_field('system').verbose_name
        # compare
        self.assertEqual(field_label, 'system')

    def test_entry_case_attribute_label(self):
        """ test attribute label """

        # get object
        entry_1 = Entry.objects.get(entry_sha1='da39a3ee5e6b4b0d3255bfef95601890afd80709')
        # get label
        field_label = entry_1._meta.get_field('case').verbose_name
        # compare
        self.assertEqual(field_label, 'case')

    def test_entry_time_attribute_label(self):
        """ test attribute label """

        # get object
        entry_1 = Entry.objects.get(entry_sha1='da39a3ee5e6b4b0d3255bfef95601890afd80709')
        # get label
        field_label = entry_1._meta.get_field('entry_time').verbose_name
        # compare
        self.assertEqual(field_label, 'entry time')

    def test_entry_sha1_attribute_label(self):
        """ test attribute label """

        # get object
        entry_1 = Entry.objects.get(entry_sha1='da39a3ee5e6b4b0d3255bfef95601890afd80709')
        # get label
        field_label = entry_1._meta.get_field('entry_sha1').verbose_name
        # compare
        self.assertEqual(field_label, 'entry sha1')

    def test_entry_date_attribute_label(self):
        """ test attribute label """

        # get object
        entry_1 = Entry.objects.get(entry_sha1='da39a3ee5e6b4b0d3255bfef95601890afd80709')
        # get label
        field_label = entry_1._meta.get_field('entry_date').verbose_name
        # compare
        self.assertEqual(field_label, 'entry date')

    def test_entry_utc_attribute_label(self):
        """ test attribute label """

        # get object
        entry_1 = Entry.objects.get(entry_sha1='da39a3ee5e6b4b0d3255bfef95601890afd80709')
        # get label
        field_label = entry_1._meta.get_field('entry_utc').verbose_name
        # compare
        self.assertEqual(field_label, 'entry utc')

    def test_entry_system_attribute_label(self):
        """ test attribute label """

        # get object
        entry_1 = Entry.objects.get(entry_sha1='da39a3ee5e6b4b0d3255bfef95601890afd80709')
        # get label
        field_label = entry_1._meta.get_field('entry_system').verbose_name
        # compare
        self.assertEqual(field_label, 'entry system')

    def test_entry_type_attribute_label(self):
        """ test attribute label """

        # get object
        entry_1 = Entry.objects.get(entry_sha1='da39a3ee5e6b4b0d3255bfef95601890afd80709')
        # get label
        field_label = entry_1._meta.get_field('entry_type').verbose_name
        # compare
        self.assertEqual(field_label, 'entry type')

    def test_entry_content_attribute_label(self):
        """ test attribute label """

        # get object
        entry_1 = Entry.objects.get(entry_sha1='da39a3ee5e6b4b0d3255bfef95601890afd80709')
        # get label
        field_label = entry_1._meta.get_field('entry_content').verbose_name
        # compare
        self.assertEqual(field_label, 'entry content')

    def test_entry_note_attribute_label(self):
        """ test attribute label """

        # get object
        entry_1 = Entry.objects.get(entry_sha1='da39a3ee5e6b4b0d3255bfef95601890afd80709')
        # get label
        field_label = entry_1._meta.get_field('entry_note').verbose_name
        # compare
        self.assertEqual(field_label, 'entry note')

    def test_entry_create_time_attribute_label(self):
        """ test attribute label """

        # get object
        entry_1 = Entry.objects.get(entry_sha1='da39a3ee5e6b4b0d3255bfef95601890afd80709')
        # get label
        field_label = entry_1._meta.get_field('entry_create_time').verbose_name
        # compare
        self.assertEqual(field_label, 'entry create time')

    def test_entry_modify_time_attribute_label(self):
        """ test attribute label """

        # get object
        entry_1 = Entry.objects.get(entry_sha1='da39a3ee5e6b4b0d3255bfef95601890afd80709')
        # get label
        field_label = entry_1._meta.get_field('entry_modify_time').verbose_name
        # compare
        self.assertEqual(field_label, 'entry modify time')

    def test_entry_api_time_attribute_label(self):
        """ test attribute label """

        # get object
        entry_1 = Entry.objects.get(entry_sha1='da39a3ee5e6b4b0d3255bfef95601890afd80709')
        # get label
        field_label = entry_1._meta.get_field('entry_api_time').verbose_name
        # compare
        self.assertEqual(field_label, 'entry api time')

    def test_entry_created_by_user_id_attribute_label(self):
        """ test attribute label """

        # get object
        entry_1 = Entry.objects.get(entry_sha1='da39a3ee5e6b4b0d3255bfef95601890afd80709')
        # get label
        field_label = entry_1._meta.get_field('entry_created_by_user_id').verbose_name
        # compare
        self.assertEqual(field_label, 'entry created by user id')

    def test_entry_modified_by_user_id_attribute_label(self):
        """ test attribute label """

        # get object
        entry_1 = Entry.objects.get(entry_sha1='da39a3ee5e6b4b0d3255bfef95601890afd80709')
        # get label
        field_label = entry_1._meta.get_field('entry_modified_by_user_id').verbose_name
        # compare
        self.assertEqual(field_label, 'entry modified by user id')

    def test_entry_sha1_length(self):
        """ test for max length """

        # get object
        entry_1 = Entry.objects.get(entry_sha1='da39a3ee5e6b4b0d3255bfef95601890afd80709')
        # get max length
        max_length = entry_1._meta.get_field('entry_sha1').max_length
        # compare
        self.assertEqual(max_length, 40)

    def test_entry_date_length(self):
        """ test for max length """

        # get object
        entry_1 = Entry.objects.get(entry_sha1='da39a3ee5e6b4b0d3255bfef95601890afd80709')
        # get max length
        max_length = entry_1._meta.get_field('entry_date').max_length
        # compare
        self.assertEqual(max_length, 10)

    def test_entry_utc_length(self):
        """ test for max length """

        # get object
        entry_1 = Entry.objects.get(entry_sha1='da39a3ee5e6b4b0d3255bfef95601890afd80709')
        # get max length
        max_length = entry_1._meta.get_field('entry_utc').max_length
        # compare
        self.assertEqual(max_length, 8)

    def test_entry_system_length(self):
        """ test for max length """

        # get object
        entry_1 = Entry.objects.get(entry_sha1='da39a3ee5e6b4b0d3255bfef95601890afd80709')
        # get max length
        max_length = entry_1._meta.get_field('entry_system').max_length
        # compare
        self.assertEqual(max_length, 30)

    def test_entry_type_length(self):
        """ test for max length """

        # get object
        entry_1 = Entry.objects.get(entry_sha1='da39a3ee5e6b4b0d3255bfef95601890afd80709')
        # get max length
        max_length = entry_1._meta.get_field('entry_type').max_length
        # compare
        self.assertEqual(max_length, 30)
