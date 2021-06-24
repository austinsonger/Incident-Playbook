from django.test import TestCase
from dfirtrack_main.models import Reason

class ReasonModelTestCase(TestCase):
    """ reason model tests """

    @classmethod
    def setUpTestData(cls):

        # create object
        Reason.objects.create(reason_name='reason_1')

    def test_reason_string(self):
        """ test string representation """

        # get object
        reason_1 = Reason.objects.get(reason_name='reason_1')
        # compare
        self.assertEqual(str(reason_1), 'reason_1')

    def test_reason_id_attribute_label(self):
        """ test attribute label """

        # get object
        reason_1 = Reason.objects.get(reason_name='reason_1')
        # get label
        field_label = reason_1._meta.get_field('reason_id').verbose_name
        # compare
        self.assertEqual(field_label, 'reason id')

    def test_reason_name_attribute_label(self):
        """ test attribute label """

        # get object
        reason_1 = Reason.objects.get(reason_name='reason_1')
        # get label
        field_label = reason_1._meta.get_field('reason_name').verbose_name
        # compare
        self.assertEqual(field_label, 'reason name')

    def test_reason_note_attribute_label(self):
        """ test attribute label """

        # get object
        reason_1 = Reason.objects.get(reason_name='reason_1')
        # get label
        field_label = reason_1._meta.get_field('reason_note').verbose_name
        # compare
        self.assertEqual(field_label, 'reason note')

    def test_reason_name_length(self):
        """ test for max length """

        # get object
        reason_1 = Reason.objects.get(reason_name='reason_1')
        # get max length
        max_length = reason_1._meta.get_field('reason_name').max_length
        # compare
        self.assertEqual(max_length, 30)
