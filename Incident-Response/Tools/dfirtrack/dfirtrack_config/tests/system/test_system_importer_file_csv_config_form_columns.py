from django.contrib.auth.models import User
from django.test import TestCase
from dfirtrack_config.forms import SystemImporterFileCsvConfigForm
from dfirtrack_main.models import Analysisstatus, Systemstatus


class SystemImporterFileCsvConfigFormColumnsTestCase(TestCase):
    """ system importer file CSV config form tests """

    @classmethod
    def setUpTestData(cls):

        # create user
        User.objects.create_user(username='testuser_system_importer_file_csv_config', password='HOflhQ5TnUJPzYzAUGfP')

        # create objects
        Analysisstatus.objects.create(analysisstatus_name = 'analysisstatus_1')
        Systemstatus.objects.create(systemstatus_name = 'systemstatus_1')

    def test_system_importer_file_csv_config_form_equal_columns(self):
        """ test minimum form requirements / VALID """

        # get user
        testuser = User.objects.get(username='testuser_system_importer_file_csv_config').id
        # get objects
        analysisstatus_1 = Analysisstatus.objects.get(analysisstatus_name = 'analysisstatus_1').analysisstatus_id
        systemstatus_1 = Systemstatus.objects.get(systemstatus_name = 'systemstatus_1').systemstatus_id
        # create string
        unique_string = 'The column has to be unique.'
        # get form
        form = SystemImporterFileCsvConfigForm(data = {
            'csv_column_system': '1',
            'csv_import_path': '/tmp',
            'csv_import_filename': 'systems.csv',
            'csv_import_username': str(testuser),
            'csv_default_systemstatus': str(systemstatus_1),
            'csv_default_analysisstatus': str(analysisstatus_1),
            'csv_default_tagfree_systemstatus': str(systemstatus_1),
            'csv_default_tagfree_analysisstatus': str(analysisstatus_1),
            'csv_tag_lock_systemstatus': 'LOCK_SYSTEMSTATUS',
            'csv_tag_lock_analysisstatus': 'LOCK_ANALYSISSTATUS',
            'csv_choice_ip': True,
            'csv_column_ip': '1',
            'csv_choice_dnsname': True,
            'csv_column_dnsname': '1',
            'csv_choice_domain': True,
            'csv_column_domain': '1',
            'csv_choice_location': True,
            'csv_column_location': '1',
            'csv_choice_os': True,
            'csv_column_os': '1',
            'csv_choice_reason': True,
            'csv_column_reason': '1',
            'csv_choice_recommendation': True,
            'csv_column_recommendation': '1',
            'csv_choice_serviceprovider': True,
            'csv_column_serviceprovider': '1',
            'csv_choice_systemtype': True,
            'csv_column_systemtype': '1',
            'csv_choice_case': True,
            'csv_column_case': '1',
            'csv_choice_company': True,
            'csv_column_company': '1',
            'csv_choice_tag': True,
            'csv_column_tag': '1',
            'csv_remove_tag': 'tag_remove_prefix',
            'csv_tag_prefix': 'AUTO',
            'csv_tag_prefix_delimiter': 'tag_prefix_underscore',
            'csv_field_delimiter': 'field_comma',
            'csv_text_quote': 'text_double_quotation_marks',
            'csv_ip_delimiter': 'ip_semicolon',
            'csv_tag_delimiter': 'tag_space',
        })
        # compare
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['csv_column_ip'], [unique_string])
        self.assertEqual(form.errors['csv_column_dnsname'], [unique_string])
        self.assertEqual(form.errors['csv_column_domain'], [unique_string])
        self.assertEqual(form.errors['csv_column_location'], [unique_string])
        self.assertEqual(form.errors['csv_column_os'], [unique_string])
        self.assertEqual(form.errors['csv_column_reason'], [unique_string])
        self.assertEqual(form.errors['csv_column_recommendation'], [unique_string])
        self.assertEqual(form.errors['csv_column_serviceprovider'], [unique_string])
        self.assertEqual(form.errors['csv_column_systemtype'], [unique_string])
        self.assertEqual(form.errors['csv_column_case'], [unique_string])
        self.assertEqual(form.errors['csv_column_company'], [unique_string])
        self.assertEqual(form.errors['csv_column_tag'], [unique_string])
