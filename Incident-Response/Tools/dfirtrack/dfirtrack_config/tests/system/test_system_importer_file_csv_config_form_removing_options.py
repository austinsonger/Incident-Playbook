from django.contrib.auth.models import User
from django.test import TestCase
from dfirtrack_config.forms import SystemImporterFileCsvConfigForm
from dfirtrack_main.models import Analysisstatus, Case, Company, Dnsname, Domain, Location, Os, Reason, Recommendation, Serviceprovider, Systemstatus, Systemtype


class SystemImporterFileCsvConfigFormRemovingOptionsTestCase(TestCase):
    """ system importer file CSV config form tests """

    @classmethod
    def setUpTestData(cls):

        # create user
        User.objects.create_user(username='testuser_system_importer_file_csv_config', password='pt1pI4h5CRTAh1GQb29e')

        # create objects
        Analysisstatus.objects.create(analysisstatus_name = 'analysisstatus_1')
        Systemstatus.objects.create(systemstatus_name = 'systemstatus_1')

    def test_system_importer_file_csv_config_form_remove_skip_systems(self):
        """ test field validation """

        # get user
        testuser = User.objects.get(username='testuser_system_importer_file_csv_config').id
        # get objects
        analysisstatus_1 = Analysisstatus.objects.get(analysisstatus_name = 'analysisstatus_1').analysisstatus_id
        systemstatus_1 = Systemstatus.objects.get(systemstatus_name = 'systemstatus_1').systemstatus_id
        # create string
        either_skip_or_remove_string = 'This choice is only valid if existing systems are not skipped. Either disable this option or disable skipping existing systems.'
        # get form
        form = SystemImporterFileCsvConfigForm(data = {
            'csv_column_system': '1',
            'csv_skip_existing_system': True,
            'csv_import_path': '/tmp',
            'csv_import_filename': 'systems.csv',
            'csv_import_username': str(testuser),
            'csv_default_systemstatus': str(systemstatus_1),
            'csv_remove_systemstatus': True,
            'csv_default_analysisstatus': str(analysisstatus_1),
            'csv_remove_analysisstatus': True,
            'csv_default_tagfree_systemstatus': str(systemstatus_1),
            'csv_default_tagfree_analysisstatus': str(analysisstatus_1),
            'csv_tag_lock_systemstatus': 'LOCK_SYSTEMSTATUS',
            'csv_tag_lock_analysisstatus': 'LOCK_ANALYSISSTATUS',
            'csv_choice_ip': True,
            'csv_column_ip': '2',
            'csv_remove_ip': True,
            'csv_choice_dnsname': True,
            'csv_column_dnsname': '3',
            'csv_remove_dnsname': True,
            'csv_choice_domain': True,
            'csv_column_domain': '4',
            'csv_remove_domain': True,
            'csv_choice_location': True,
            'csv_column_location': '5',
            'csv_remove_location': True,
            'csv_choice_os': True,
            'csv_column_os': '6',
            'csv_remove_os': True,
            'csv_choice_reason': True,
            'csv_column_reason': '7',
            'csv_remove_reason': True,
            'csv_choice_recommendation': True,
            'csv_column_recommendation': '8',
            'csv_remove_recommendation': True,
            'csv_choice_serviceprovider': True,
            'csv_column_serviceprovider': '9',
            'csv_remove_serviceprovider': True,
            'csv_choice_systemtype': True,
            'csv_column_systemtype': '10',
            'csv_remove_systemtype': True,
            'csv_choice_case': True,
            'csv_column_case': '11',
            'csv_remove_case': True,
            'csv_choice_company': True,
            'csv_column_company': '12',
            'csv_remove_company': True,
            'csv_remove_tag': 'tag_remove_prefix',
            'csv_field_delimiter': 'field_comma',
            'csv_text_quote': 'text_double_quotation_marks',
            'csv_ip_delimiter': 'ip_semicolon',
            'csv_tag_delimiter': 'tag_space',
        })
        # compare
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['csv_remove_systemstatus'], [either_skip_or_remove_string])
        self.assertEqual(form.errors['csv_remove_analysisstatus'], [either_skip_or_remove_string])
        self.assertEqual(form.errors['csv_remove_ip'], [either_skip_or_remove_string])
        self.assertEqual(form.errors['csv_remove_dnsname'], [either_skip_or_remove_string])
        self.assertEqual(form.errors['csv_remove_domain'], [either_skip_or_remove_string])
        self.assertEqual(form.errors['csv_remove_location'], [either_skip_or_remove_string])
        self.assertEqual(form.errors['csv_remove_os'], [either_skip_or_remove_string])
        self.assertEqual(form.errors['csv_remove_reason'], [either_skip_or_remove_string])
        self.assertEqual(form.errors['csv_remove_recommendation'], [either_skip_or_remove_string])
        self.assertEqual(form.errors['csv_remove_serviceprovider'], [either_skip_or_remove_string])
        self.assertEqual(form.errors['csv_remove_systemtype'], [either_skip_or_remove_string])
        self.assertEqual(form.errors['csv_remove_case'], [either_skip_or_remove_string])
        self.assertEqual(form.errors['csv_remove_company'], [either_skip_or_remove_string])

    def test_system_importer_file_csv_config_form_remove_no_attribute_selected(self):
        """ test field validation """

        # get user
        testuser = User.objects.get(username='testuser_system_importer_file_csv_config').id
        # get objects
        analysisstatus_1 = Analysisstatus.objects.get(analysisstatus_name = 'analysisstatus_1').analysisstatus_id
        systemstatus_1 = Systemstatus.objects.get(systemstatus_name = 'systemstatus_1').systemstatus_id
        # create string
        remove_string = 'This choice is only valid if attribute is selected.'
        # get form
        form = SystemImporterFileCsvConfigForm(data = {
            'csv_column_system': '1',
            'csv_skip_existing_system': False,
            'csv_import_path': '/tmp',
            'csv_import_filename': 'systems.csv',
            'csv_import_username': str(testuser),
            'csv_default_systemstatus': str(systemstatus_1),
            'csv_remove_systemstatus': True,
            'csv_default_analysisstatus': str(analysisstatus_1),
            'csv_remove_analysisstatus': True,
            'csv_default_tagfree_systemstatus': str(systemstatus_1),
            'csv_default_tagfree_analysisstatus': str(analysisstatus_1),
            'csv_tag_lock_systemstatus': 'LOCK_SYSTEMSTATUS',
            'csv_tag_lock_analysisstatus': 'LOCK_ANALYSISSTATUS',
            'csv_remove_ip': True,
            'csv_remove_dnsname': True,
            'csv_remove_domain': True,
            'csv_remove_location': True,
            'csv_remove_os': True,
            'csv_remove_reason': True,
            'csv_remove_recommendation': True,
            'csv_remove_serviceprovider': True,
            'csv_remove_systemtype': True,
            'csv_remove_case': True,
            'csv_remove_company': True,
            'csv_remove_tag': 'tag_remove_prefix',
            'csv_field_delimiter': 'field_comma',
            'csv_text_quote': 'text_double_quotation_marks',
            'csv_ip_delimiter': 'ip_semicolon',
            'csv_tag_delimiter': 'tag_space',
        })
        # compare
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['csv_remove_ip'], [remove_string])
        self.assertEqual(form.errors['csv_remove_dnsname'], [remove_string])
        self.assertEqual(form.errors['csv_remove_domain'], [remove_string])
        self.assertEqual(form.errors['csv_remove_location'], [remove_string])
        self.assertEqual(form.errors['csv_remove_os'], [remove_string])
        self.assertEqual(form.errors['csv_remove_reason'], [remove_string])
        self.assertEqual(form.errors['csv_remove_recommendation'], [remove_string])
        self.assertEqual(form.errors['csv_remove_serviceprovider'], [remove_string])
        self.assertEqual(form.errors['csv_remove_systemtype'], [remove_string])
        self.assertEqual(form.errors['csv_remove_case'], [remove_string])
        self.assertEqual(form.errors['csv_remove_company'], [remove_string])

    def test_system_importer_file_csv_config_form_remove_csv_valid(self):
        """ test field validation """

        # get user
        testuser = User.objects.get(username='testuser_system_importer_file_csv_config').id
        # get objects
        analysisstatus_1 = Analysisstatus.objects.get(analysisstatus_name = 'analysisstatus_1').analysisstatus_id
        systemstatus_1 = Systemstatus.objects.get(systemstatus_name = 'systemstatus_1').systemstatus_id
        # get form
        form = SystemImporterFileCsvConfigForm(data = {
            'csv_column_system': '1',
            'csv_skip_existing_system': False,
            'csv_import_path': '/tmp',
            'csv_import_filename': 'systems.csv',
            'csv_import_username': str(testuser),
            'csv_default_systemstatus': str(systemstatus_1),
            'csv_remove_systemstatus': True,
            'csv_default_analysisstatus': str(analysisstatus_1),
            'csv_remove_analysisstatus': True,
            'csv_default_tagfree_systemstatus': str(systemstatus_1),
            'csv_default_tagfree_analysisstatus': str(analysisstatus_1),
            'csv_tag_lock_systemstatus': 'LOCK_SYSTEMSTATUS',
            'csv_tag_lock_analysisstatus': 'LOCK_ANALYSISSTATUS',
            'csv_choice_ip': True,
            'csv_column_ip': '2',
            'csv_remove_ip': True,
            'csv_choice_dnsname': True,
            'csv_column_dnsname': '3',
            'csv_remove_dnsname': True,
            'csv_choice_domain': True,
            'csv_column_domain': '4',
            'csv_remove_domain': True,
            'csv_choice_location': True,
            'csv_column_location': '5',
            'csv_remove_location': True,
            'csv_choice_os': True,
            'csv_column_os': '6',
            'csv_remove_os': True,
            'csv_choice_reason': True,
            'csv_column_reason': '7',
            'csv_remove_reason': True,
            'csv_choice_recommendation': True,
            'csv_column_recommendation': '8',
            'csv_remove_recommendation': True,
            'csv_choice_serviceprovider': True,
            'csv_column_serviceprovider': '9',
            'csv_remove_serviceprovider': True,
            'csv_choice_systemtype': True,
            'csv_column_systemtype': '10',
            'csv_remove_systemtype': True,
            'csv_choice_case': True,
            'csv_column_case': '11',
            'csv_remove_case': True,
            'csv_choice_company': True,
            'csv_column_company': '12',
            'csv_remove_company': True,
            'csv_remove_tag': 'tag_remove_prefix',
            'csv_field_delimiter': 'field_comma',
            'csv_text_quote': 'text_double_quotation_marks',
            'csv_ip_delimiter': 'ip_semicolon',
            'csv_tag_delimiter': 'tag_space',
        })
        # compare
        self.assertTrue(form.is_valid())

    def test_system_importer_file_csv_config_form_remove_db_valid(self):
        """ test field validation """

        # get user
        testuser = User.objects.get(username='testuser_system_importer_file_csv_config')
        # get objects
        analysisstatus_1 = Analysisstatus.objects.get(analysisstatus_name = 'analysisstatus_1').analysisstatus_id
        systemstatus_1 = Systemstatus.objects.get(systemstatus_name = 'systemstatus_1').systemstatus_id
        # create objects
        case_1 = Case.objects.create(
            case_name = 'case_1',
            case_is_incident = False,
            case_created_by_user_id = testuser,
        ).case_id
        company_1 = Company.objects.create(company_name = 'company_1').company_id
        dnsname_1 = Dnsname.objects.create(dnsname_name = 'dnsname_1').dnsname_id
        domain_1 = Domain.objects.create(domain_name = 'domain_1').domain_id
        location_1 = Location.objects.create(location_name = 'location_1').location_id
        os_1 = Os.objects.create(os_name = 'os_1').os_id
        reason_1 = Reason.objects.create(reason_name = 'reason_1').reason_id
        recommendation_1 = Recommendation.objects.create(recommendation_name = 'recommendation_1').recommendation_id
        serviceprovider_1 = Serviceprovider.objects.create(serviceprovider_name = 'serviceprovider_1').serviceprovider_id
        systemtype_1 = Systemtype.objects.create(systemtype_name = 'systemtype_1').systemtype_id
        # get form
        form = SystemImporterFileCsvConfigForm(data = {
            'csv_column_system': '1',
            'csv_skip_existing_system': False,
            'csv_import_path': '/tmp',
            'csv_import_filename': 'systems.csv',
            'csv_import_username': str(testuser.id),
            'csv_default_systemstatus': str(systemstatus_1),
            'csv_remove_systemstatus': True,
            'csv_default_analysisstatus': str(analysisstatus_1),
            'csv_remove_analysisstatus': True,
            'csv_default_tagfree_systemstatus': str(systemstatus_1),
            'csv_default_tagfree_analysisstatus': str(analysisstatus_1),
            'csv_tag_lock_systemstatus': 'LOCK_SYSTEMSTATUS',
            'csv_tag_lock_analysisstatus': 'LOCK_ANALYSISSTATUS',
            'csv_default_dnsname': str(dnsname_1),
            'csv_remove_dnsname': True,
            'csv_default_domain': str(domain_1),
            'csv_remove_domain': True,
            'csv_default_location': str(location_1),
            'csv_remove_location': True,
            'csv_default_os': str(os_1),
            'csv_remove_os': True,
            'csv_default_reason': str(reason_1),
            'csv_remove_reason': True,
            'csv_default_recommendation': str(recommendation_1),
            'csv_remove_recommendation': True,
            'csv_default_serviceprovider': str(serviceprovider_1),
            'csv_remove_serviceprovider': True,
            'csv_default_systemtype': str(systemtype_1),
            'csv_remove_systemtype': True,
            'csv_default_case': [str(case_1)],
            'csv_remove_case': True,
            'csv_default_company': [str(company_1)],
            'csv_remove_company': True,
            'csv_remove_tag': 'tag_remove_prefix',
            'csv_field_delimiter': 'field_comma',
            'csv_text_quote': 'text_double_quotation_marks',
            'csv_ip_delimiter': 'ip_semicolon',
            'csv_tag_delimiter': 'tag_space',
        })
        # compare
        self.assertTrue(form.is_valid())
