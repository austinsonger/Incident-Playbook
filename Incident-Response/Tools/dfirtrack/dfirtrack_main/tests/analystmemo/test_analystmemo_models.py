from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone
from dfirtrack_main.models import Analystmemo, System, Systemstatus

class AnalystmemoModelTestCase(TestCase):
    """ analystmemo model tests """

    @classmethod
    def setUpTestData(cls):

        # create user
        test_user = User.objects.create_user(username='testuser_analystmemo', password='h09JwX22izrDh7zvPley')

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
        Analystmemo.objects.create(
            analystmemo_note='lorem ipsum',
            system = system_1,
            analystmemo_created_by_user_id = test_user,
            analystmemo_modified_by_user_id = test_user,
        )

    def test_analystmemo_string(self):
        """ test string representation """

        # get object
        analystmemo_1 = Analystmemo.objects.get(analystmemo_note='lorem ipsum')
        # compare
        self.assertEqual(str(analystmemo_1), 'Analystmemo ' + str(analystmemo_1.analystmemo_id) + ' (' + str(analystmemo_1.system) + ')')

    def test_analystmemo_id_attribute_label(self):
        """ test attribute label """

        # get object
        analystmemo_1 = Analystmemo.objects.get(analystmemo_note='lorem ipsum')
        # get label
        field_label = analystmemo_1._meta.get_field('analystmemo_id').verbose_name
        # compare
        self.assertEqual(field_label, 'analystmemo id')

    def test_analystmemo_system_attribute_label(self):
        """ test attribute label """

        # get object
        analystmemo_1 = Analystmemo.objects.get(analystmemo_note='lorem ipsum')
        # get label
        field_label = analystmemo_1._meta.get_field('system').verbose_name
        # compare
        self.assertEqual(field_label, 'system')

    def test_analystmemo_note_attribute_label(self):
        """ test attribute label """

        # get object
        analystmemo_1 = Analystmemo.objects.get(analystmemo_note='lorem ipsum')
        # get label
        field_label = analystmemo_1._meta.get_field('analystmemo_note').verbose_name
        # compare
        self.assertEqual(field_label, 'analystmemo note')

    def test_analystmemo_create_time_attribute_label(self):
        """ test attribute label """

        # get object
        analystmemo_1 = Analystmemo.objects.get(analystmemo_note='lorem ipsum')
        # get label
        field_label = analystmemo_1._meta.get_field('analystmemo_create_time').verbose_name
        # compare
        self.assertEqual(field_label, 'analystmemo create time')

    def test_analystmemo_modify_time_attribute_label(self):
        """ test attribute label """

        # get object
        analystmemo_1 = Analystmemo.objects.get(analystmemo_note='lorem ipsum')
        # get label
        field_label = analystmemo_1._meta.get_field('analystmemo_modify_time').verbose_name
        # compare
        self.assertEqual(field_label, 'analystmemo modify time')

    def test_analystmemo_created_by_user_id_attribute_label(self):
        """ test attribute label """

        # get object
        analystmemo_1 = Analystmemo.objects.get(analystmemo_note='lorem ipsum')
        # get label
        field_label = analystmemo_1._meta.get_field('analystmemo_created_by_user_id').verbose_name
        # compare
        self.assertEqual(field_label, 'analystmemo created by user id')

    def test_analystmemo_modified_by_user_id_attribute_label(self):
        """ test attribute label """

        # get object
        analystmemo_1 = Analystmemo.objects.get(analystmemo_note='lorem ipsum')
        # get label
        field_label = analystmemo_1._meta.get_field('analystmemo_modified_by_user_id').verbose_name
        # compare
        self.assertEqual(field_label, 'analystmemo modified by user id')
