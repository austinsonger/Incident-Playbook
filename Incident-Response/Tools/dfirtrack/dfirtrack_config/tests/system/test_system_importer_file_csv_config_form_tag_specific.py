from django.contrib.auth.models import User
from django.test import TestCase
from dfirtrack_config.forms import SystemImporterFileCsvConfigForm
from dfirtrack_main.models import Analysisstatus, Systemstatus, Tag, Tagcolor


class SystemImporterFileCsvConfigFormTagSpecificTestCase(TestCase):
    """ system importer file CSV config form tests """

    @classmethod
    def setUpTestData(cls):

        # create user
        User.objects.create_user(username='testuser_system_importer_file_csv_config', password='U8Mc5zzE3b2XMzxhJISf')

        # create objects
        Analysisstatus.objects.create(analysisstatus_name = 'analysisstatus_1')
        Systemstatus.objects.create(systemstatus_name = 'systemstatus_1')
        tagcolor_1 = Tagcolor.objects.create(tagcolor_name = 'tagcolor_1')
        Tag.objects.create(
            tag_name = 'tag_1',
            tagcolor = tagcolor_1,
        )

    """ tag """

    def test_system_importer_file_csv_config_form_tag_choice_only(self):
        """ test field validation """

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
            'csv_choice_tag': True,
            'csv_column_tag': None,
        })
        # compare
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['csv_choice_tag'], ['Add CSV column.'])

    def test_system_importer_file_csv_config_form_tag_column_only(self):
        """ test field validation """

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
            'csv_choice_tag': False,
            'csv_column_tag': '2',
        })
        # compare
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['csv_choice_tag'], ['Forgot to choose CSV?'])

    def test_system_importer_file_csv_config_form_tag_choice_and_db(self):
        """ test field validation """

        # get user
        testuser = User.objects.get(username='testuser_system_importer_file_csv_config').id
        # get objects
        analysisstatus_1 = Analysisstatus.objects.get(analysisstatus_name = 'analysisstatus_1').analysisstatus_id
        tag_1 = Tag.objects.get(tag_name = 'tag_1').tag_id
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
            'csv_choice_tag': True,
            'csv_default_tag': [str(tag_1),],
        })
        # compare
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['csv_choice_tag'], ['Decide between CSV or database or nothing.'])

    def test_system_importer_file_csv_config_form_tag_column_and_db(self):
        """ test field validation """

        # get user
        testuser = User.objects.get(username='testuser_system_importer_file_csv_config').id
        # get objects
        analysisstatus_1 = Analysisstatus.objects.get(analysisstatus_name = 'analysisstatus_1').analysisstatus_id
        tag_1 = Tag.objects.get(tag_name = 'tag_1').tag_id
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
            'csv_column_tag': '2',
            'csv_default_tag': [str(tag_1),],
        })
        # compare
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['csv_choice_tag'], ['Decide between CSV or database or nothing.'])

    def test_system_importer_file_csv_config_form_tag_choice_column_and_db(self):
        """ test field validation """

        # get user
        testuser = User.objects.get(username='testuser_system_importer_file_csv_config').id
        # get objects
        analysisstatus_1 = Analysisstatus.objects.get(analysisstatus_name = 'analysisstatus_1').analysisstatus_id
        tag_1 = Tag.objects.get(tag_name = 'tag_1').tag_id
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
            'csv_choice_tag': True,
            'csv_column_tag': '2',
            'csv_default_tag': [str(tag_1),],
        })
        # compare
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['csv_choice_tag'], ['Decide between CSV or database or nothing.'])

    def test_system_importer_file_csv_config_form_tag_from_csv_no_prefix(self):
        """ test field validation """

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
            'csv_choice_tag': True,
            'csv_column_tag': '2',
            'csv_tag_prefix_delimiter': 'tag_prefix_underscore',
        })
        # compare
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['csv_tag_prefix'], ['Choose prefix and delimiter for tag import from CSV to distinguish between manual set tags.'])

    def test_system_importer_file_csv_config_form_tag_from_csv_no_prefix_delimiter(self):
        """ test field validation """

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
            'csv_choice_tag': True,
            'csv_column_tag': '2',
            'csv_tag_prefix': 'AUTO',
        })
        # compare
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['csv_tag_prefix'], ['Choose prefix and delimiter for tag import from CSV to distinguish between manual set tags.'])

    def test_system_importer_file_csv_config_form_tag_from_csv_valid(self):
        """ test field validation """

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
            'csv_choice_tag': True,
            'csv_column_tag': '2',
            'csv_tag_prefix': 'AUTO',
            'csv_tag_prefix_delimiter': 'tag_prefix_underscore',
        })
        # compare
        self.assertTrue(form.is_valid())

    def test_system_importer_file_csv_config_form_tag_from_db_and_prefix(self):
        """ test field validation """

        # get user
        testuser = User.objects.get(username='testuser_system_importer_file_csv_config').id
        # get objects
        analysisstatus_1 = Analysisstatus.objects.get(analysisstatus_name = 'analysisstatus_1').analysisstatus_id
        tag_1 = Tag.objects.get(tag_name = 'tag_1').tag_id
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
            'csv_remove_tag': 'tag_remove_all',
            'csv_field_delimiter': 'field_comma',
            'csv_text_quote': 'text_double_quotation_marks',
            'csv_ip_delimiter': 'ip_semicolon',
            'csv_tag_delimiter': 'tag_space',
            'csv_default_tag': [str(tag_1),],
            'csv_tag_prefix': 'AUTO',
        })
        # compare
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['csv_tag_prefix'], ['Prefix and delimiter are not available when setting tags from database.'])

    def test_system_importer_file_csv_config_form_tag_from_db_and_prefix_delimiter(self):
        """ test field validation """

        # get user
        testuser = User.objects.get(username='testuser_system_importer_file_csv_config').id
        # get objects
        analysisstatus_1 = Analysisstatus.objects.get(analysisstatus_name = 'analysisstatus_1').analysisstatus_id
        tag_1 = Tag.objects.get(tag_name = 'tag_1').tag_id
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
            'csv_remove_tag': 'tag_remove_all',
            'csv_field_delimiter': 'field_comma',
            'csv_text_quote': 'text_double_quotation_marks',
            'csv_ip_delimiter': 'ip_semicolon',
            'csv_tag_delimiter': 'tag_space',
            'csv_default_tag': [str(tag_1),],
            'csv_tag_prefix_delimiter': 'tag_prefix_underscore',
        })
        # compare
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['csv_tag_prefix'], ['Prefix and delimiter are not available when setting tags from database.'])

    def test_system_importer_file_csv_config_form_tag_from_db_prefix_and_prefix_delimiter(self):
        """ test field validation """

        # get user
        testuser = User.objects.get(username='testuser_system_importer_file_csv_config').id
        # get objects
        analysisstatus_1 = Analysisstatus.objects.get(analysisstatus_name = 'analysisstatus_1').analysisstatus_id
        tag_1 = Tag.objects.get(tag_name = 'tag_1').tag_id
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
            'csv_remove_tag': 'tag_remove_all',
            'csv_field_delimiter': 'field_comma',
            'csv_text_quote': 'text_double_quotation_marks',
            'csv_ip_delimiter': 'ip_semicolon',
            'csv_tag_delimiter': 'tag_space',
            'csv_default_tag': [str(tag_1),],
            'csv_tag_prefix': 'AUTO',
            'csv_tag_prefix_delimiter': 'tag_prefix_underscore',
        })
        # compare
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['csv_tag_prefix'], ['Prefix and delimiter are not available when setting tags from database.'])

    def test_system_importer_file_csv_config_form_tag_from_db_and_remove_prefix(self):
        """ test field validation """

        # get user
        testuser = User.objects.get(username='testuser_system_importer_file_csv_config').id
        # get objects
        analysisstatus_1 = Analysisstatus.objects.get(analysisstatus_name = 'analysisstatus_1').analysisstatus_id
        tag_1 = Tag.objects.get(tag_name = 'tag_1').tag_id
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
            'csv_default_tag': [str(tag_1),],
        })
        # compare
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['csv_remove_tag'], ['Removing tags with prefix is only available when setting tags from CSV.'])

    def test_system_importer_file_csv_config_form_tag_from_db_and_tagfree_systemstatus(self):
        """ test field validation """

        # get user
        testuser = User.objects.get(username='testuser_system_importer_file_csv_config').id
        # get objects
        analysisstatus_1 = Analysisstatus.objects.get(analysisstatus_name = 'analysisstatus_1').analysisstatus_id
        tag_1 = Tag.objects.get(tag_name = 'tag_1').tag_id
        systemstatus_1 = Systemstatus.objects.get(systemstatus_name = 'systemstatus_1').systemstatus_id
        # create object
        systemstatus_2 = Systemstatus.objects.create(systemstatus_name = 'systemstatus_2').systemstatus_id
        # get form
        form = SystemImporterFileCsvConfigForm(data = {
            'csv_column_system': '1',
            'csv_import_path': '/tmp',
            'csv_import_filename': 'systems.csv',
            'csv_import_username': str(testuser),
            'csv_default_systemstatus': str(systemstatus_1),
            'csv_default_analysisstatus': str(analysisstatus_1),
            'csv_choice_tagfree_systemstatus': True,
            'csv_default_tagfree_systemstatus': str(systemstatus_2),
            'csv_default_tagfree_analysisstatus': str(analysisstatus_1),
            'csv_tag_lock_systemstatus': 'LOCK_SYSTEMSTATUS',
            'csv_tag_lock_analysisstatus': 'LOCK_ANALYSISSTATUS',
            'csv_remove_tag': 'tag_remove_all',
            'csv_field_delimiter': 'field_comma',
            'csv_text_quote': 'text_double_quotation_marks',
            'csv_ip_delimiter': 'ip_semicolon',
            'csv_tag_delimiter': 'tag_space',
            'csv_default_tag': [str(tag_1),],
        })
        # compare
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['csv_choice_tagfree_systemstatus'], ['Alternative systemstatus only available with tags from CSV.'])

    def test_system_importer_file_csv_config_form_tag_from_db_and_tagfree_analysisstatus(self):
        """ test field validation """

        # get user
        testuser = User.objects.get(username='testuser_system_importer_file_csv_config').id
        # get objects
        analysisstatus_1 = Analysisstatus.objects.get(analysisstatus_name = 'analysisstatus_1').analysisstatus_id
        tag_1 = Tag.objects.get(tag_name = 'tag_1').tag_id
        systemstatus_1 = Systemstatus.objects.get(systemstatus_name = 'systemstatus_1').systemstatus_id
        # create object
        analysisstatus_2 = Analysisstatus.objects.create(analysisstatus_name = 'analysisstatus_2').analysisstatus_id
        # get form
        form = SystemImporterFileCsvConfigForm(data = {
            'csv_column_system': '1',
            'csv_import_path': '/tmp',
            'csv_import_filename': 'systems.csv',
            'csv_import_username': str(testuser),
            'csv_default_systemstatus': str(systemstatus_1),
            'csv_default_analysisstatus': str(analysisstatus_1),
            'csv_choice_tagfree_analysisstatus': True,
            'csv_default_tagfree_systemstatus': str(systemstatus_1),
            'csv_default_tagfree_analysisstatus': str(analysisstatus_2),
            'csv_tag_lock_systemstatus': 'LOCK_SYSTEMSTATUS',
            'csv_tag_lock_analysisstatus': 'LOCK_ANALYSISSTATUS',
            'csv_remove_tag': 'tag_remove_all',
            'csv_field_delimiter': 'field_comma',
            'csv_text_quote': 'text_double_quotation_marks',
            'csv_ip_delimiter': 'ip_semicolon',
            'csv_tag_delimiter': 'tag_space',
            'csv_default_tag': [str(tag_1),],
        })
        # compare
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['csv_choice_tagfree_analysisstatus'], ['Alternative analysisstatus only available with tags from CSV.'])

    def test_system_importer_file_csv_config_form_tag_from_db_valid(self):
        """ test field validation """

        # get user
        testuser = User.objects.get(username='testuser_system_importer_file_csv_config').id
        # get objects
        analysisstatus_1 = Analysisstatus.objects.get(analysisstatus_name = 'analysisstatus_1').analysisstatus_id
        tag_1 = Tag.objects.get(tag_name = 'tag_1').tag_id
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
            'csv_remove_tag': 'tag_remove_all',
            'csv_field_delimiter': 'field_comma',
            'csv_text_quote': 'text_double_quotation_marks',
            'csv_ip_delimiter': 'ip_semicolon',
            'csv_tag_delimiter': 'tag_space',
            'csv_default_tag': [str(tag_1),],
        })
        # compare
        self.assertTrue(form.is_valid())
