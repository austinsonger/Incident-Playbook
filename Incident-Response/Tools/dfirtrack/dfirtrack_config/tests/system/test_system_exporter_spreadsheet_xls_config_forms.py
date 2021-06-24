from django.test import TestCase
from dfirtrack_config.forms import SystemExporterSpreadsheetXlsConfigForm

class SystemExporterSpreadsheetXlsConfigFormTestCase(TestCase):
    """ system exporter spreadsheet XLS config form tests """

    def test_system_exporter_spreadsheet_xls_config_spread_xls_system_id_form_label(self):
        """ test form label """

        # get object
        form = SystemExporterSpreadsheetXlsConfigForm()
        # compare
        self.assertEqual(form.fields['spread_xls_system_id'].label, 'Export system ID')

    def test_system_exporter_spreadsheet_xls_config_spread_xls_dnsname_form_label(self):
        """ test form label """

        # get object
        form = SystemExporterSpreadsheetXlsConfigForm()
        # compare
        self.assertEqual(form.fields['spread_xls_dnsname'].label, 'Export DNS name')

    def test_system_exporter_spreadsheet_xls_config_spread_xls_domain_form_label(self):
        """ test form label """

        # get object
        form = SystemExporterSpreadsheetXlsConfigForm()
        # compare
        self.assertEqual(form.fields['spread_xls_domain'].label, 'Export domain')

    def test_system_exporter_spreadsheet_xls_config_spread_xls_systemstatus_form_label(self):
        """ test form label """

        # get object
        form = SystemExporterSpreadsheetXlsConfigForm()
        # compare
        self.assertEqual(form.fields['spread_xls_systemstatus'].label, 'Export systemstatus')

    def test_system_exporter_spreadsheet_xls_config_spread_xls_analysisstatus_form_label(self):
        """ test form label """

        # get object
        form = SystemExporterSpreadsheetXlsConfigForm()
        # compare
        self.assertEqual(form.fields['spread_xls_analysisstatus'].label, 'Export analysisstatus')

    def test_system_exporter_spreadsheet_xls_config_spread_xls_reason_form_label(self):
        """ test form label """

        # get object
        form = SystemExporterSpreadsheetXlsConfigForm()
        # compare
        self.assertEqual(form.fields['spread_xls_reason'].label, 'Export reason')

    def test_system_exporter_spreadsheet_xls_config_spread_xls_recommendation_form_label(self):
        """ test form label """

        # get object
        form = SystemExporterSpreadsheetXlsConfigForm()
        # compare
        self.assertEqual(form.fields['spread_xls_recommendation'].label, 'Export recommendation')

    def test_system_exporter_spreadsheet_xls_config_spread_xls_systemtype_form_label(self):
        """ test form label """

        # get object
        form = SystemExporterSpreadsheetXlsConfigForm()
        # compare
        self.assertEqual(form.fields['spread_xls_systemtype'].label, 'Export systemtype')

    def test_system_exporter_spreadsheet_xls_config_spread_xls_ip_form_label(self):
        """ test form label """

        # get object
        form = SystemExporterSpreadsheetXlsConfigForm()
        # compare
        self.assertEqual(form.fields['spread_xls_ip'].label, 'Export IP')

    def test_system_exporter_spreadsheet_xls_config_spread_xls_os_form_label(self):
        """ test form label """

        # get object
        form = SystemExporterSpreadsheetXlsConfigForm()
        # compare
        self.assertEqual(form.fields['spread_xls_os'].label, 'Export OS')

    def test_system_exporter_spreadsheet_xls_config_spread_xls_company_form_label(self):
        """ test form label """

        # get object
        form = SystemExporterSpreadsheetXlsConfigForm()
        # compare
        self.assertEqual(form.fields['spread_xls_company'].label, 'Export company')

    def test_system_exporter_spreadsheet_xls_config_spread_xls_location_form_label(self):
        """ test form label """

        # get object
        form = SystemExporterSpreadsheetXlsConfigForm()
        # compare
        self.assertEqual(form.fields['spread_xls_location'].label, 'Export location')

    def test_system_exporter_spreadsheet_xls_config_spread_xls_serviceprovider_form_label(self):
        """ test form label """

        # get object
        form = SystemExporterSpreadsheetXlsConfigForm()
        # compare
        self.assertEqual(form.fields['spread_xls_serviceprovider'].label, 'Export serviceprovider')

    def test_system_exporter_spreadsheet_xls_config_spread_xls_tag_form_label(self):
        """ test form label """

        # get object
        form = SystemExporterSpreadsheetXlsConfigForm()
        # compare
        self.assertEqual(form.fields['spread_xls_tag'].label, 'Export tag')

    def test_system_exporter_spreadsheet_xls_config_spread_xls_case_form_label(self):
        """ test form label """

        # get object
        form = SystemExporterSpreadsheetXlsConfigForm()
        # compare
        self.assertEqual(form.fields['spread_xls_case'].label, 'Export case')

    def test_system_exporter_spreadsheet_xls_config_spread_xls_system_create_time_form_label(self):
        """ test form label """

        # get object
        form = SystemExporterSpreadsheetXlsConfigForm()
        # compare
        self.assertEqual(form.fields['spread_xls_system_create_time'].label, 'Export system create time')

    def test_system_exporter_spreadsheet_xls_config_spread_xls_system_modify_time_form_label(self):
        """ test form label """

        # get object
        form = SystemExporterSpreadsheetXlsConfigForm()
        # compare
        self.assertEqual(form.fields['spread_xls_system_modify_time'].label, 'Export system modify time')

    def test_system_exporter_spreadsheet_xls_config_spread_xls_worksheet_systemstatus_form_label(self):
        """ test form label """

        # get object
        form = SystemExporterSpreadsheetXlsConfigForm()
        # compare
        self.assertEqual(form.fields['spread_xls_worksheet_systemstatus'].label, 'Export worksheet to explain systemstatus')

    def test_system_exporter_spreadsheet_xls_config_spread_xls_worksheet_analysisstatus_form_label(self):
        """ test form label """

        # get object
        form = SystemExporterSpreadsheetXlsConfigForm()
        # compare
        self.assertEqual(form.fields['spread_xls_worksheet_analysisstatus'].label, 'Export worksheet to explain analysisstatus')

    def test_system_exporter_spreadsheet_xls_config_spread_xls_worksheet_reason_form_label(self):
        """ test form label """

        # get object
        form = SystemExporterSpreadsheetXlsConfigForm()
        # compare
        self.assertEqual(form.fields['spread_xls_worksheet_reason'].label, 'Export worksheet to explain reason')

    def test_system_exporter_spreadsheet_xls_config_spread_xls_worksheet_recommendation_form_label(self):
        """ test form label """

        # get object
        form = SystemExporterSpreadsheetXlsConfigForm()
        # compare
        self.assertEqual(form.fields['spread_xls_worksheet_recommendation'].label, 'Export worksheet to explain recommendation')

    def test_system_exporter_spreadsheet_xls_config_spread_xls_worksheet_tag_form_label(self):
        """ test form label """

        # get object
        form = SystemExporterSpreadsheetXlsConfigForm()
        # compare
        self.assertEqual(form.fields['spread_xls_worksheet_tag'].label, 'Export worksheet to explain tag')

    def test_system_exporter_spreadsheet_xls_config_form_empty(self):
        """ test minimum form requirements / VALID """

        # get object
        form = SystemExporterSpreadsheetXlsConfigForm(data = {})
        # compare
        self.assertTrue(form.is_valid())
