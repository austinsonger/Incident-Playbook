from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone
from dfirtrack_main.models import Headline, Reportitem, System, Systemstatus

class ReportitemModelTestCase(TestCase):
    """ reportitem model tests """

    @classmethod
    def setUpTestData(cls):

        # create user
        test_user = User.objects.create_user(username='testuser_reportitem', password='n26RCEzVtmtmpAHa5g1M')

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
        headline_1 = Headline.objects.create(headline_name='headline_1')

        # create object
        Reportitem.objects.create(
            reportitem_note='lorem ipsum',
            system = system_1,
            headline = headline_1,
            reportitem_created_by_user_id = test_user,
            reportitem_modified_by_user_id = test_user,
        )

    def test_reportitem_string(self):
        """ test string representation """

        # get object
        reportitem_1 = Reportitem.objects.get(reportitem_note='lorem ipsum')
        # compare
        self.assertEqual(str(reportitem_1), str(reportitem_1.system) + ' | ' + str(reportitem_1.headline.headline_name) + ' | ' + str(reportitem_1.reportitem_subheadline))

    def test_reportitem_id_attribute_label(self):
        """ test attribute label """

        # get object
        reportitem_1 = Reportitem.objects.get(reportitem_note='lorem ipsum')
        # get label
        field_label = reportitem_1._meta.get_field('reportitem_id').verbose_name
        # compare
        self.assertEqual(field_label, 'reportitem id')

    def test_reportitem_system_attribute_label(self):
        """ test attribute label """

        # get object
        reportitem_1 = Reportitem.objects.get(reportitem_note='lorem ipsum')
        # get label
        field_label = reportitem_1._meta.get_field('system').verbose_name
        # compare
        self.assertEqual(field_label, 'system')

    def test_reportitem_headline_attribute_label(self):
        """ test attribute label """

        # get object
        reportitem_1 = Reportitem.objects.get(reportitem_note='lorem ipsum')
        # get label
        field_label = reportitem_1._meta.get_field('headline').verbose_name
        # compare
        self.assertEqual(field_label, 'headline')

    def test_reportitem_subheadline_attribute_label(self):
        """ test attribute label """

        # get object
        reportitem_1 = Reportitem.objects.get(reportitem_note='lorem ipsum')
        # get label
        field_label = reportitem_1._meta.get_field('reportitem_subheadline').verbose_name
        # compare
        self.assertEqual(field_label, 'reportitem subheadline')

    def test_reportitem_note_attribute_label(self):
        """ test attribute label """

        # get object
        reportitem_1 = Reportitem.objects.get(reportitem_note='lorem ipsum')
        # get label
        field_label = reportitem_1._meta.get_field('reportitem_note').verbose_name
        # compare
        self.assertEqual(field_label, 'reportitem note')

    def test_reportitem_create_time_attribute_label(self):
        """ test attribute label """

        # get object
        reportitem_1 = Reportitem.objects.get(reportitem_note='lorem ipsum')
        # get label
        field_label = reportitem_1._meta.get_field('reportitem_create_time').verbose_name
        # compare
        self.assertEqual(field_label, 'reportitem create time')

    def test_reportitem_modify_time_attribute_label(self):
        """ test attribute label """

        # get object
        reportitem_1 = Reportitem.objects.get(reportitem_note='lorem ipsum')
        # get label
        field_label = reportitem_1._meta.get_field('reportitem_modify_time').verbose_name
        # compare
        self.assertEqual(field_label, 'reportitem modify time')

    def test_reportitem_created_by_user_id_attribute_label(self):
        """ test attribute label """

        # get object
        reportitem_1 = Reportitem.objects.get(reportitem_note='lorem ipsum')
        # get label
        field_label = reportitem_1._meta.get_field('reportitem_created_by_user_id').verbose_name
        # compare
        self.assertEqual(field_label, 'reportitem created by user id')

    def test_reportitem_modified_by_user_id_attribute_label(self):
        """ test attribute label """

        # get object
        reportitem_1 = Reportitem.objects.get(reportitem_note='lorem ipsum')
        # get label
        field_label = reportitem_1._meta.get_field('reportitem_modified_by_user_id').verbose_name
        # compare
        self.assertEqual(field_label, 'reportitem modified by user id')

    def test_reportitem_subheadline_length(self):
        """ test for max length """

        # get object
        reportitem_1 = Reportitem.objects.get(reportitem_note='lorem ipsum')
        # get max length
        max_length = reportitem_1._meta.get_field('reportitem_subheadline').max_length
        # compare
        self.assertEqual(max_length, 100)
