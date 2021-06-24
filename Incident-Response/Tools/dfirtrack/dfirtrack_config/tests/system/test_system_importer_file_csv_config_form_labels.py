from django.test import TestCase
from dfirtrack_config.forms import SystemImporterFileCsvConfigForm


class SystemImporterFileCsvConfigFormLabelTestCase(TestCase):
    """ system importer file CSV config form tests """

    @classmethod
    def setUpTestData(cls):

        pass

    def test_system_importer_file_csv_config_labels(self):
        """ test form labels """

        # get form
        form = SystemImporterFileCsvConfigForm()
        # compare
        self.assertEqual(form.fields['csv_import_username'].label, 'Use this user for the import (*)')
        self.assertEqual(form.fields['csv_default_systemstatus'].label, 'Set from database (*)')
        self.assertEqual(form.fields['csv_default_analysisstatus'].label, 'Set from database (*)')
        self.assertEqual(form.fields['csv_default_tagfree_systemstatus'].label, 'Set from database (no tags assigned)')
        self.assertEqual(form.fields['csv_default_tagfree_analysisstatus'].label, 'Set from database (no tags assigned)')
        self.assertEqual(form.fields['csv_default_dnsname'].label, 'Set from database')
        self.assertEqual(form.fields['csv_default_domain'].label, 'Set from database')
        self.assertEqual(form.fields['csv_default_location'].label, 'Set from database')
        self.assertEqual(form.fields['csv_default_os'].label, 'Set from database')
        self.assertEqual(form.fields['csv_default_reason'].label, 'Set from database')
        self.assertEqual(form.fields['csv_default_recommendation'].label, 'Set from database')
        self.assertEqual(form.fields['csv_default_serviceprovider'].label, 'Set from database')
        self.assertEqual(form.fields['csv_default_systemtype'].label, 'Set from database')
        self.assertEqual(form.fields['csv_default_case'].label, 'Set from database')
        self.assertEqual(form.fields['csv_default_company'].label, 'Set from database')
        self.assertEqual(form.fields['csv_default_tag'].label, 'Set from database')
        self.assertEqual(form.fields['csv_column_system'].label, 'CSV column (*)')
        self.assertEqual(form.fields['csv_skip_existing_system'].label, 'Skip existing systems')
        self.assertEqual(form.fields['csv_headline'].label, 'CSV file contains a headline row')
        self.assertEqual(form.fields['csv_import_path'].label, 'Path to CSV file (*)')
        self.assertEqual(form.fields['csv_import_filename'].label, 'File name of CSV file (*)')
        self.assertEqual(form.fields['csv_remove_systemstatus'].label, 'Overwrite for existing systems')
        self.assertEqual(form.fields['csv_remove_analysisstatus'].label, 'Overwrite for existing systems')
        self.assertEqual(form.fields['csv_choice_tagfree_systemstatus'].label, 'Set alternative (no tags assigned)')
        self.assertEqual(form.fields['csv_choice_tagfree_analysisstatus'].label, 'Set alternative (no tags assigned)')
        self.assertEqual(form.fields['csv_tag_lock_systemstatus'].label, 'Tag that preserves systemstatus (*)')
        self.assertEqual(form.fields['csv_tag_lock_analysisstatus'].label, 'Tag that preserves analysisstatus (*)')
        self.assertEqual(form.fields['csv_choice_ip'].label, 'Set from CSV')
        self.assertEqual(form.fields['csv_column_ip'].label, 'CSV column')
        self.assertEqual(form.fields['csv_remove_ip'].label, 'Overwrite for existing systems')
        self.assertEqual(form.fields['csv_choice_dnsname'].label, 'Set from CSV')
        self.assertEqual(form.fields['csv_column_dnsname'].label, 'CSV column')
        self.assertEqual(form.fields['csv_remove_dnsname'].label, 'Overwrite for existing systems')
        self.assertEqual(form.fields['csv_choice_domain'].label, 'Set from CSV')
        self.assertEqual(form.fields['csv_column_domain'].label, 'CSV column')
        self.assertEqual(form.fields['csv_remove_domain'].label, 'Overwrite for existing systems')
        self.assertEqual(form.fields['csv_choice_location'].label, 'Set from CSV')
        self.assertEqual(form.fields['csv_column_location'].label, 'CSV column')
        self.assertEqual(form.fields['csv_remove_location'].label, 'Overwrite for existing systems')
        self.assertEqual(form.fields['csv_choice_os'].label, 'Set from CSV')
        self.assertEqual(form.fields['csv_column_os'].label, 'CSV column')
        self.assertEqual(form.fields['csv_remove_os'].label, 'Overwrite for existing systems')
        self.assertEqual(form.fields['csv_choice_reason'].label, 'Set from CSV')
        self.assertEqual(form.fields['csv_column_reason'].label, 'CSV column')
        self.assertEqual(form.fields['csv_remove_reason'].label, 'Overwrite for existing systems')
        self.assertEqual(form.fields['csv_choice_recommendation'].label, 'Set from CSV')
        self.assertEqual(form.fields['csv_column_recommendation'].label, 'CSV column')
        self.assertEqual(form.fields['csv_remove_recommendation'].label, 'Overwrite for existing systems')
        self.assertEqual(form.fields['csv_choice_serviceprovider'].label, 'Set from CSV')
        self.assertEqual(form.fields['csv_column_serviceprovider'].label, 'CSV column')
        self.assertEqual(form.fields['csv_remove_serviceprovider'].label, 'Overwrite for existing systems')
        self.assertEqual(form.fields['csv_choice_systemtype'].label, 'Set from CSV')
        self.assertEqual(form.fields['csv_column_systemtype'].label, 'CSV column')
        self.assertEqual(form.fields['csv_remove_systemtype'].label, 'Overwrite for existing systems')
        self.assertEqual(form.fields['csv_choice_case'].label, 'Set from CSV')
        self.assertEqual(form.fields['csv_column_case'].label, 'CSV column')
        self.assertEqual(form.fields['csv_remove_case'].label, 'Overwrite for existing systems')
        self.assertEqual(form.fields['csv_choice_company'].label, 'Set from CSV')
        self.assertEqual(form.fields['csv_column_company'].label, 'CSV column')
        self.assertEqual(form.fields['csv_remove_company'].label, 'Overwrite for existing systems')
        self.assertEqual(form.fields['csv_choice_tag'].label, 'Set from CSV')
        self.assertEqual(form.fields['csv_column_tag'].label, 'CSV column')
        self.assertEqual(form.fields['csv_remove_tag'].label, 'Overwrite for existing systems')
        self.assertEqual(form.fields['csv_tag_prefix'].label, 'Prefix for tags imported via CSV')
        self.assertEqual(form.fields['csv_tag_prefix_delimiter'].label, 'Delimiter to separate prefix from tag')
        self.assertEqual(form.fields['csv_field_delimiter'].label, 'CSV field delimiter')
        self.assertEqual(form.fields['csv_text_quote'].label, 'CSV text quotation mark')
        self.assertEqual(form.fields['csv_ip_delimiter'].label, 'IP address delimiter (within CSV field)')
        self.assertEqual(form.fields['csv_tag_delimiter'].label, 'Tag delimiter (within CSV field)')
