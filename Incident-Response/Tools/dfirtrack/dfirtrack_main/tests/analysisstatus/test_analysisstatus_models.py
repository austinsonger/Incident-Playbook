from django.test import TestCase
from dfirtrack_main.models import Analysisstatus

class AnalysisstatusModelTestCase(TestCase):
    """ analysisstatus model tests """

    @classmethod
    def setUpTestData(cls):

        # create object
        Analysisstatus.objects.create(analysisstatus_name='analysisstatus_1')

    def test_analysisstatus_string(self):
        """ test string representation """

        # get object
        analysisstatus_1 = Analysisstatus.objects.get(analysisstatus_name='analysisstatus_1')
        # compare
        self.assertEqual(str(analysisstatus_1), 'analysisstatus_1')

    def test_analysisstatus_id_attribute_label(self):
        """ test attribute label """

        # get object
        analysisstatus_1 = Analysisstatus.objects.get(analysisstatus_name='analysisstatus_1')
        # get label
        field_label = analysisstatus_1._meta.get_field('analysisstatus_id').verbose_name
        # compare
        self.assertEqual(field_label, 'analysisstatus id')

    def test_analysisstatus_name_attribute_label(self):
        """ test attribute label """

        # get object
        analysisstatus_1 = Analysisstatus.objects.get(analysisstatus_name='analysisstatus_1')
        # get label
        field_label = analysisstatus_1._meta.get_field('analysisstatus_name').verbose_name
        # compare
        self.assertEqual(field_label, 'analysisstatus name')

    def test_analysisstatus_note_attribute_label(self):
        """ test attribute label """

        # get object
        analysisstatus_1 = Analysisstatus.objects.get(analysisstatus_name='analysisstatus_1')
        # get label
        field_label = analysisstatus_1._meta.get_field('analysisstatus_note').verbose_name
        # compare
        self.assertEqual(field_label, 'analysisstatus note')

    def test_analysisstatus_name_length(self):
        """ test attribute label """

        # get object
        analysisstatus_1 = Analysisstatus.objects.get(analysisstatus_name='analysisstatus_1')
        # get max length
        max_length = analysisstatus_1._meta.get_field('analysisstatus_name').max_length
        # compare
        self.assertEqual(max_length, 30)
