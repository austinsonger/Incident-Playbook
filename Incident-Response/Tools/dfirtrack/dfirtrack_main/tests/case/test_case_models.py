from django.contrib.auth.models import User
from django.test import TestCase
from dfirtrack_main.models import Case

class CaseModelTestCase(TestCase):
    """ case model tests """

    @classmethod
    def setUpTestData(cls):

        # create user
        test_user = User.objects.create_user(username='testuser_case', password='ubtMz0kJgkeBqBKNlNUG')

        # create object
        Case.objects.create(
            case_name='case_1',
            case_is_incident=True,
            case_created_by_user_id=test_user,
        )

    def test_case_string(self):
        """ test string representation """

        # get object
        case_1 = Case.objects.get(case_name='case_1')
        # compare
        self.assertEqual(str(case_1), 'case_1')

    def test_case_id_attribute_label(self):
        """ test attribute label """

        # get object
        case_1 = Case.objects.get(case_name='case_1')
        # get label
        field_label = case_1._meta.get_field('case_id').verbose_name
        # compare
        self.assertEqual(field_label, 'case id')

    def test_case_name_attribute_label(self):
        """ test attribute label """

        # get object
        case_1 = Case.objects.get(case_name='case_1')
        # get label
        field_label = case_1._meta.get_field('case_name').verbose_name
        # compare
        self.assertEqual(field_label, 'case name')

    def test_case_is_incident_attribute_label(self):
        """ test attribute label """

        # get object
        case_1 = Case.objects.get(case_name='case_1')
        # get label
        field_label = case_1._meta.get_field('case_is_incident').verbose_name
        # compare
        self.assertEqual(field_label, 'case is incident')

    def test_case_create_time_attribute_label(self):
        """ test attribute label """

        # get object
        case_1 = Case.objects.get(case_name='case_1')
        # get label
        field_label = case_1._meta.get_field('case_create_time').verbose_name
        # compare
        self.assertEqual(field_label, 'case create time')

    def test_case_created_by_user_id_attribute_label(self):
        """ test attribute label """

        # get object
        case_1 = Case.objects.get(case_name='case_1')
        # get label
        field_label = case_1._meta.get_field('case_created_by_user_id').verbose_name
        # compare
        self.assertEqual(field_label, 'case created by user id')

    def test_case_name_length(self):
        """ test for max length """

        # get object
        case_1 = Case.objects.get(case_name='case_1')
        # get max length
        max_length = case_1._meta.get_field('case_name').max_length
        # compare
        self.assertEqual(max_length, 50)
