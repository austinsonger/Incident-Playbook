from django.test import TestCase
from dfirtrack_config.forms import SystemExporterSpreadsheetCsvConfigForm

class SystemExporterSpreadsheetCsvConfigFormTestCase(TestCase):
    """ system exporter spreadsheet CSV config form tests """

    def test_system_exporter_spreadsheet_csv_config_spread_csv_system_id_form_label(self):
        """ test form label """

        # get object
        form = SystemExporterSpreadsheetCsvConfigForm()
        # compare
        self.assertEqual(form.fields['spread_csv_system_id'].label, 'Export system ID')

    def test_system_exporter_spreadsheet_csv_config_spread_csv_dnsname_form_label(self):
        """ test form label """

        # get object
        form = SystemExporterSpreadsheetCsvConfigForm()
        # compare
        self.assertEqual(form.fields['spread_csv_dnsname'].label, 'Export DNS name')

    def test_system_exporter_spreadsheet_csv_config_spread_csv_domain_form_label(self):
        """ test form label """

        # get object
        form = SystemExporterSpreadsheetCsvConfigForm()
        # compare
        self.assertEqual(form.fields['spread_csv_domain'].label, 'Export domain')

    def test_system_exporter_spreadsheet_csv_config_spread_csv_systemstatus_form_label(self):
        """ test form label """

        # get object
        form = SystemExporterSpreadsheetCsvConfigForm()
        # compare
        self.assertEqual(form.fields['spread_csv_systemstatus'].label, 'Export systemstatus')

    def test_system_exporter_spreadsheet_csv_config_spread_csv_analysisstatus_form_label(self):
        """ test form label """

        # get object
        form = SystemExporterSpreadsheetCsvConfigForm()
        # compare
        self.assertEqual(form.fields['spread_csv_analysisstatus'].label, 'Export analysisstatus')

    def test_system_exporter_spreadsheet_csv_config_spread_csv_reason_form_label(self):
        """ test form label """

        # get object
        form = SystemExporterSpreadsheetCsvConfigForm()
        # compare
        self.assertEqual(form.fields['spread_csv_reason'].label, 'Export reason')

    def test_system_exporter_spreadsheet_csv_config_spread_csv_recommendation_form_label(self):
        """ test form label """

        # get object
        form = SystemExporterSpreadsheetCsvConfigForm()
        # compare
        self.assertEqual(form.fields['spread_csv_recommendation'].label, 'Export recommendation')

    def test_system_exporter_spreadsheet_csv_config_spread_csv_systemtype_form_label(self):
        """ test form label """

        # get object
        form = SystemExporterSpreadsheetCsvConfigForm()
        # compare
        self.assertEqual(form.fields['spread_csv_systemtype'].label, 'Export systemtype')

    def test_system_exporter_spreadsheet_csv_config_spread_csv_ip_form_label(self):
        """ test form label """

        # get object
        form = SystemExporterSpreadsheetCsvConfigForm()
        # compare
        self.assertEqual(form.fields['spread_csv_ip'].label, 'Export IP')

    def test_system_exporter_spreadsheet_csv_config_spread_csv_os_form_label(self):
        """ test form label """

        # get object
        form = SystemExporterSpreadsheetCsvConfigForm()
        # compare
        self.assertEqual(form.fields['spread_csv_os'].label, 'Export OS')

    def test_system_exporter_spreadsheet_csv_config_spread_csv_company_form_label(self):
        """ test form label """

        # get object
        form = SystemExporterSpreadsheetCsvConfigForm()
        # compare
        self.assertEqual(form.fields['spread_csv_company'].label, 'Export company')

    def test_system_exporter_spreadsheet_csv_config_spread_csv_location_form_label(self):
        """ test form label """

        # get object
        form = SystemExporterSpreadsheetCsvConfigForm()
        # compare
        self.assertEqual(form.fields['spread_csv_location'].label, 'Export location')

    def test_system_exporter_spreadsheet_csv_config_spread_csv_serviceprovider_form_label(self):
        """ test form label """

        # get object
        form = SystemExporterSpreadsheetCsvConfigForm()
        # compare
        self.assertEqual(form.fields['spread_csv_serviceprovider'].label, 'Export serviceprovider')

    def test_system_exporter_spreadsheet_csv_config_spread_csv_tag_form_label(self):
        """ test form label """

        # get object
        form = SystemExporterSpreadsheetCsvConfigForm()
        # compare
        self.assertEqual(form.fields['spread_csv_tag'].label, 'Export tag')

    def test_system_exporter_spreadsheet_csv_config_spread_csv_case_form_label(self):
        """ test form label """

        # get object
        form = SystemExporterSpreadsheetCsvConfigForm()
        # compare
        self.assertEqual(form.fields['spread_csv_case'].label, 'Export case')

    def test_system_exporter_spreadsheet_csv_config_spread_csv_system_create_time_form_label(self):
        """ test form label """

        # get object
        form = SystemExporterSpreadsheetCsvConfigForm()
        # compare
        self.assertEqual(form.fields['spread_csv_system_create_time'].label, 'Export system create time')

    def test_system_exporter_spreadsheet_csv_config_spread_csv_system_modify_time_form_label(self):
        """ test form label """

        # get object
        form = SystemExporterSpreadsheetCsvConfigForm()
        # compare
        self.assertEqual(form.fields['spread_csv_system_modify_time'].label, 'Export system modify time')

    def test_system_exporter_spreadsheet_csv_config_form_empty(self):
        """ test minimum form requirements / VALID """

        # get object
        form = SystemExporterSpreadsheetCsvConfigForm(data = {})
        # compare
        self.assertTrue(form.is_valid())
