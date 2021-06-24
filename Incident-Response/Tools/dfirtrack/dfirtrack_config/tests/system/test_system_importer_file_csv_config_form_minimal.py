from django.contrib.auth.models import User
from django.test import TestCase
from dfirtrack_config.forms import SystemImporterFileCsvConfigForm
from dfirtrack_main.models import Analysisstatus, Systemstatus


class SystemImporterFileCsvConfigFormMinimalTestCase(TestCase):
    """ system importer file CSV config form tests """

    @classmethod
    def setUpTestData(cls):

        # create user
        User.objects.create_user(username='testuser_system_importer_file_csv_config', password='j1mNhkDDrKC57triHZTE')

        # create objects
        Analysisstatus.objects.create(analysisstatus_name = 'analysisstatus_1')
        Systemstatus.objects.create(systemstatus_name = 'systemstatus_1')

    def test_system_importer_file_csv_config_form_minimal(self):
        """ test minimum form requirements / VALID """

        # get user
        testuser = User.objects.get(username='testuser_system_importer_file_csv_config').id
        # get objects
        analysisstatus_1 = Analysisstatus.objects.get(analysisstatus_name = 'analysisstatus_1').analysisstatus_id
        systemstatus_1 = Systemstatus.objects.get(systemstatus_name = 'systemstatus_1').systemstatus_id
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
            'csv_remove_tag': 'tag_remove_prefix',
            'csv_field_delimiter': 'field_comma',
            'csv_text_quote': 'text_double_quotation_marks',
            'csv_ip_delimiter': 'ip_semicolon',
            'csv_tag_delimiter': 'tag_space',
        })
        # compare
        self.assertTrue(form.is_valid())
