from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone
from dfirtrack_main.forms import ReportitemForm
from dfirtrack_main.models import Headline, System, Systemstatus

class ReportitemFormTestCase(TestCase):
    """ reportitem form tests """

    @classmethod
    def setUpTestData(cls):

        # create user
        test_user = User.objects.create_user(username='testuser_reportitem', password='6vrj2phUKrw6cjbbtN9V')

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
        Headline.objects.create(headline_name='headline_1')

    def test_reportitem_system_form_label(self):
        """ test form label """

        # get object
        form = ReportitemForm()
        # compare
        self.assertEqual(form.fields['system'].label, 'System (*)')

    def test_reportitem_headline_form_label(self):
        """ test form label """

        # get object
        form = ReportitemForm()
        # compare
        self.assertEqual(form.fields['headline'].label, 'Headline (*)')

    def test_reportitem_subheadline_form_label(self):
        """ test form label """

        # get object
        form = ReportitemForm()
        # compare
        self.assertEqual(form.fields['reportitem_subheadline'].label, 'Subheadline')

    def test_reportitem_note_form_label(self):
        """ test form label """

        # get object
        form = ReportitemForm()
        # compare
        self.assertEqual(form.fields['reportitem_note'].label, 'Note (*)')

    def test_reportitem_form_empty(self):
        """ test minimum form requirements / INVALID """

        # get object
        form = ReportitemForm(data = {})
        # compare
        self.assertFalse(form.is_valid())

    def test_reportitem_note_form_filled(self):
        """ test minimum form requirements / INVALID """

        # get object
        form = ReportitemForm(data = {
            'reportitem_note': 'lorem ipsum',
        })
        # compare
        self.assertFalse(form.is_valid())

    def test_reportitem_system_form_filled(self):
        """ test minimum form requirements / INVALID """

        # get foreign key object id
        system_id = System.objects.get(system_name='system_1').system_id
        # get object
        form = ReportitemForm(data = {
            'reportitem_note': 'lorem ipsum',
            'system': system_id,
        })
        # compare
        self.assertFalse(form.is_valid())

    def test_reportitem_headline_form_filled(self):
        """ test minimum form requirements / VALID """

        # get foreign key object id
        headline_id = Headline.objects.get(headline_name='headline_1').headline_id
        # get foreign key object id
        system_id = System.objects.get(system_name='system_1').system_id
        # get object
        form = ReportitemForm(data = {
            'reportitem_note': 'lorem ipsum',
            'system': system_id,
            'headline': headline_id,
        })
        # compare
        self.assertTrue(form.is_valid())

    def test_reportitem_subheadline_form_filled(self):
        """ test additional form content """

        # get foreign key object id
        headline_id = Headline.objects.get(headline_name='headline_1').headline_id
        # get foreign key object id
        system_id = System.objects.get(system_name='system_1').system_id
        # get object
        form = ReportitemForm(data = {
            'reportitem_note': 'lorem ipsum',
            'system': system_id,
            'headline': headline_id,
            'reportitem_subheadline': 'subheadline_1',
        })
        # compare
        self.assertTrue(form.is_valid())

    def test_reportitem_subheadline_proper_chars(self):
        """ test for max length """

        # get foreign key object id
        headline_id = Headline.objects.get(headline_name='headline_1').headline_id
        # get foreign key object id
        system_id = System.objects.get(system_name='system_1').system_id
        # get object
        form = ReportitemForm(data = {
            'reportitem_note': 'lorem ipsum',
            'system': system_id,
            'headline': headline_id,
            'reportitem_subheadline': 'ssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss',
        })
        # compare
        self.assertTrue(form.is_valid())

    def test_reportitem_subheadline_too_many_chars(self):
        """ test for max length """

        # get foreign key object id
        headline_id = Headline.objects.get(headline_name='headline_1').headline_id
        # get foreign key object id
        system_id = System.objects.get(system_name='system_1').system_id
        # get object
        form = ReportitemForm(data = {
            'reportitem_note': 'lorem ipsum',
            'system': system_id,
            'headline': headline_id,
            'reportitem_subheadline': 'sssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss'
        })
        # compare
        self.assertFalse(form.is_valid())
