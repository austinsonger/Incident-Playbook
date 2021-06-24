from django.contrib.auth.models import User
from django.test import TestCase
from dfirtrack_config.forms import SystemImporterFileCsvConfigForm
from dfirtrack_main.models import Analysisstatus, Case, Company, Dnsname, Domain, Location, Os, Reason, Recommendation, Serviceprovider, Systemstatus, Systemtype


class SystemImporterFileCsvConfigFormCsvVsDbTestCase(TestCase):
    """ system importer file CSV config form tests """

    @classmethod
    def setUpTestData(cls):

        # create user
        testuser = User.objects.create_user(username='testuser_system_importer_file_csv_config', password='KnnxdpiEIgygkh8qGmXK')

        # create objects
        Analysisstatus.objects.create(analysisstatus_name = 'analysisstatus_1')
        Case.objects.create(
            case_name = 'case_1',
            case_is_incident = False,
            case_created_by_user_id = testuser,
        )
        Company.objects.create(company_name = 'company_1').company_id
        Dnsname.objects.create(dnsname_name = 'dnsname_1').dnsname_id
        Domain.objects.create(domain_name = 'domain_1').domain_id
        Location.objects.create(location_name = 'location_1').location_id
        Os.objects.create(os_name = 'os_1').os_id
        Reason.objects.create(reason_name = 'reason_1').reason_id
        Recommendation.objects.create(recommendation_name = 'recommendation_1').recommendation_id
        Serviceprovider.objects.create(serviceprovider_name = 'serviceprovider_1').serviceprovider_id
        Systemstatus.objects.create(systemstatus_name = 'systemstatus_1')
        Systemtype.objects.create(systemtype_name = 'systemtype_1').systemtype_id

    """ ip """

    def test_system_importer_file_csv_config_form_ip_choice_only(self):
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
            'csv_choice_ip': True,
            'csv_column_ip': None,
        })
        # compare
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['csv_choice_ip'], ['Add CSV column.'])

    def test_system_importer_file_csv_config_form_ip_column_only(self):
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
            'csv_choice_ip': False,
            'csv_column_ip': '2',
        })
        # compare
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['csv_choice_ip'], ['Forgot to choose CSV?'])

    def test_system_importer_file_csv_config_form_ip_from_csv(self):
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
            'csv_choice_ip': True,
            'csv_column_ip': '2',
        })
        # compare
        self.assertTrue(form.is_valid())

    """ dnsname """

    def test_system_importer_file_csv_config_form_dnsname_choice_only(self):
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
            'csv_choice_dnsname': True,
            'csv_column_dnsname': None,
        })
        # compare
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['csv_choice_dnsname'], ['Add CSV column.'])

    def test_system_importer_file_csv_config_form_dnsname_column_only(self):
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
            'csv_choice_dnsname': False,
            'csv_column_dnsname': '2',
        })
        # compare
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['csv_choice_dnsname'], ['Forgot to choose CSV?'])

    def test_system_importer_file_csv_config_form_dnsname_choice_and_db(self):
        """ test field validation """

        # get user
        testuser = User.objects.get(username='testuser_system_importer_file_csv_config').id
        # get objects
        analysisstatus_1 = Analysisstatus.objects.get(analysisstatus_name = 'analysisstatus_1').analysisstatus_id
        dnsname_1 = Dnsname.objects.get(dnsname_name = 'dnsname_1').dnsname_id
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
            'csv_choice_dnsname': True,
            'csv_default_dnsname': str(dnsname_1),
        })
        # compare
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['csv_choice_dnsname'], ['Decide between CSV or database or nothing.'])

    def test_system_importer_file_csv_config_form_dnsname_column_and_db(self):
        """ test field validation """

        # get user
        testuser = User.objects.get(username='testuser_system_importer_file_csv_config').id
        # get objects
        analysisstatus_1 = Analysisstatus.objects.get(analysisstatus_name = 'analysisstatus_1').analysisstatus_id
        dnsname_1 = Dnsname.objects.get(dnsname_name = 'dnsname_1').dnsname_id
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
            'csv_column_dnsname': '2',
            'csv_default_dnsname': str(dnsname_1),
        })
        # compare
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['csv_choice_dnsname'], ['Decide between CSV or database or nothing.'])

    def test_system_importer_file_csv_config_form_dnsname_choice_column_and_db(self):
        """ test field validation """

        # get user
        testuser = User.objects.get(username='testuser_system_importer_file_csv_config').id
        # get objects
        analysisstatus_1 = Analysisstatus.objects.get(analysisstatus_name = 'analysisstatus_1').analysisstatus_id
        dnsname_1 = Dnsname.objects.get(dnsname_name = 'dnsname_1').dnsname_id
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
            'csv_choice_dnsname': True,
            'csv_column_dnsname': '2',
            'csv_default_dnsname': str(dnsname_1),
        })
        # compare
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['csv_choice_dnsname'], ['Decide between CSV or database or nothing.'])

    def test_system_importer_file_csv_config_form_dnsname_from_csv(self):
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
            'csv_choice_dnsname': True,
            'csv_column_dnsname': '2',
        })
        # compare
        self.assertTrue(form.is_valid())

    def test_system_importer_file_csv_config_form_dnsname_from_db(self):
        """ test field validation """

        # get user
        testuser = User.objects.get(username='testuser_system_importer_file_csv_config').id
        # get objects
        analysisstatus_1 = Analysisstatus.objects.get(analysisstatus_name = 'analysisstatus_1').analysisstatus_id
        dnsname_1 = Dnsname.objects.get(dnsname_name = 'dnsname_1').dnsname_id
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
            'csv_default_dnsname': str(dnsname_1),
        })
        # compare
        self.assertTrue(form.is_valid())

    """ domain """

    def test_system_importer_file_csv_config_form_domain_choice_only(self):
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
            'csv_choice_domain': True,
            'csv_column_domain': None,
        })
        # compare
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['csv_choice_domain'], ['Add CSV column.'])

    def test_system_importer_file_csv_config_form_domain_column_only(self):
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
            'csv_choice_domain': False,
            'csv_column_domain': '2',
        })
        # compare
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['csv_choice_domain'], ['Forgot to choose CSV?'])

    def test_system_importer_file_csv_config_form_domain_choice_and_db(self):
        """ test field validation """

        # get user
        testuser = User.objects.get(username='testuser_system_importer_file_csv_config').id
        # get objects
        analysisstatus_1 = Analysisstatus.objects.get(analysisstatus_name = 'analysisstatus_1').analysisstatus_id
        domain_1 = Domain.objects.get(domain_name = 'domain_1').domain_id
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
            'csv_choice_domain': True,
            'csv_default_domain': str(domain_1),
        })
        # compare
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['csv_choice_domain'], ['Decide between CSV or database or nothing.'])

    def test_system_importer_file_csv_config_form_domain_column_and_db(self):
        """ test field validation """

        # get user
        testuser = User.objects.get(username='testuser_system_importer_file_csv_config').id
        # get objects
        analysisstatus_1 = Analysisstatus.objects.get(analysisstatus_name = 'analysisstatus_1').analysisstatus_id
        domain_1 = Domain.objects.get(domain_name = 'domain_1').domain_id
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
            'csv_column_domain': '2',
            'csv_default_domain': str(domain_1),
        })
        # compare
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['csv_choice_domain'], ['Decide between CSV or database or nothing.'])

    def test_system_importer_file_csv_config_form_domain_choice_column_and_db(self):
        """ test field validation """

        # get user
        testuser = User.objects.get(username='testuser_system_importer_file_csv_config').id
        # get objects
        analysisstatus_1 = Analysisstatus.objects.get(analysisstatus_name = 'analysisstatus_1').analysisstatus_id
        domain_1 = Domain.objects.get(domain_name = 'domain_1').domain_id
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
            'csv_choice_domain': True,
            'csv_column_domain': '2',
            'csv_default_domain': str(domain_1),
        })
        # compare
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['csv_choice_domain'], ['Decide between CSV or database or nothing.'])

    def test_system_importer_file_csv_config_form_domain_from_csv(self):
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
            'csv_choice_domain': True,
            'csv_column_domain': '2',
        })
        # compare
        self.assertTrue(form.is_valid())

    def test_system_importer_file_csv_config_form_domain_from_db(self):
        """ test field validation """

        # get user
        testuser = User.objects.get(username='testuser_system_importer_file_csv_config').id
        # get objects
        analysisstatus_1 = Analysisstatus.objects.get(analysisstatus_name = 'analysisstatus_1').analysisstatus_id
        domain_1 = Domain.objects.get(domain_name = 'domain_1').domain_id
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
            'csv_default_domain': str(domain_1),
        })
        # compare
        self.assertTrue(form.is_valid())

    """ location """

    def test_system_importer_file_csv_config_form_location_choice_only(self):
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
            'csv_choice_location': True,
            'csv_column_location': None,
        })
        # compare
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['csv_choice_location'], ['Add CSV column.'])

    def test_system_importer_file_csv_config_form_location_column_only(self):
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
            'csv_choice_location': False,
            'csv_column_location': '2',
        })
        # compare
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['csv_choice_location'], ['Forgot to choose CSV?'])

    def test_system_importer_file_csv_config_form_location_choice_and_db(self):
        """ test field validation """

        # get user
        testuser = User.objects.get(username='testuser_system_importer_file_csv_config').id
        # get objects
        analysisstatus_1 = Analysisstatus.objects.get(analysisstatus_name = 'analysisstatus_1').analysisstatus_id
        location_1 = Location.objects.get(location_name = 'location_1').location_id
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
            'csv_choice_location': True,
            'csv_default_location': str(location_1),
        })
        # compare
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['csv_choice_location'], ['Decide between CSV or database or nothing.'])

    def test_system_importer_file_csv_config_form_location_column_and_db(self):
        """ test field validation """

        # get user
        testuser = User.objects.get(username='testuser_system_importer_file_csv_config').id
        # get objects
        analysisstatus_1 = Analysisstatus.objects.get(analysisstatus_name = 'analysisstatus_1').analysisstatus_id
        location_1 = Location.objects.get(location_name = 'location_1').location_id
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
            'csv_column_location': '2',
            'csv_default_location': str(location_1),
        })
        # compare
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['csv_choice_location'], ['Decide between CSV or database or nothing.'])

    def test_system_importer_file_csv_config_form_location_choice_column_and_db(self):
        """ test field validation """

        # get user
        testuser = User.objects.get(username='testuser_system_importer_file_csv_config').id
        # get objects
        analysisstatus_1 = Analysisstatus.objects.get(analysisstatus_name = 'analysisstatus_1').analysisstatus_id
        location_1 = Location.objects.get(location_name = 'location_1').location_id
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
            'csv_choice_location': True,
            'csv_column_location': '2',
            'csv_default_location': str(location_1),
        })
        # compare
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['csv_choice_location'], ['Decide between CSV or database or nothing.'])

    def test_system_importer_file_csv_config_form_location_from_csv(self):
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
            'csv_choice_location': True,
            'csv_column_location': '2',
        })
        # compare
        self.assertTrue(form.is_valid())

    def test_system_importer_file_csv_config_form_location_from_db(self):
        """ test field validation """

        # get user
        testuser = User.objects.get(username='testuser_system_importer_file_csv_config').id
        # get objects
        analysisstatus_1 = Analysisstatus.objects.get(analysisstatus_name = 'analysisstatus_1').analysisstatus_id
        location_1 = Location.objects.get(location_name = 'location_1').location_id
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
            'csv_default_location': str(location_1),
        })
        # compare
        self.assertTrue(form.is_valid())

    """ os """

    def test_system_importer_file_csv_config_form_os_choice_only(self):
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
            'csv_choice_os': True,
            'csv_column_os': None,
        })
        # compare
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['csv_choice_os'], ['Add CSV column.'])

    def test_system_importer_file_csv_config_form_os_column_only(self):
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
            'csv_choice_os': False,
            'csv_column_os': '2',
        })
        # compare
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['csv_choice_os'], ['Forgot to choose CSV?'])

    def test_system_importer_file_csv_config_form_os_choice_and_db(self):
        """ test field validation """

        # get user
        testuser = User.objects.get(username='testuser_system_importer_file_csv_config').id
        # get objects
        analysisstatus_1 = Analysisstatus.objects.get(analysisstatus_name = 'analysisstatus_1').analysisstatus_id
        os_1 = Os.objects.get(os_name = 'os_1').os_id
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
            'csv_choice_os': True,
            'csv_default_os': str(os_1),
        })
        # compare
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['csv_choice_os'], ['Decide between CSV or database or nothing.'])

    def test_system_importer_file_csv_config_form_os_column_and_db(self):
        """ test field validation """

        # get user
        testuser = User.objects.get(username='testuser_system_importer_file_csv_config').id
        # get objects
        analysisstatus_1 = Analysisstatus.objects.get(analysisstatus_name = 'analysisstatus_1').analysisstatus_id
        os_1 = Os.objects.get(os_name = 'os_1').os_id
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
            'csv_column_os': '2',
            'csv_default_os': str(os_1),
        })
        # compare
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['csv_choice_os'], ['Decide between CSV or database or nothing.'])

    def test_system_importer_file_csv_config_form_os_choice_column_and_db(self):
        """ test field validation """

        # get user
        testuser = User.objects.get(username='testuser_system_importer_file_csv_config').id
        # get objects
        analysisstatus_1 = Analysisstatus.objects.get(analysisstatus_name = 'analysisstatus_1').analysisstatus_id
        os_1 = Os.objects.get(os_name = 'os_1').os_id
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
            'csv_choice_os': True,
            'csv_column_os': '2',
            'csv_default_os': str(os_1),
        })
        # compare
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['csv_choice_os'], ['Decide between CSV or database or nothing.'])

    def test_system_importer_file_csv_config_form_os_from_csv(self):
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
            'csv_choice_os': True,
            'csv_column_os': '2',
        })
        # compare
        self.assertTrue(form.is_valid())

    def test_system_importer_file_csv_config_form_os_from_db(self):
        """ test field validation """

        # get user
        testuser = User.objects.get(username='testuser_system_importer_file_csv_config').id
        # get objects
        analysisstatus_1 = Analysisstatus.objects.get(analysisstatus_name = 'analysisstatus_1').analysisstatus_id
        os_1 = Os.objects.get(os_name = 'os_1').os_id
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
            'csv_default_os': str(os_1),
        })
        # compare
        self.assertTrue(form.is_valid())

    """ reason """

    def test_system_importer_file_csv_config_form_reason_choice_only(self):
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
            'csv_choice_reason': True,
            'csv_column_reason': None,
        })
        # compare
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['csv_choice_reason'], ['Add CSV column.'])

    def test_system_importer_file_csv_config_form_reason_column_only(self):
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
            'csv_choice_reason': False,
            'csv_column_reason': '2',
        })
        # compare
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['csv_choice_reason'], ['Forgot to choose CSV?'])

    def test_system_importer_file_csv_config_form_reason_choice_and_db(self):
        """ test field validation """

        # get user
        testuser = User.objects.get(username='testuser_system_importer_file_csv_config').id
        # get objects
        analysisstatus_1 = Analysisstatus.objects.get(analysisstatus_name = 'analysisstatus_1').analysisstatus_id
        reason_1 = Reason.objects.get(reason_name = 'reason_1').reason_id
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
            'csv_choice_reason': True,
            'csv_default_reason': str(reason_1),
        })
        # compare
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['csv_choice_reason'], ['Decide between CSV or database or nothing.'])

    def test_system_importer_file_csv_config_form_reason_column_and_db(self):
        """ test field validation """

        # get user
        testuser = User.objects.get(username='testuser_system_importer_file_csv_config').id
        # get objects
        analysisstatus_1 = Analysisstatus.objects.get(analysisstatus_name = 'analysisstatus_1').analysisstatus_id
        reason_1 = Reason.objects.get(reason_name = 'reason_1').reason_id
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
            'csv_column_reason': '2',
            'csv_default_reason': str(reason_1),
        })
        # compare
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['csv_choice_reason'], ['Decide between CSV or database or nothing.'])

    def test_system_importer_file_csv_config_form_reason_choice_column_and_db(self):
        """ test field validation """

        # get user
        testuser = User.objects.get(username='testuser_system_importer_file_csv_config').id
        # get objects
        analysisstatus_1 = Analysisstatus.objects.get(analysisstatus_name = 'analysisstatus_1').analysisstatus_id
        reason_1 = Reason.objects.get(reason_name = 'reason_1').reason_id
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
            'csv_choice_reason': True,
            'csv_column_reason': '2',
            'csv_default_reason': str(reason_1),
        })
        # compare
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['csv_choice_reason'], ['Decide between CSV or database or nothing.'])

    def test_system_importer_file_csv_config_form_reason_from_csv(self):
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
            'csv_choice_reason': True,
            'csv_column_reason': '2',
        })
        # compare
        self.assertTrue(form.is_valid())

    def test_system_importer_file_csv_config_form_reason_from_db(self):
        """ test field validation """

        # get user
        testuser = User.objects.get(username='testuser_system_importer_file_csv_config').id
        # get objects
        analysisstatus_1 = Analysisstatus.objects.get(analysisstatus_name = 'analysisstatus_1').analysisstatus_id
        reason_1 = Reason.objects.get(reason_name = 'reason_1').reason_id
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
            'csv_default_reason': str(reason_1),
        })
        # compare
        self.assertTrue(form.is_valid())

    """ recommendation """

    def test_system_importer_file_csv_config_form_recommendation_choice_only(self):
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
            'csv_choice_recommendation': True,
            'csv_column_recommendation': None,
        })
        # compare
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['csv_choice_recommendation'], ['Add CSV column.'])

    def test_system_importer_file_csv_config_form_recommendation_column_only(self):
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
            'csv_choice_recommendation': False,
            'csv_column_recommendation': '2',
        })
        # compare
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['csv_choice_recommendation'], ['Forgot to choose CSV?'])

    def test_system_importer_file_csv_config_form_recommendation_choice_and_db(self):
        """ test field validation """

        # get user
        testuser = User.objects.get(username='testuser_system_importer_file_csv_config').id
        # get objects
        analysisstatus_1 = Analysisstatus.objects.get(analysisstatus_name = 'analysisstatus_1').analysisstatus_id
        recommendation_1 = Recommendation.objects.get(recommendation_name = 'recommendation_1').recommendation_id
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
            'csv_choice_recommendation': True,
            'csv_default_recommendation': str(recommendation_1),
        })
        # compare
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['csv_choice_recommendation'], ['Decide between CSV or database or nothing.'])

    def test_system_importer_file_csv_config_form_recommendation_column_and_db(self):
        """ test field validation """

        # get user
        testuser = User.objects.get(username='testuser_system_importer_file_csv_config').id
        # get objects
        analysisstatus_1 = Analysisstatus.objects.get(analysisstatus_name = 'analysisstatus_1').analysisstatus_id
        recommendation_1 = Recommendation.objects.get(recommendation_name = 'recommendation_1').recommendation_id
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
            'csv_column_recommendation': '2',
            'csv_default_recommendation': str(recommendation_1),
        })
        # compare
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['csv_choice_recommendation'], ['Decide between CSV or database or nothing.'])

    def test_system_importer_file_csv_config_form_recommendation_choice_column_and_db(self):
        """ test field validation """

        # get user
        testuser = User.objects.get(username='testuser_system_importer_file_csv_config').id
        # get objects
        analysisstatus_1 = Analysisstatus.objects.get(analysisstatus_name = 'analysisstatus_1').analysisstatus_id
        recommendation_1 = Recommendation.objects.get(recommendation_name = 'recommendation_1').recommendation_id
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
            'csv_choice_recommendation': True,
            'csv_column_recommendation': '2',
            'csv_default_recommendation': str(recommendation_1),
        })
        # compare
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['csv_choice_recommendation'], ['Decide between CSV or database or nothing.'])

    def test_system_importer_file_csv_config_form_recommendation_from_csv(self):
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
            'csv_choice_recommendation': True,
            'csv_column_recommendation': '2',
        })
        # compare
        self.assertTrue(form.is_valid())

    def test_system_importer_file_csv_config_form_recommendation_from_db(self):
        """ test field validation """

        # get user
        testuser = User.objects.get(username='testuser_system_importer_file_csv_config').id
        # get objects
        analysisstatus_1 = Analysisstatus.objects.get(analysisstatus_name = 'analysisstatus_1').analysisstatus_id
        recommendation_1 = Recommendation.objects.get(recommendation_name = 'recommendation_1').recommendation_id
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
            'csv_default_recommendation': str(recommendation_1),
        })
        # compare
        self.assertTrue(form.is_valid())

    """ serviceprovider """

    def test_system_importer_file_csv_config_form_serviceprovider_choice_only(self):
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
            'csv_choice_serviceprovider': True,
            'csv_column_serviceprovider': None,
        })
        # compare
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['csv_choice_serviceprovider'], ['Add CSV column.'])

    def test_system_importer_file_csv_config_form_serviceprovider_column_only(self):
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
            'csv_choice_serviceprovider': False,
            'csv_column_serviceprovider': '2',
        })
        # compare
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['csv_choice_serviceprovider'], ['Forgot to choose CSV?'])

    def test_system_importer_file_csv_config_form_serviceprovider_choice_and_db(self):
        """ test field validation """

        # get user
        testuser = User.objects.get(username='testuser_system_importer_file_csv_config').id
        # get objects
        analysisstatus_1 = Analysisstatus.objects.get(analysisstatus_name = 'analysisstatus_1').analysisstatus_id
        serviceprovider_1 = Serviceprovider.objects.get(serviceprovider_name = 'serviceprovider_1').serviceprovider_id
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
            'csv_choice_serviceprovider': True,
            'csv_default_serviceprovider': str(serviceprovider_1),
        })
        # compare
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['csv_choice_serviceprovider'], ['Decide between CSV or database or nothing.'])

    def test_system_importer_file_csv_config_form_serviceprovider_column_and_db(self):
        """ test field validation """

        # get user
        testuser = User.objects.get(username='testuser_system_importer_file_csv_config').id
        # get objects
        analysisstatus_1 = Analysisstatus.objects.get(analysisstatus_name = 'analysisstatus_1').analysisstatus_id
        serviceprovider_1 = Serviceprovider.objects.get(serviceprovider_name = 'serviceprovider_1').serviceprovider_id
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
            'csv_column_serviceprovider': '2',
            'csv_default_serviceprovider': str(serviceprovider_1),
        })
        # compare
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['csv_choice_serviceprovider'], ['Decide between CSV or database or nothing.'])

    def test_system_importer_file_csv_config_form_serviceprovider_choice_column_and_db(self):
        """ test field validation """

        # get user
        testuser = User.objects.get(username='testuser_system_importer_file_csv_config').id
        # get objects
        analysisstatus_1 = Analysisstatus.objects.get(analysisstatus_name = 'analysisstatus_1').analysisstatus_id
        serviceprovider_1 = Serviceprovider.objects.get(serviceprovider_name = 'serviceprovider_1').serviceprovider_id
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
            'csv_choice_serviceprovider': True,
            'csv_column_serviceprovider': '2',
            'csv_default_serviceprovider': str(serviceprovider_1),
        })
        # compare
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['csv_choice_serviceprovider'], ['Decide between CSV or database or nothing.'])

    def test_system_importer_file_csv_config_form_serviceprovider_from_csv(self):
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
            'csv_choice_serviceprovider': True,
            'csv_column_serviceprovider': '2',
        })
        # compare
        self.assertTrue(form.is_valid())

    def test_system_importer_file_csv_config_form_serviceprovider_from_db(self):
        """ test field validation """

        # get user
        testuser = User.objects.get(username='testuser_system_importer_file_csv_config').id
        # get objects
        analysisstatus_1 = Analysisstatus.objects.get(analysisstatus_name = 'analysisstatus_1').analysisstatus_id
        serviceprovider_1 = Serviceprovider.objects.get(serviceprovider_name = 'serviceprovider_1').serviceprovider_id
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
            'csv_default_serviceprovider': str(serviceprovider_1),
        })
        # compare
        self.assertTrue(form.is_valid())

    """ systemtype """

    def test_system_importer_file_csv_config_form_systemtype_choice_only(self):
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
            'csv_choice_systemtype': True,
            'csv_column_systemtype': None,
        })
        # compare
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['csv_choice_systemtype'], ['Add CSV column.'])

    def test_system_importer_file_csv_config_form_systemtype_column_only(self):
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
            'csv_choice_systemtype': False,
            'csv_column_systemtype': '2',
        })
        # compare
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['csv_choice_systemtype'], ['Forgot to choose CSV?'])

    def test_system_importer_file_csv_config_form_systemtype_choice_and_db(self):
        """ test field validation """

        # get user
        testuser = User.objects.get(username='testuser_system_importer_file_csv_config').id
        # get objects
        analysisstatus_1 = Analysisstatus.objects.get(analysisstatus_name = 'analysisstatus_1').analysisstatus_id
        systemstatus_1 = Systemstatus.objects.get(systemstatus_name = 'systemstatus_1').systemstatus_id
        systemtype_1 = Systemtype.objects.get(systemtype_name = 'systemtype_1').systemtype_id
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
            'csv_choice_systemtype': True,
            'csv_default_systemtype': str(systemtype_1),
        })
        # compare
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['csv_choice_systemtype'], ['Decide between CSV or database or nothing.'])

    def test_system_importer_file_csv_config_form_systemtype_column_and_db(self):
        """ test field validation """

        # get user
        testuser = User.objects.get(username='testuser_system_importer_file_csv_config').id
        # get objects
        analysisstatus_1 = Analysisstatus.objects.get(analysisstatus_name = 'analysisstatus_1').analysisstatus_id
        systemstatus_1 = Systemstatus.objects.get(systemstatus_name = 'systemstatus_1').systemstatus_id
        systemtype_1 = Systemtype.objects.get(systemtype_name = 'systemtype_1').systemtype_id
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
            'csv_column_systemtype': '2',
            'csv_default_systemtype': str(systemtype_1),
        })
        # compare
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['csv_choice_systemtype'], ['Decide between CSV or database or nothing.'])

    def test_system_importer_file_csv_config_form_systemtype_choice_column_and_db(self):
        """ test field validation """

        # get user
        testuser = User.objects.get(username='testuser_system_importer_file_csv_config').id
        # get objects
        analysisstatus_1 = Analysisstatus.objects.get(analysisstatus_name = 'analysisstatus_1').analysisstatus_id
        systemstatus_1 = Systemstatus.objects.get(systemstatus_name = 'systemstatus_1').systemstatus_id
        systemtype_1 = Systemtype.objects.get(systemtype_name = 'systemtype_1').systemtype_id
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
            'csv_choice_systemtype': True,
            'csv_column_systemtype': '2',
            'csv_default_systemtype': str(systemtype_1),
        })
        # compare
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['csv_choice_systemtype'], ['Decide between CSV or database or nothing.'])

    def test_system_importer_file_csv_config_form_systemtype_from_csv(self):
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
            'csv_choice_systemtype': True,
            'csv_column_systemtype': '2',
        })
        # compare
        self.assertTrue(form.is_valid())

    def test_system_importer_file_csv_config_form_systemtype_from_db(self):
        """ test field validation """

        # get user
        testuser = User.objects.get(username='testuser_system_importer_file_csv_config').id
        # get objects
        analysisstatus_1 = Analysisstatus.objects.get(analysisstatus_name = 'analysisstatus_1').analysisstatus_id
        systemstatus_1 = Systemstatus.objects.get(systemstatus_name = 'systemstatus_1').systemstatus_id
        systemtype_1 = Systemtype.objects.get(systemtype_name = 'systemtype_1').systemtype_id
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
            'csv_default_systemtype': str(systemtype_1),
        })
        # compare
        self.assertTrue(form.is_valid())

    """ case """

    def test_system_importer_file_csv_config_form_case_choice_only(self):
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
            'csv_choice_case': True,
            'csv_column_case': None,
        })
        # compare
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['csv_choice_case'], ['Add CSV column.'])

    def test_system_importer_file_csv_config_form_case_column_only(self):
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
            'csv_choice_case': False,
            'csv_column_case': '2',
        })
        # compare
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['csv_choice_case'], ['Forgot to choose CSV?'])

    def test_system_importer_file_csv_config_form_case_choice_and_db(self):
        """ test field validation """

        # get user
        testuser = User.objects.get(username='testuser_system_importer_file_csv_config').id
        # get objects
        analysisstatus_1 = Analysisstatus.objects.get(analysisstatus_name = 'analysisstatus_1').analysisstatus_id
        case_1 = Case.objects.get(case_name = 'case_1').case_id
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
            'csv_choice_case': True,
            'csv_default_case': [str(case_1),],
        })
        # compare
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['csv_choice_case'], ['Decide between CSV or database or nothing.'])

    def test_system_importer_file_csv_config_form_case_column_and_db(self):
        """ test field validation """

        # get user
        testuser = User.objects.get(username='testuser_system_importer_file_csv_config').id
        # get objects
        analysisstatus_1 = Analysisstatus.objects.get(analysisstatus_name = 'analysisstatus_1').analysisstatus_id
        case_1 = Case.objects.get(case_name = 'case_1').case_id
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
            'csv_column_case': '2',
            'csv_default_case': [str(case_1),],
        })
        # compare
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['csv_choice_case'], ['Decide between CSV or database or nothing.'])

    def test_system_importer_file_csv_config_form_case_choice_column_and_db(self):
        """ test field validation """

        # get user
        testuser = User.objects.get(username='testuser_system_importer_file_csv_config').id
        # get objects
        analysisstatus_1 = Analysisstatus.objects.get(analysisstatus_name = 'analysisstatus_1').analysisstatus_id
        case_1 = Case.objects.get(case_name = 'case_1').case_id
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
            'csv_choice_case': True,
            'csv_column_case': '2',
            'csv_default_case': [str(case_1),],
        })
        # compare
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['csv_choice_case'], ['Decide between CSV or database or nothing.'])

    def test_system_importer_file_csv_config_form_case_from_csv(self):
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
            'csv_choice_case': True,
            'csv_column_case': '2',
        })
        # compare
        self.assertTrue(form.is_valid())

    def test_system_importer_file_csv_config_form_case_from_db(self):
        """ test field validation """

        # get user
        testuser = User.objects.get(username='testuser_system_importer_file_csv_config').id
        # get objects
        analysisstatus_1 = Analysisstatus.objects.get(analysisstatus_name = 'analysisstatus_1').analysisstatus_id
        case_1 = Case.objects.get(case_name = 'case_1').case_id
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
            'csv_default_case': [str(case_1),],
        })
        # compare
        self.assertTrue(form.is_valid())

    """ company """

    def test_system_importer_file_csv_config_form_company_choice_only(self):
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
            'csv_choice_company': True,
            'csv_column_company': None,
        })
        # compare
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['csv_choice_company'], ['Add CSV column.'])

    def test_system_importer_file_csv_config_form_company_column_only(self):
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
            'csv_choice_company': False,
            'csv_column_company': '2',
        })
        # compare
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['csv_choice_company'], ['Forgot to choose CSV?'])

    def test_system_importer_file_csv_config_form_company_choice_and_db(self):
        """ test field validation """

        # get user
        testuser = User.objects.get(username='testuser_system_importer_file_csv_config').id
        # get objects
        analysisstatus_1 = Analysisstatus.objects.get(analysisstatus_name = 'analysisstatus_1').analysisstatus_id
        company_1 = Company.objects.get(company_name = 'company_1').company_id
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
            'csv_choice_company': True,
            'csv_default_company': [str(company_1),],
        })
        # compare
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['csv_choice_company'], ['Decide between CSV or database or nothing.'])

    def test_system_importer_file_csv_config_form_company_column_and_db(self):
        """ test field validation """

        # get user
        testuser = User.objects.get(username='testuser_system_importer_file_csv_config').id
        # get objects
        analysisstatus_1 = Analysisstatus.objects.get(analysisstatus_name = 'analysisstatus_1').analysisstatus_id
        company_1 = Company.objects.get(company_name = 'company_1').company_id
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
            'csv_column_company': '2',
            'csv_default_company': [str(company_1),],
        })
        # compare
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['csv_choice_company'], ['Decide between CSV or database or nothing.'])

    def test_system_importer_file_csv_config_form_company_choice_column_and_db(self):
        """ test field validation """

        # get user
        testuser = User.objects.get(username='testuser_system_importer_file_csv_config').id
        # get objects
        analysisstatus_1 = Analysisstatus.objects.get(analysisstatus_name = 'analysisstatus_1').analysisstatus_id
        company_1 = Company.objects.get(company_name = 'company_1').company_id
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
            'csv_choice_company': True,
            'csv_column_company': '2',
            'csv_default_company': [str(company_1),],
        })
        # compare
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['csv_choice_company'], ['Decide between CSV or database or nothing.'])

    def test_system_importer_file_csv_config_form_company_from_csv(self):
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
            'csv_choice_company': True,
            'csv_column_company': '2',
        })
        # compare
        self.assertTrue(form.is_valid())

    def test_system_importer_file_csv_config_form_company_from_db(self):
        """ test field validation """

        # get user
        testuser = User.objects.get(username='testuser_system_importer_file_csv_config').id
        # get objects
        analysisstatus_1 = Analysisstatus.objects.get(analysisstatus_name = 'analysisstatus_1').analysisstatus_id
        company_1 = Company.objects.get(company_name = 'company_1').company_id
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
            'csv_default_company': [str(company_1),],
        })
        # compare
        self.assertTrue(form.is_valid())
